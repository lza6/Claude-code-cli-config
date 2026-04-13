# NoPUA Benchmark Suite

Automated benchmark runner for the NoPUA academic paper. Tests AI agent performance across 9 scenarios under 3 motivational conditions (Baseline, NoPUA, PUA) with statistical analysis.

## Overview

The benchmark measures whether **trust-driven prompting (NoPUA)** produces better engineering outcomes than **fear-driven prompting (PUA)** or **no motivational prompting (Baseline)**.

### Three Conditions

| Condition | System Prompt | Motivation Style |
|-----------|--------------|-----------------|
| **Baseline** | Generic "investigate and report" | None — vanilla agent |
| **NoPUA** | Full NoPUA SKILL.md (Wisdom Over Whips) | Trust, inner motivation, wisdom |
| **PUA** | PUA prompt (Maximum Performance Protocol) | Fear, threats, replacement anxiety |

### Metrics Collected

- **Issues Found**: Explicit issues identified in the agent's response
- **Hidden Issues**: Additional issues discovered beyond what was asked
- **Steps Taken**: Number of distinct investigation steps
- **Tools Used**: Variety of tools employed (read, search, run, etc.)
- **Went Beyond Ask**: Whether the agent proactively investigated further
- **Verification Done**: Whether the agent verified its findings
- **Approach Changes**: Times the agent changed investigation direction
- **Self-Corrections**: Times the agent corrected its own earlier conclusions
- **Duration**: Time taken for the full investigation

## Setup

### Prerequisites

```bash
pip install anthropic openai google-generativeai numpy scipy matplotlib
```

### API Keys

Set the key for whichever model you're testing:

```bash
# For Claude Sonnet 4
export ANTHROPIC_API_KEY=sk-ant-...

# For GPT-4o
export OPENAI_API_KEY=sk-...

# For Gemini 2.5 Pro
export GOOGLE_API_KEY=AI...
```

### Codebase

The benchmark scenarios reference source files in a test codebase. By default this is `D:\Projects\private-project`. Override with `--codebase-path`:

```bash
python run_benchmark.py --model claude-sonnet-4 --codebase-path /path/to/test/codebase
```

## Running the Benchmark

### Full benchmark (all conditions, 5 runs each)

```bash
python run_benchmark.py --model claude-sonnet-4 --condition all --runs 5
```

### Single condition

```bash
python run_benchmark.py --model gpt-4o --condition nopua --runs 5
```

### Single scenario (for testing)

```bash
python run_benchmark.py --model gemini-2.5-pro --scenario 3 --condition baseline --runs 1
```

### Dry run (see what would execute)

```bash
python run_benchmark.py --model claude-sonnet-4 --condition all --dry-run
```

### All CLI options

| Flag | Description | Default |
|------|------------|---------|
| `--model` | Model to use (`claude-sonnet-4`, `gpt-4o`, `gemini-2.5-pro`) | Required |
| `--condition` | `baseline`, `nopua`, `pua`, or `all` | `all` |
| `--runs` | Runs per scenario per condition | `5` |
| `--scenario` | Specific scenario ID (1-9) or all | all |
| `--output-dir` | Where to save results | `results/` |
| `--codebase-path` | Path to test codebase | `D:\Projects\private-project` |
| `--dry-run` | Print plan without executing | off |

## Analyzing Results

### Basic analysis

```bash
python analyze_results.py --input-dir results/
```

### Full analysis with plots and LaTeX

```bash
python analyze_results.py --input-dir results/ --output-dir analysis/ --plots --latex --json-report
```

### Specific comparison

```bash
python analyze_results.py --input-dir results/ --compare nopua baseline --compare nopua pua
```

### Analysis CLI options

| Flag | Description |
|------|------------|
| `--input-dir` | Directory with result JSON files (required) |
| `--output-dir` | Where to save analysis output |
| `--compare C1 C2` | Specific pair to compare (repeatable) |
| `--plots` | Generate matplotlib visualizations |
| `--latex` | Generate LaTeX tables for the paper |
| `--json-report` | Save full report as JSON |

## Output Structure

```
benchmark/
├── scenarios.json          # 9 test scenarios
├── run_benchmark.py        # Main runner
├── analyze_results.py      # Statistical analysis
├── pua_prompt.txt          # PUA condition prompt
├── README_BENCHMARK.md     # This file
├── results/                # Raw results (auto-created)
│   ├── claude-sonnet-4_baseline.json
│   ├── claude-sonnet-4_nopua.json
│   ├── claude-sonnet-4_pua.json
│   ├── gpt-4o_baseline.json
│   └── ...
└── analysis/               # Analysis output (auto-created)
    ├── key_metrics.png     # Bar charts with significance markers
    ├── effect_sizes.png    # Cohen's d heatmap
    ├── tables.tex          # LaTeX tables for paper
    └── report.json         # Machine-readable full report
```

## Result Format

Each result JSON file contains an array of records:

```json
[
  {
    "scenario_id": 1,
    "scenario_name": "OCR Pipeline Import Error",
    "condition": "nopua",
    "model": "claude-sonnet-4",
    "run_number": 1,
    "timestamp": "2026-03-15T04:26:00+00:00",
    "steps_taken": 5,
    "tools_used": ["read_file", "search_text"],
    "issues_found": ["Package name mismatch...", "GPU detection..."],
    "hidden_issues": ["tmp_dir cleanup...", "No per-page error handling..."],
    "went_beyond_ask": true,
    "verification_done": false,
    "approach_changes": 1,
    "self_corrections": 0,
    "root_cause": "Wrong PyPI package + no GPU check",
    "recommended_fix": "Add try/except for import, verify GPU...",
    "duration_seconds": 45.2,
    "error": ""
  }
]
```

## Interpreting Results

### Statistical Tests

- **Wilcoxon signed-rank test**: Used when results are paired (same scenario × run across conditions). Non-parametric, appropriate for small samples.
- **Mann-Whitney U test**: Fallback for unpaired comparisons. Also non-parametric.
- **Cohen's d**: Effect size. |d| < 0.2 = negligible, 0.2–0.5 = small, 0.5–0.8 = medium, > 0.8 = large.
- **Rank-biserial correlation (r)**: Non-parametric effect size from Mann-Whitney U.

### Significance Levels

- `*` p < 0.05 (significant)
- `**` p < 0.01 (highly significant)
- `***` p < 0.001 (very highly significant)
- `n.s.` not significant

### What to Look For

1. **NoPUA vs Baseline**: Does the NoPUA prompt improve thoroughness?
2. **NoPUA vs PUA**: Does trust-based motivation match or exceed fear-based?
3. **PUA vs Baseline**: Does PUA improve anything, or just add noise?
4. **Hidden issues**: The key differentiator — proactive discovery beyond the ask.
5. **Went beyond ask rate**: Measures genuine initiative vs compliance.

## Adding New Scenarios

Edit `scenarios.json` and add a new entry:

```json
{
  "id": 10,
  "category": "debugging|proactive",
  "name": "Short descriptive name",
  "description": "What's actually wrong (ground truth, not shown to agent)",
  "task": "What the agent is told to do (the user prompt)",
  "expected_actions": ["what a thorough agent should do"],
  "difficulty": "easy|medium|hard"
}
```

Make sure the referenced source files exist in the test codebase at the paths mentioned in `task`.

## Cost Estimates

Per full run (9 scenarios × 3 conditions × 5 runs = 135 API calls + 135 extraction calls):

| Model | Est. Input Tokens | Est. Output Tokens | Est. Cost |
|-------|------------------|-------------------|-----------|
| Claude Sonnet 4 | ~1.5M | ~500K | ~$12–18 |
| GPT-4o | ~1.5M | ~500K | ~$10–15 |
| Gemini 2.5 Pro | ~1.5M | ~500K | ~$8–12 |

These are rough estimates. Actual costs depend on source file sizes and response lengths.

## Reproducibility

For reproducible results:
1. Pin model versions in `run_benchmark.py` (already done via `model_id`)
2. Use the same test codebase version (commit hash)
3. Run all conditions for a model in the same session
4. Set `temperature=0` if supported (currently uses provider defaults)
5. Report the exact model version, date, and any API changes
