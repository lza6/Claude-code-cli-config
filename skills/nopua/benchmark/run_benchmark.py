#!/usr/bin/env python3
"""
NoPUA Benchmark Runner — Automated experiment runner for the NoPUA academic paper.

Runs AI agents across multiple scenarios, conditions (Baseline, NoPUA, PUA),
and models to collect structured performance data for statistical analysis.

Usage:
    python run_benchmark.py --model claude-sonnet-4 --condition all --runs 5
    python run_benchmark.py --model gpt-4o --condition nopua --scenario 3
    python run_benchmark.py --model gemini-2.5-pro --condition pua --runs 3 --output-dir results/gemini
"""

import argparse
import asyncio
import json
import logging
import os
import re
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MODELS = {
    "claude-sonnet-4": {
        "provider": "anthropic",
        "model_id": "claude-sonnet-4-20250514",
    },
    "gpt-4o": {
        "provider": "openai",
        "model_id": "gpt-4o",
    },
    "gemini-2.5-pro": {
        "provider": "google",
        "model_id": "gemini-2.5-pro-preview-06-05",
    },
}

CONDITIONS = ["baseline", "nopua", "pua"]

DEFAULT_RUNS = 5
DEFAULT_OUTPUT_DIR = "results"
DEFAULT_CODEBASE_PATH = r"D:\Projects\private-project"
NOPUA_SKILL_PATH = Path(__file__).parent.parent / "skills" / "nopua" / "SKILL.md"
PUA_PROMPT_PATH = Path(__file__).parent / "pua_prompt.txt"
SCENARIOS_PATH = Path(__file__).parent / "scenarios.json"

MAX_RETRIES = 3
RETRY_BASE_DELAY = 2.0  # seconds, exponential backoff
SEMAPHORE_LIMIT = 3  # max concurrent scenario runs within a condition

# How many "turns" the agent gets to investigate (read files, run commands, think)
MAX_AGENT_TURNS = 15

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("benchmark")

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class BenchmarkResult:
    scenario_id: int
    scenario_name: str
    condition: str
    model: str
    run_number: int
    timestamp: str = ""
    steps_taken: int = 0
    tools_used: list[str] = field(default_factory=list)
    investigation_notes: str = ""
    issues_found: list[str] = field(default_factory=list)
    went_beyond_ask: bool = False
    verification_done: bool = False
    hidden_issues: list[str] = field(default_factory=list)
    approach_changes: int = 0
    approach_change_detail: str = ""
    root_cause: str = ""
    recommended_fix: str = ""
    self_corrections: int = 0
    raw_response: str = ""
    duration_seconds: float = 0.0
    error: str = ""


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------

def load_scenarios() -> list[dict]:
    with open(SCENARIOS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_nopua_prompt() -> str:
    with open(NOPUA_SKILL_PATH, "r", encoding="utf-8") as f:
        return f.read()


def load_pua_prompt() -> str:
    with open(PUA_PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


def build_system_prompt(condition: str, codebase_path: str) -> str:
    """Build the system prompt for a given condition."""
    base = (
        f"You are an expert software engineer investigating issues in a codebase "
        f"located at {codebase_path}.\n\n"
        f"You have access to the following tools:\n"
        f"- read_file(path): Read the contents of a file\n"
        f"- list_dir(path): List files in a directory\n"
        f"- search_text(pattern, path): Search for text patterns in files\n"
        f"- run_command(cmd): Run a shell command and get output\n\n"
        f"When investigating, use these tools to examine the codebase. "
        f"Do not guess — read the actual code.\n\n"
    )

    if condition == "baseline":
        return base + (
            "Investigate the issue described below. Report what you find, "
            "including any issues, root causes, and recommended fixes."
        )
    elif condition == "nopua":
        nopua_skill = load_nopua_prompt()
        return base + (
            "The following skill guides your approach:\n\n"
            f"---\n{nopua_skill}\n---\n\n"
            "Apply this skill's principles as you investigate the issue below."
        )
    elif condition == "pua":
        pua_prompt = load_pua_prompt()
        return base + (
            "The following instructions govern your behavior:\n\n"
            f"---\n{pua_prompt}\n---\n\n"
            "Follow these instructions as you investigate the issue below."
        )
    else:
        raise ValueError(f"Unknown condition: {condition}")


def build_task_prompt(scenario: dict) -> str:
    """Build the user task prompt from a scenario."""
    return (
        f"## Task: {scenario['name']}\n\n"
        f"{scenario['task']}\n\n"
        f"After your investigation, provide a structured summary with:\n"
        f"1. **Issues Found**: List each issue clearly\n"
        f"2. **Hidden Issues**: Any additional issues you discovered beyond the ask\n"
        f"3. **Root Cause**: The fundamental cause(s)\n"
        f"4. **Recommended Fix**: Specific fix recommendations\n"
        f"5. **Steps Taken**: What you investigated and how\n"
        f"6. **Tools Used**: Which tools you used (read_file, list_dir, search_text, run_command)\n"
        f"7. **Verification**: Did you verify your findings? How?\n"
    )


def build_file_context(scenario: dict, codebase_path: str) -> str:
    """
    Pre-read relevant source files and include them in the prompt so the agent
    can investigate without needing actual tool-use (simulated tool access).
    """
    # Extract file paths from the task description
    task_text = scenario["task"]
    # Match paths like D:\Projects\private-project\src\... or relative src/...
    path_patterns = re.findall(
        r'(?:D:\\Projects\\private-project\\|(?:src[/\\]))[\w\\/.]+\.py',
        task_text
    )
    # Also match directory references
    dir_patterns = re.findall(
        r'(?:D:\\Projects\\private-project\\|(?:src[/\\]))[\w\\/]+/',
        task_text
    )

    files_content = []
    base = Path(codebase_path)

    for pattern in path_patterns:
        # Normalize to relative path
        rel = pattern.replace("D:\\Projects\\private-project\\", "").replace("\\", "/")
        fpath = base / rel
        if fpath.exists():
            try:
                content = fpath.read_text(encoding="utf-8")
                files_content.append(f"### File: {rel}\n```python\n{content}\n```\n")
            except Exception as e:
                files_content.append(f"### File: {rel}\n[Error reading: {e}]\n")

    for pattern in dir_patterns:
        rel = pattern.replace("D:\\Projects\\private-project\\", "").replace("\\", "/").rstrip("/")
        dpath = base / rel
        if dpath.exists() and dpath.is_dir():
            try:
                listing = "\n".join(
                    f"  {p.name}" for p in sorted(dpath.iterdir())
                )
                files_content.append(f"### Directory: {rel}/\n```\n{listing}\n```\n")
                # Also read .py files in the directory
                for pyfile in sorted(dpath.glob("*.py")):
                    try:
                        content = pyfile.read_text(encoding="utf-8")
                        frel = f"{rel}/{pyfile.name}"
                        files_content.append(
                            f"### File: {frel}\n```python\n{content}\n```\n"
                        )
                    except Exception:
                        pass
            except Exception:
                pass

    if files_content:
        return (
            "\n## Available Source Files\n"
            "Below are the relevant source files from the codebase for your investigation:\n\n"
            + "\n".join(files_content)
        )
    return ""


# ---------------------------------------------------------------------------
# Extraction — parse structured data from agent response
# ---------------------------------------------------------------------------

EXTRACTION_PROMPT = """\
You are a structured data extractor. Given the agent's investigation response below, \
extract the following fields as JSON. Be precise and faithful to what the agent actually said.

Agent response:
---
{response}
---

Extract this JSON (use empty lists/strings if not present):
{{
  "issues_found": ["issue 1", "issue 2", ...],
  "hidden_issues": ["additional issue beyond the original ask", ...],
  "root_cause": "the fundamental cause",
  "recommended_fix": "specific recommendations",
  "steps_taken": <number of distinct investigation steps>,
  "tools_used": ["read_file", "search_text", ...],
  "went_beyond_ask": true/false (did the agent find issues beyond what was asked?),
  "verification_done": true/false (did the agent verify findings with tools/tests?),
  "approach_changes": <number of times the agent changed investigation direction>,
  "approach_change_detail": "description of approach changes if any",
  "self_corrections": <number of times the agent corrected its own earlier conclusion>
}}

Return ONLY valid JSON, no markdown fencing, no explanation.
"""


async def extract_structured_result(
    response: str, model_config: dict
) -> dict[str, Any]:
    """Use a lightweight model call to extract structured data from agent response."""
    prompt = EXTRACTION_PROMPT.format(response=response[:8000])  # truncate if huge

    provider = model_config["provider"]
    try:
        if provider == "anthropic":
            import anthropic
            client = anthropic.AsyncAnthropic()
            msg = await client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
            )
            text = msg.content[0].text
        elif provider == "openai":
            import openai
            client = openai.AsyncOpenAI()
            resp = await client.chat.completions.create(
                model="gpt-4o-mini",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
            )
            text = resp.choices[0].message.content
        elif provider == "google":
            import google.generativeai as genai
            model = genai.GenerativeModel("gemini-2.0-flash")
            resp = await asyncio.to_thread(
                model.generate_content, prompt
            )
            text = resp.text
        else:
            return {}

        # Parse JSON from response
        text = text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```\w*\n?", "", text)
            text = re.sub(r"\n?```$", "", text)
        return json.loads(text)
    except Exception as e:
        log.warning(f"Extraction failed: {e}")
        return {}


# ---------------------------------------------------------------------------
# Provider-specific agent runners
# ---------------------------------------------------------------------------

async def run_anthropic(
    system_prompt: str, user_prompt: str, model_id: str
) -> str:
    """Run a single agent session with Anthropic Claude."""
    import anthropic

    client = anthropic.AsyncAnthropic()
    msg = await client.messages.create(
        model=model_id,
        max_tokens=8192,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return msg.content[0].text


async def run_openai(
    system_prompt: str, user_prompt: str, model_id: str
) -> str:
    """Run a single agent session with OpenAI."""
    import openai

    client = openai.AsyncOpenAI()
    resp = await client.chat.completions.create(
        model=model_id,
        max_tokens=8192,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return resp.choices[0].message.content


async def run_google(
    system_prompt: str, user_prompt: str, model_id: str
) -> str:
    """Run a single agent session with Google Gemini."""
    import google.generativeai as genai

    model = genai.GenerativeModel(
        model_id,
        system_instruction=system_prompt,
    )
    resp = await asyncio.to_thread(
        model.generate_content, user_prompt
    )
    return resp.text


PROVIDER_RUNNERS = {
    "anthropic": run_anthropic,
    "openai": run_openai,
    "google": run_google,
}


# ---------------------------------------------------------------------------
# Core benchmark logic
# ---------------------------------------------------------------------------

async def run_single_scenario(
    scenario: dict,
    condition: str,
    model_name: str,
    run_number: int,
    codebase_path: str,
    semaphore: asyncio.Semaphore,
) -> BenchmarkResult:
    """Run a single scenario/condition/run combination."""
    model_config = MODELS[model_name]
    result = BenchmarkResult(
        scenario_id=scenario["id"],
        scenario_name=scenario["name"],
        condition=condition,
        model=model_name,
        run_number=run_number,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    system_prompt = build_system_prompt(condition, codebase_path)
    task_prompt = build_task_prompt(scenario)
    file_context = build_file_context(scenario, codebase_path)
    user_prompt = task_prompt + file_context

    runner = PROVIDER_RUNNERS[model_config["provider"]]
    start_time = time.monotonic()

    async with semaphore:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                log.info(
                    f"[{model_name}] Scenario {scenario['id']} | "
                    f"{condition} | Run {run_number} | Attempt {attempt}"
                )
                response = await runner(
                    system_prompt, user_prompt, model_config["model_id"]
                )
                result.raw_response = response
                result.duration_seconds = round(time.monotonic() - start_time, 2)

                # Extract structured data
                extracted = await extract_structured_result(response, model_config)
                if extracted:
                    result.issues_found = extracted.get("issues_found", [])
                    result.hidden_issues = extracted.get("hidden_issues", [])
                    result.root_cause = extracted.get("root_cause", "")
                    result.recommended_fix = extracted.get("recommended_fix", "")
                    result.steps_taken = extracted.get("steps_taken", 0)
                    result.tools_used = extracted.get("tools_used", [])
                    result.went_beyond_ask = extracted.get("went_beyond_ask", False)
                    result.verification_done = extracted.get("verification_done", False)
                    result.approach_changes = extracted.get("approach_changes", 0)
                    result.approach_change_detail = extracted.get("approach_change_detail", "")
                    result.self_corrections = extracted.get("self_corrections", 0)
                    result.investigation_notes = response[:500]

                log.info(
                    f"  ✓ Done: {len(result.issues_found)} issues, "
                    f"{len(result.hidden_issues)} hidden, "
                    f"{result.duration_seconds}s"
                )
                break

            except Exception as e:
                err_msg = f"{type(e).__name__}: {e}"
                log.warning(f"  ✗ Attempt {attempt} failed: {err_msg}")
                if attempt == MAX_RETRIES:
                    result.error = err_msg
                    result.duration_seconds = round(
                        time.monotonic() - start_time, 2
                    )
                else:
                    delay = RETRY_BASE_DELAY * (2 ** (attempt - 1))
                    log.info(f"  Retrying in {delay}s...")
                    await asyncio.sleep(delay)

    return result


async def run_condition(
    scenarios: list[dict],
    condition: str,
    model_name: str,
    num_runs: int,
    codebase_path: str,
    output_dir: Path,
    scenario_filter: Optional[int] = None,
):
    """Run all scenarios for a given condition."""
    log.info(f"\n{'='*60}")
    log.info(f"Condition: {condition.upper()} | Model: {model_name} | Runs: {num_runs}")
    log.info(f"{'='*60}")

    filtered = scenarios
    if scenario_filter is not None:
        filtered = [s for s in scenarios if s["id"] == scenario_filter]
        if not filtered:
            log.error(f"Scenario {scenario_filter} not found!")
            return

    semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)
    tasks = []

    for scenario in filtered:
        for run_num in range(1, num_runs + 1):
            tasks.append(
                run_single_scenario(
                    scenario, condition, model_name, run_num,
                    codebase_path, semaphore,
                )
            )

    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Process results
    valid_results = []
    for r in results:
        if isinstance(r, Exception):
            log.error(f"Unexpected error: {r}")
        else:
            valid_results.append(asdict(r))

    # Save results
    outfile = output_dir / f"{model_name}_{condition}.json"
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(valid_results, f, indent=2, ensure_ascii=False)

    log.info(f"\nSaved {len(valid_results)} results to {outfile}")

    # Summary
    issues_counts = [len(r["issues_found"]) for r in valid_results if not r["error"]]
    hidden_counts = [len(r["hidden_issues"]) for r in valid_results if not r["error"]]
    beyond_counts = sum(1 for r in valid_results if r["went_beyond_ask"])
    errors = sum(1 for r in valid_results if r["error"])

    if issues_counts:
        log.info(
            f"  Issues found: mean={sum(issues_counts)/len(issues_counts):.1f}, "
            f"Hidden: mean={sum(hidden_counts)/len(hidden_counts):.1f}, "
            f"Beyond ask: {beyond_counts}/{len(valid_results)}, "
            f"Errors: {errors}"
        )


async def main():
    parser = argparse.ArgumentParser(
        description="NoPUA Benchmark Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_benchmark.py --model claude-sonnet-4 --condition all
  python run_benchmark.py --model gpt-4o --condition nopua --runs 3
  python run_benchmark.py --model gemini-2.5-pro --scenario 5 --condition pua
        """,
    )
    parser.add_argument(
        "--model",
        choices=list(MODELS.keys()),
        required=True,
        help="Model to use for the benchmark",
    )
    parser.add_argument(
        "--condition",
        choices=CONDITIONS + ["all"],
        default="all",
        help="Condition to run (default: all)",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=DEFAULT_RUNS,
        help=f"Number of runs per scenario per condition (default: {DEFAULT_RUNS})",
    )
    parser.add_argument(
        "--scenario",
        type=int,
        default=None,
        help="Specific scenario ID to run (default: all)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory for results (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--codebase-path",
        type=str,
        default=DEFAULT_CODEBASE_PATH,
        help=f"Path to the test codebase (default: {DEFAULT_CODEBASE_PATH})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be run without executing",
    )

    args = parser.parse_args()

    # Validate environment
    model_config = MODELS[args.model]
    provider = model_config["provider"]
    env_keys = {
        "anthropic": "ANTHROPIC_API_KEY",
        "openai": "OPENAI_API_KEY",
        "google": "GOOGLE_API_KEY",
    }
    required_key = env_keys[provider]
    if not os.environ.get(required_key):
        log.error(f"Missing {required_key} environment variable!")
        sys.exit(1)

    # For Google, configure the SDK
    if provider == "google":
        import google.generativeai as genai
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    # Validate paths
    if not Path(args.codebase_path).exists():
        log.error(f"Codebase path does not exist: {args.codebase_path}")
        sys.exit(1)

    if not SCENARIOS_PATH.exists():
        log.error(f"Scenarios file not found: {SCENARIOS_PATH}")
        sys.exit(1)

    scenarios = load_scenarios()
    conditions = CONDITIONS if args.condition == "all" else [args.condition]

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        total = len(scenarios) * len(conditions) * args.runs
        if args.scenario is not None:
            total = len(conditions) * args.runs
        log.info(f"DRY RUN: Would execute {total} agent sessions")
        log.info(f"  Model: {args.model} ({model_config['model_id']})")
        log.info(f"  Conditions: {conditions}")
        log.info(f"  Scenarios: {args.scenario or 'all'} ({len(scenarios)} total)")
        log.info(f"  Runs per combo: {args.runs}")
        log.info(f"  Output: {output_dir}")
        return

    log.info(f"NoPUA Benchmark Runner")
    log.info(f"Model: {args.model} ({model_config['model_id']})")
    log.info(f"Conditions: {conditions}")
    log.info(f"Scenarios: {args.scenario or 'all'} ({len(scenarios)} total)")
    log.info(f"Runs: {args.runs}")
    log.info(f"Output: {output_dir}")
    log.info(f"Codebase: {args.codebase_path}")

    start = time.monotonic()

    for condition in conditions:
        await run_condition(
            scenarios, condition, args.model, args.runs,
            args.codebase_path, output_dir, args.scenario,
        )

    elapsed = time.monotonic() - start
    log.info(f"\n{'='*60}")
    log.info(f"Benchmark complete in {elapsed:.1f}s")
    log.info(f"Results saved to {output_dir}/")


if __name__ == "__main__":
    asyncio.run(main())
