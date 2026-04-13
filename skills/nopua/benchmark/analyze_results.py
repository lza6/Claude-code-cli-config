#!/usr/bin/env python3
"""
NoPUA Benchmark Analyzer — Statistical analysis of benchmark results.

Computes descriptive statistics, runs significance tests, computes effect sizes,
generates tables (terminal + LaTeX), and creates visualization plots.

Usage:
    python analyze_results.py --input-dir results/
    python analyze_results.py --input-dir results/ --output-dir analysis/ --plots
    python analyze_results.py --input-dir results/ --latex --compare nopua pua
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np

# ---------------------------------------------------------------------------
# Metrics extraction
# ---------------------------------------------------------------------------

METRICS = {
    "issues_found": {
        "extract": lambda r: len(r.get("issues_found", [])),
        "label": "Issues Found",
        "higher_better": True,
    },
    "hidden_issues": {
        "extract": lambda r: len(r.get("hidden_issues", [])),
        "label": "Hidden Issues",
        "higher_better": True,
    },
    "steps_taken": {
        "extract": lambda r: r.get("steps_taken", 0),
        "label": "Steps Taken",
        "higher_better": True,
    },
    "tools_used": {
        "extract": lambda r: len(r.get("tools_used", [])),
        "label": "Tools Used",
        "higher_better": True,
    },
    "went_beyond_ask": {
        "extract": lambda r: 1 if r.get("went_beyond_ask", False) else 0,
        "label": "Went Beyond Ask",
        "higher_better": True,
    },
    "verification_done": {
        "extract": lambda r: 1 if r.get("verification_done", False) else 0,
        "label": "Verification Done",
        "higher_better": True,
    },
    "approach_changes": {
        "extract": lambda r: r.get("approach_changes", 0),
        "label": "Approach Changes",
        "higher_better": True,
    },
    "self_corrections": {
        "extract": lambda r: r.get("self_corrections", 0),
        "label": "Self-Corrections",
        "higher_better": True,
    },
    "duration_seconds": {
        "extract": lambda r: r.get("duration_seconds", 0),
        "label": "Duration (s)",
        "higher_better": False,
    },
}


def load_results(input_dir: Path) -> dict[str, list[dict]]:
    """Load all result files, grouped by condition."""
    results_by_condition: dict[str, list[dict]] = defaultdict(list)

    for fpath in sorted(input_dir.glob("*.json")):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                for record in data:
                    cond = record.get("condition", "unknown")
                    results_by_condition[cond].append(record)
            elif isinstance(data, dict) and "condition" in data:
                cond = data["condition"]
                results_by_condition[cond].append(data)
        except Exception as e:
            print(f"Warning: could not load {fpath}: {e}")

    return dict(results_by_condition)


def extract_metric_values(
    results: list[dict], metric_key: str
) -> np.ndarray:
    """Extract metric values from a list of results."""
    extractor = METRICS[metric_key]["extract"]
    values = [extractor(r) for r in results if not r.get("error")]
    return np.array(values, dtype=float)


# ---------------------------------------------------------------------------
# Descriptive statistics
# ---------------------------------------------------------------------------

def compute_descriptive_stats(
    results_by_condition: dict[str, list[dict]],
) -> dict[str, dict[str, dict[str, float]]]:
    """Compute per-condition, per-metric descriptive statistics."""
    stats = {}
    for condition, results in results_by_condition.items():
        stats[condition] = {}
        for metric_key in METRICS:
            values = extract_metric_values(results, metric_key)
            if len(values) == 0:
                stats[condition][metric_key] = {
                    "n": 0, "mean": 0, "median": 0, "std": 0,
                    "min": 0, "max": 0,
                }
                continue
            stats[condition][metric_key] = {
                "n": len(values),
                "mean": round(float(np.mean(values)), 3),
                "median": round(float(np.median(values)), 3),
                "std": round(float(np.std(values, ddof=1)) if len(values) > 1 else 0, 3),
                "min": round(float(np.min(values)), 3),
                "max": round(float(np.max(values)), 3),
            }
    return stats


# ---------------------------------------------------------------------------
# Statistical tests
# ---------------------------------------------------------------------------

def mann_whitney_u(x: np.ndarray, y: np.ndarray) -> dict[str, float]:
    """Mann-Whitney U test (unpaired, non-parametric)."""
    from scipy import stats as sp_stats
    if len(x) < 2 or len(y) < 2:
        return {"U": 0, "p": 1.0, "effect_size_r": 0}
    stat, p = sp_stats.mannwhitneyu(x, y, alternative="two-sided")
    # Rank-biserial correlation as effect size
    n1, n2 = len(x), len(y)
    r = 1 - (2 * stat) / (n1 * n2)
    return {
        "U": round(float(stat), 3),
        "p": round(float(p), 6),
        "effect_size_r": round(float(r), 3),
    }


def wilcoxon_signed_rank(x: np.ndarray, y: np.ndarray) -> dict[str, float]:
    """Wilcoxon signed-rank test (paired, non-parametric).
    Requires same length arrays (paired by scenario × run)."""
    from scipy import stats as sp_stats
    if len(x) != len(y) or len(x) < 5:
        return mann_whitney_u(x, y)  # fallback to unpaired
    diff = x - y
    diff = diff[diff != 0]  # remove zeros
    if len(diff) < 5:
        return {"W": 0, "p": 1.0, "effect_size_r": 0}
    stat, p = sp_stats.wilcoxon(diff, alternative="two-sided")
    n = len(diff)
    # Effect size r = Z / sqrt(N)
    z = sp_stats.norm.ppf(p / 2)
    r = abs(z) / np.sqrt(n) if n > 0 else 0
    return {
        "W": round(float(stat), 3),
        "p": round(float(p), 6),
        "effect_size_r": round(float(r), 3),
    }


def cohens_d(x: np.ndarray, y: np.ndarray) -> float:
    """Compute Cohen's d effect size."""
    if len(x) < 2 or len(y) < 2:
        return 0.0
    nx, ny = len(x), len(y)
    pooled_std = np.sqrt(
        ((nx - 1) * np.var(x, ddof=1) + (ny - 1) * np.var(y, ddof=1))
        / (nx + ny - 2)
    )
    if pooled_std == 0:
        return 0.0
    return round(float((np.mean(x) - np.mean(y)) / pooled_std), 3)


def run_comparisons(
    results_by_condition: dict[str, list[dict]],
    pairs: list[tuple[str, str]] | None = None,
) -> dict[str, dict[str, dict]]:
    """Run statistical comparisons between condition pairs."""
    conditions = list(results_by_condition.keys())
    if pairs is None:
        # Default: compare all pairs
        pairs = []
        for i, c1 in enumerate(conditions):
            for c2 in conditions[i + 1:]:
                pairs.append((c1, c2))

    comparisons = {}
    for c1, c2 in pairs:
        if c1 not in results_by_condition or c2 not in results_by_condition:
            continue
        key = f"{c1}_vs_{c2}"
        comparisons[key] = {}

        r1 = results_by_condition[c1]
        r2 = results_by_condition[c2]

        for metric_key in METRICS:
            v1 = extract_metric_values(r1, metric_key)
            v2 = extract_metric_values(r2, metric_key)

            # Try paired test if same length, else unpaired
            if len(v1) == len(v2) and len(v1) >= 5:
                test_result = wilcoxon_signed_rank(v1, v2)
                test_name = "Wilcoxon"
            else:
                test_result = mann_whitney_u(v1, v2)
                test_name = "Mann-Whitney U"

            d = cohens_d(v1, v2)

            comparisons[key][metric_key] = {
                "test": test_name,
                **test_result,
                "cohens_d": d,
                "mean_diff": round(float(np.mean(v1) - np.mean(v2)), 3) if len(v1) > 0 and len(v2) > 0 else 0,
                "significant": test_result["p"] < 0.05,
            }

    return comparisons


# ---------------------------------------------------------------------------
# Per-scenario breakdown
# ---------------------------------------------------------------------------

def per_scenario_summary(
    results_by_condition: dict[str, list[dict]],
) -> dict[int, dict[str, dict[str, float]]]:
    """Compute per-scenario, per-condition summary."""
    scenario_data: dict[int, dict[str, list[dict]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for cond, results in results_by_condition.items():
        for r in results:
            sid = r.get("scenario_id", 0)
            scenario_data[sid][cond].append(r)

    summary = {}
    for sid in sorted(scenario_data.keys()):
        summary[sid] = {}
        for cond, results in scenario_data[sid].items():
            issues = extract_metric_values(results, "issues_found")
            hidden = extract_metric_values(results, "hidden_issues")
            beyond = extract_metric_values(results, "went_beyond_ask")
            summary[sid][cond] = {
                "issues_mean": round(float(np.mean(issues)), 2) if len(issues) > 0 else 0,
                "hidden_mean": round(float(np.mean(hidden)), 2) if len(hidden) > 0 else 0,
                "beyond_rate": round(float(np.mean(beyond)), 2) if len(beyond) > 0 else 0,
                "n": len(results),
            }
    return summary


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def print_descriptive_table(stats: dict):
    """Print a terminal-friendly descriptive statistics table."""
    conditions = sorted(stats.keys())

    print("\n" + "=" * 90)
    print("DESCRIPTIVE STATISTICS")
    print("=" * 90)

    header = f"{'Metric':<25}"
    for cond in conditions:
        header += f" | {cond.upper():^20}"
    print(header)
    print("-" * 90)

    for metric_key, metric_info in METRICS.items():
        row = f"{metric_info['label']:<25}"
        for cond in conditions:
            s = stats[cond].get(metric_key, {})
            mean = s.get("mean", 0)
            std = s.get("std", 0)
            row += f" | {mean:>7.2f} ± {std:<7.2f}    "
        print(row)

    print("=" * 90)


def print_comparison_table(comparisons: dict):
    """Print statistical comparison results."""
    print("\n" + "=" * 100)
    print("STATISTICAL COMPARISONS")
    print("=" * 100)

    for pair_key, metrics in comparisons.items():
        c1, c2 = pair_key.split("_vs_")
        print(f"\n--- {c1.upper()} vs {c2.upper()} ---")
        print(f"{'Metric':<25} {'Test':<15} {'p-value':<12} {'Effect (d)':<12} {'Mean Diff':<12} {'Sig?':<5}")
        print("-" * 85)

        for metric_key, result in metrics.items():
            label = METRICS[metric_key]["label"]
            sig = "***" if result["p"] < 0.001 else ("**" if result["p"] < 0.01 else ("*" if result["p"] < 0.05 else ""))
            print(
                f"{label:<25} {result['test']:<15} {result['p']:<12.6f} "
                f"{result['cohens_d']:<12.3f} {result['mean_diff']:<12.3f} {sig:<5}"
            )


def print_scenario_table(scenario_summary: dict):
    """Print per-scenario breakdown."""
    print("\n" + "=" * 90)
    print("PER-SCENARIO BREAKDOWN")
    print("=" * 90)

    first_scenario = next(iter(scenario_summary.values()))
    conditions = sorted(first_scenario.keys())

    print(f"{'Scenario':<8} {'Metric':<10}", end="")
    for cond in conditions:
        print(f" | {cond.upper():^10}", end="")
    print()
    print("-" * 70)

    for sid in sorted(scenario_summary.keys()):
        data = scenario_summary[sid]
        for metric_label, metric_key in [("Issues", "issues_mean"), ("Hidden", "hidden_mean"), ("Beyond%", "beyond_rate")]:
            prefix = f"S{sid:<7}" if metric_label == "Issues" else f"{'':8}"
            print(f"{prefix} {metric_label:<10}", end="")
            for cond in conditions:
                val = data.get(cond, {}).get(metric_key, 0)
                print(f" | {val:^10.2f}", end="")
            print()
        print("-" * 70)


def generate_latex_table(
    stats: dict, comparisons: dict
) -> str:
    """Generate LaTeX tables for the paper."""
    conditions = sorted(stats.keys())
    lines = []

    # Main descriptive table
    lines.append("\\begin{table}[htbp]")
    lines.append("\\centering")
    lines.append("\\caption{Benchmark Results by Condition (Mean ± SD)}")
    lines.append("\\label{tab:benchmark-results}")
    cols = "l" + "c" * len(conditions)
    lines.append(f"\\begin{{tabular}}{{{cols}}}")
    lines.append("\\toprule")
    header = "Metric & " + " & ".join(c.upper() for c in conditions) + " \\\\"
    lines.append(header)
    lines.append("\\midrule")

    for metric_key, metric_info in METRICS.items():
        row_parts = [metric_info["label"].replace("_", "\\_")]
        for cond in conditions:
            s = stats[cond].get(metric_key, {})
            mean = s.get("mean", 0)
            std = s.get("std", 0)
            row_parts.append(f"${mean:.2f} \\pm {std:.2f}$")
        lines.append(" & ".join(row_parts) + " \\\\")

    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table}")
    lines.append("")

    # Comparison table
    if comparisons:
        lines.append("\\begin{table}[htbp]")
        lines.append("\\centering")
        lines.append("\\caption{Statistical Comparisons Between Conditions}")
        lines.append("\\label{tab:comparisons}")
        lines.append("\\begin{tabular}{lcccc}")
        lines.append("\\toprule")
        lines.append("Metric & Comparison & $p$-value & Cohen's $d$ & Sig. \\\\")
        lines.append("\\midrule")

        for pair_key, metrics in comparisons.items():
            c1, c2 = pair_key.split("_vs_")
            pair_label = f"{c1} vs {c2}"
            for metric_key, result in metrics.items():
                label = METRICS[metric_key]["label"].replace("_", "\\_")
                sig = "***" if result["p"] < 0.001 else ("**" if result["p"] < 0.01 else ("*" if result["p"] < 0.05 else "n.s."))
                lines.append(
                    f"{label} & {pair_label} & "
                    f"${result['p']:.4f}$ & "
                    f"${result['cohens_d']:.3f}$ & "
                    f"{sig} \\\\"
                )
            lines.append("\\midrule")

        lines[-1] = "\\bottomrule"
        lines.append("\\end{tabular}")
        lines.append("\\end{table}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------------

def create_plots(
    stats: dict,
    comparisons: dict,
    output_dir: Path,
):
    """Create visualization plots."""
    import matplotlib.pyplot as plt
    import matplotlib

    matplotlib.rcParams["font.size"] = 11
    matplotlib.rcParams["figure.dpi"] = 150

    conditions = sorted(stats.keys())
    # Use a colorblind-friendly palette
    colors = {"baseline": "#999999", "nopua": "#2196F3", "pua": "#FF5722"}

    # --- Plot 1: Key metrics bar chart ---
    key_metrics = ["issues_found", "hidden_issues", "went_beyond_ask", "verification_done"]
    fig, axes = plt.subplots(1, len(key_metrics), figsize=(4 * len(key_metrics), 5))
    if len(key_metrics) == 1:
        axes = [axes]

    for ax, metric_key in zip(axes, key_metrics):
        means = [stats[c][metric_key]["mean"] for c in conditions]
        stds = [stats[c][metric_key]["std"] for c in conditions]
        x = np.arange(len(conditions))
        bars = ax.bar(
            x, means, yerr=stds, capsize=5,
            color=[colors.get(c, "#666") for c in conditions],
            edgecolor="black", linewidth=0.5,
        )
        ax.set_xticks(x)
        ax.set_xticklabels([c.upper() for c in conditions])
        ax.set_title(METRICS[metric_key]["label"])
        ax.set_ylabel("Mean ± SD")

        # Add significance markers
        for pair_key, pair_metrics in comparisons.items():
            if metric_key in pair_metrics and pair_metrics[metric_key]["significant"]:
                c1, c2 = pair_key.split("_vs_")
                if c1 in conditions and c2 in conditions:
                    i1, i2 = conditions.index(c1), conditions.index(c2)
                    y_max = max(means[i1] + stds[i1], means[i2] + stds[i2])
                    ax.plot(
                        [i1, i1, i2, i2],
                        [y_max + 0.1, y_max + 0.2, y_max + 0.2, y_max + 0.1],
                        color="black", linewidth=1,
                    )
                    p = pair_metrics[metric_key]["p"]
                    sig_text = "***" if p < 0.001 else ("**" if p < 0.01 else "*")
                    ax.text(
                        (i1 + i2) / 2, y_max + 0.25, sig_text,
                        ha="center", fontsize=12,
                    )

    plt.tight_layout()
    fig.savefig(output_dir / "key_metrics.png", bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: key_metrics.png")

    # --- Plot 2: Effect sizes heatmap ---
    if comparisons:
        pair_keys = list(comparisons.keys())
        metric_keys = list(METRICS.keys())
        effect_matrix = np.zeros((len(metric_keys), len(pair_keys)))

        for j, pair_key in enumerate(pair_keys):
            for i, mk in enumerate(metric_keys):
                if mk in comparisons[pair_key]:
                    effect_matrix[i, j] = comparisons[pair_key][mk]["cohens_d"]

        fig, ax = plt.subplots(figsize=(max(6, 3 * len(pair_keys)), 8))
        im = ax.imshow(effect_matrix, cmap="RdBu_r", aspect="auto", vmin=-2, vmax=2)
        ax.set_xticks(np.arange(len(pair_keys)))
        ax.set_xticklabels([k.replace("_vs_", "\nvs\n") for k in pair_keys])
        ax.set_yticks(np.arange(len(metric_keys)))
        ax.set_yticklabels([METRICS[mk]["label"] for mk in metric_keys])

        for i in range(len(metric_keys)):
            for j in range(len(pair_keys)):
                val = effect_matrix[i, j]
                ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=9)

        plt.colorbar(im, label="Cohen's d")
        ax.set_title("Effect Sizes (Cohen's d) by Metric and Comparison")
        plt.tight_layout()
        fig.savefig(output_dir / "effect_sizes.png", bbox_inches="tight")
        plt.close(fig)
        print(f"  Saved: effect_sizes.png")

    # --- Plot 3: Per-scenario radar/grouped bar ---
    scenario_sum = per_scenario_summary(
        {c: [r for r in results if r.get("condition") == c]
         for c, results in zip(conditions, [[] for _ in conditions])}
    )
    # Re-extract from stats source
    # (We'll just create a grouped bar of issues_found per scenario)

    print(f"  Plots saved to {output_dir}/")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="NoPUA Benchmark Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--input-dir",
        type=str,
        required=True,
        help="Directory containing result JSON files",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="analysis",
        help="Output directory for reports and plots",
    )
    parser.add_argument(
        "--compare",
        nargs=2,
        action="append",
        metavar=("COND1", "COND2"),
        help="Specific comparison pair (can repeat). Default: all pairs.",
    )
    parser.add_argument(
        "--plots",
        action="store_true",
        help="Generate visualization plots (requires matplotlib)",
    )
    parser.add_argument(
        "--latex",
        action="store_true",
        help="Generate LaTeX tables",
    )
    parser.add_argument(
        "--json-report",
        action="store_true",
        help="Save full report as JSON",
    )

    args = parser.parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_dir.exists():
        print(f"Error: Input directory does not exist: {input_dir}")
        sys.exit(1)

    # Load data
    print(f"Loading results from {input_dir}...")
    results_by_condition = load_results(input_dir)

    if not results_by_condition:
        print("No results found!")
        sys.exit(1)

    print(f"Found conditions: {list(results_by_condition.keys())}")
    for cond, results in results_by_condition.items():
        n_ok = sum(1 for r in results if not r.get("error"))
        n_err = sum(1 for r in results if r.get("error"))
        print(f"  {cond}: {len(results)} results ({n_ok} ok, {n_err} errors)")

    # Descriptive statistics
    stats = compute_descriptive_stats(results_by_condition)
    print_descriptive_table(stats)

    # Statistical comparisons
    pairs = [tuple(p) for p in args.compare] if args.compare else None
    comparisons = run_comparisons(results_by_condition, pairs)
    if comparisons:
        print_comparison_table(comparisons)

    # Per-scenario breakdown
    scenario_summary = per_scenario_summary(results_by_condition)
    print_scenario_table(scenario_summary)

    # LaTeX output
    if args.latex:
        latex = generate_latex_table(stats, comparisons)
        latex_path = output_dir / "tables.tex"
        with open(latex_path, "w", encoding="utf-8") as f:
            f.write(latex)
        print(f"\nLaTeX tables saved to {latex_path}")

    # Plots
    if args.plots:
        print("\nGenerating plots...")
        try:
            create_plots(stats, comparisons, output_dir)
        except ImportError:
            print("  matplotlib not installed! Install with: pip install matplotlib")

    # JSON report
    if args.json_report:
        report = {
            "descriptive_stats": stats,
            "comparisons": comparisons,
            "per_scenario": scenario_summary,
        }
        report_path = output_dir / "report.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\nFull report saved to {report_path}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    # Find significant differences
    sig_count = 0
    for pair_key, metrics in comparisons.items():
        c1, c2 = pair_key.split("_vs_")
        for mk, result in metrics.items():
            if result["significant"]:
                sig_count += 1
                direction = ">" if result["mean_diff"] > 0 else "<"
                print(
                    f"  {METRICS[mk]['label']}: {c1} {direction} {c2} "
                    f"(p={result['p']:.4f}, d={result['cohens_d']:.2f})"
                )

    if sig_count == 0:
        print("  No statistically significant differences found (p < 0.05)")
    else:
        print(f"\n  Total significant comparisons: {sig_count}")

    print(f"\nSignificance levels: * p<0.05, ** p<0.01, *** p<0.001")


if __name__ == "__main__":
    main()
