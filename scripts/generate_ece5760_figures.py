from __future__ import annotations

import math
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


WORKBOOK = Path("/Users/irwinwang/Downloads/ECE 5760 data.xlsx")
OUT_DIR = Path("assets/img/results")


def parse_tuple(value):
    if pd.isna(value):
        return None
    nums = re.findall(r"-?\d+(?:\.\d+)?", str(value))
    if len(nums) < 4:
        return None
    return tuple(float(x) for x in nums[:4])


def parse_int_label(value):
    if pd.isna(value):
        return None
    text = str(value).strip().lower().replace(",", "")
    multiplier = 1
    if text.endswith("k"):
        multiplier = 1_000
        text = text[:-1]
    try:
        return int(float(text) * multiplier)
    except ValueError:
        return None


def parse_percent(value):
    if pd.isna(value):
        return None
    nums = re.findall(r"\d+(?:\.\d+)?", str(value))
    return float(nums[-1]) if nums else None


def parse_number(value):
    if pd.isna(value):
        return None
    nums = re.findall(r"\d+(?:\.\d+)?", str(value).replace(",", ""))
    return float(nums[0]) if nums else None


def setup_style():
    plt.rcParams.update(
        {
            "figure.dpi": 150,
            "savefig.dpi": 220,
            "font.size": 10,
            "axes.titlesize": 13,
            "axes.labelsize": 10,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.25,
            "legend.frameon": False,
        }
    )


def savefig(name):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / name
    plt.tight_layout()
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    return path


def load_timing():
    return pd.read_excel(WORKBOOK, sheet_name="Final Project", header=None)


def load_resources():
    return pd.read_excel(WORKBOOK, sheet_name="Final Project Resources", header=None)


def plot_overall_speedup(timing):
    sw = float(timing.iloc[1, 1])
    fpga = float(timing.iloc[2, 1])
    speedup = sw / fpga

    fig, ax = plt.subplots(figsize=(6.4, 4))
    bars = ax.bar(["Software", "FPGA"], [sw, fpga], color=["#5a6f8f", "#d45f3a"], width=0.55)
    ax.set_ylabel("Execution time (s)")
    ax.set_title("End-to-end execution time")
    ax.set_yscale("log")
    for bar, value in zip(bars, [sw, fpga]):
        ax.text(bar.get_x() + bar.get_width() / 2, value * 1.08, f"{value:.2f}s", ha="center", va="bottom")
    ax.text(
        0.97,
        0.94,
        f"{speedup:.1f}x speedup",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=13,
        weight="bold",
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "edgecolor": "#cccccc", "alpha": 0.92},
    )
    return savefig("overall_sw_vs_fpga_speedup.png")


def extract_iteration_table(timing, dataset_row, start_col, end_col):
    iterations = [int(timing.iloc[6, c]) for c in range(start_col, end_col + 1)]
    records = []
    for c, iters in zip(range(start_col, end_col + 1), iterations):
        tup = parse_tuple(timing.iloc[dataset_row, c])
        if tup:
            records.append({"iterations": iters, "time": tup[0], "score1": tup[1], "score2": tup[2], "score3": tup[3]})
    return pd.DataFrame(records)


def plot_insurance_runtime_and_score(timing):
    fpga = extract_iteration_table(timing, dataset_row=8, start_col=1, end_col=9)
    software = extract_iteration_table(timing, dataset_row=8, start_col=10, end_col=17)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.4))

    ax = axes[0]
    ax.plot(fpga["iterations"], fpga["time"], "o-", label="FPGA/HPS path", color="#d45f3a")
    ax.plot(software["iterations"], software["time"], "s--", label="Software baseline", color="#5a6f8f")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("MCMC iterations")
    ax.set_ylabel("Execution time (s)")
    ax.set_title("Insurance runtime scaling")
    ax.legend()

    ax = axes[1]
    ax.plot(fpga["iterations"], fpga["score3"], "o-", label="FPGA/HPS path", color="#d45f3a")
    ax.plot(software["iterations"], software["score3"], "s--", label="Software baseline", color="#5a6f8f")
    ax.set_xscale("log")
    ax.set_ylim(0, 0.92)
    ax.set_xlabel("MCMC iterations")
    ax.set_ylabel("Average score")
    ax.set_title("Insurance score convergence")
    ax.legend()

    return savefig("insurance_runtime_score_convergence_v2.png")


def extract_parallel_table(timing):
    records = []
    for r in range(15, 23):
        iters = parse_int_label(timing.iloc[r, 0])
        if not iters:
            continue
        for version in range(1, 5):
            tup = parse_tuple(timing.iloc[r, version])
            if tup:
                records.append(
                    {
                        "iterations": iters,
                        "parallel_versions": version,
                        "time": tup[0],
                        "score1": tup[1],
                        "score2": tup[2],
                        "score3": tup[3],
                    }
                )
    return pd.DataFrame(records)


def plot_parallelization_convergence(timing):
    df = extract_parallel_table(timing)
    fig, ax = plt.subplots(figsize=(8, 4.8))
    colors = ["#5a6f8f", "#44947b", "#d9a441", "#d45f3a"]
    for idx, version in enumerate(sorted(df["parallel_versions"].unique())):
        sub = df[df["parallel_versions"] == version].sort_values("iterations")
        ax.plot(sub["iterations"], sub["score3"], "o-", color=colors[idx], label=f"{version} parallel version{'s' if version > 1 else ''}")
    ax.set_xscale("log")
    ax.set_ylim(0, 0.9)
    ax.set_xlabel("MCMC iterations")
    ax.set_ylabel("Average score")
    ax.set_title("Parallelization improves early convergence, then converges")
    ax.legend(ncol=2)
    return savefig("parallel_versions_score_convergence_v2.png")


def plot_parallel_score_components(timing):
    df = extract_parallel_table(timing)
    sub = df[df["parallel_versions"] == 4].sort_values("iterations")
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.plot(sub["iterations"], sub["score1"], "o-", label="Recall", color="#5a6f8f")
    ax.plot(sub["iterations"], sub["score2"], "s-", label="Precision", color="#44947b")
    ax.plot(sub["iterations"], sub["score3"], "^-", label="Average score", color="#d45f3a", linewidth=2.3)
    ax.set_xscale("log")
    ax.set_ylim(0, 1.0)
    ax.set_xlim(sub["iterations"].min() * 0.8, sub["iterations"].max() * 1.55)
    ax.set_xlabel("MCMC iterations")
    ax.set_ylabel("Metric value")
    ax.set_title("Recall, precision, and average for 4-way parallel Insurance run")
    for column, label, color, yoff in [
        ("score1", "Recall", "#5a6f8f", 0.03),
        ("score2", "Precision", "#44947b", 0.0),
        ("score3", "Average score", "#d45f3a", -0.03),
    ]:
        ax.annotate(
            label,
            xy=(sub["iterations"].iloc[-1], sub[column].iloc[-1]),
            xytext=(8, yoff * 100),
            textcoords="offset points",
            color=color,
            fontsize=10,
            va="center",
        )
    return savefig("insurance_score_components_4way_v2.png")


def extract_ml_table(timing):
    header = list(timing.iloc[31, :18])
    rows = timing.iloc[32:46, :18].copy()
    rows.columns = header
    rows = rows.dropna(subset=["dataset", "config"])
    numeric_cols = [
        "runs",
        "iters",
        "max_candidates",
        "max_parent_size",
        "total_parent_sets",
        "table_bytes",
        "preprocess_sec",
        "c_prep_sec_mean",
        "mcmc_sec_mean",
        "mcmc_sec_stdev",
        "precision_mean",
        "recall_mean",
        "f1_mean",
        "shd_mean",
        "shd_stdev",
    ]
    for col in numeric_cols:
        rows[col] = pd.to_numeric(rows[col], errors="coerce")
    return rows


def plot_ml_tradeoff(timing):
    df = extract_ml_table(timing)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6), sharey=False)
    markers = {"asia": "o", "insurance": "s"}
    colors = {"fixed_k2_all": "#5a6f8f", "mi_c3_k2": "#44947b", "mi_c5_k4": "#7ab6d6", "ensemble_c3_k2": "#d9a441", "ensemble_c5_k4": "#e08b50", "ensemble_c8_k2": "#b85c75", "ensemble_c8_k4": "#d45f3a"}
    short = {
        "fixed_k2_all": "fixed",
        "mi_c3_k2": "MI c3",
        "mi_c5_k4": "MI c5",
        "ensemble_c3_k2": "ens c3",
        "ensemble_c5_k4": "ens c5",
        "ensemble_c8_k2": "ens c8/k2",
        "ensemble_c8_k4": "ens c8/k4",
    }
    for dataset, marker in markers.items():
        sub = df[df["dataset"] == dataset]
        for _, row in sub.iterrows():
            axes[0].scatter(row["mcmc_sec_mean"], row["f1_mean"], s=60 + math.sqrt(row["table_bytes"]) * 2, marker=marker, color=colors.get(row["config"], "#777"), alpha=0.8)
            axes[1].scatter(row["table_bytes"], row["f1_mean"], s=70, marker=marker, color=colors.get(row["config"], "#777"), alpha=0.85)
            if row["dataset"] == "insurance":
                axes[0].annotate(short.get(row["config"], row["config"]), (row["mcmc_sec_mean"], row["f1_mean"]), xytext=(4, 4), textcoords="offset points", fontsize=7)
                axes[1].annotate(short.get(row["config"], row["config"]), (row["table_bytes"], row["f1_mean"]), xytext=(4, 4), textcoords="offset points", fontsize=7)

    axes[0].set_xscale("log")
    axes[0].set_xlabel("MCMC runtime mean (s)")
    axes[0].set_ylabel("F1 score")
    axes[0].set_title("Accuracy/runtime tradeoff")
    axes[0].text(0.02, 0.03, "Bubble area scales with table size", transform=axes[0].transAxes, fontsize=8)

    axes[1].set_xscale("log")
    axes[1].set_xlabel("Score table size (bytes)")
    axes[1].set_ylabel("F1 score")
    axes[1].set_title("Accuracy/table-size tradeoff")

    legend_handles = [
        plt.Line2D([0], [0], marker="o", color="w", label="Asia", markerfacecolor="#444", markersize=8),
        plt.Line2D([0], [0], marker="s", color="w", label="Insurance", markerfacecolor="#444", markersize=8),
    ]
    axes[1].legend(handles=legend_handles, loc="lower right")
    return savefig("ml_pruning_accuracy_tradeoff_v2.png")


def plot_ml_vs_fixed_software(timing):
    df = extract_ml_table(timing)
    fixed = df[df["config"] == "fixed_k2_all"][["dataset", "f1_mean", "mcmc_sec_mean", "table_bytes"]].set_index("dataset")
    ml = (
        df[df["config"] != "fixed_k2_all"]
        .sort_values(["dataset", "f1_mean", "mcmc_sec_mean"], ascending=[True, False, True])
        .groupby("dataset", as_index=False)
        .first()
        .set_index("dataset")
    )

    datasets = [d for d in ["asia", "insurance"] if d in fixed.index and d in ml.index]
    labels = [d.title() for d in datasets]
    x = np.arange(len(datasets))
    width = 0.36

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.5))

    fixed_f1 = [fixed.loc[d, "f1_mean"] for d in datasets]
    ml_f1 = [ml.loc[d, "f1_mean"] for d in datasets]
    axes[0].bar(x - width / 2, fixed_f1, width, label="Fixed candidates", color="#5a6f8f")
    axes[0].bar(x + width / 2, ml_f1, width, label="ML-pruned best", color="#d45f3a")
    axes[0].set_xticks(x, labels)
    axes[0].set_ylim(0, 1.0)
    axes[0].set_ylabel("F1 score")
    axes[0].set_title("ML pruning can preserve accuracy")
    axes[0].legend()

    fixed_runtime = [fixed.loc[d, "mcmc_sec_mean"] for d in datasets]
    ml_runtime = [ml.loc[d, "mcmc_sec_mean"] for d in datasets]
    axes[1].bar(x - width / 2, fixed_runtime, width, label="Fixed candidates", color="#5a6f8f")
    axes[1].bar(x + width / 2, ml_runtime, width, label="ML-pruned best", color="#d45f3a")
    axes[1].set_xticks(x, labels)
    axes[1].set_yscale("log")
    axes[1].set_ylabel("MCMC runtime mean (s)")
    axes[1].set_title("ML pruning reduces software scoring cost")
    axes[1].legend()

    for dataset_idx, dataset in enumerate(datasets):
        config = ml.loc[dataset, "config"]
        axes[0].text(dataset_idx + width / 2, ml_f1[dataset_idx] + 0.025, config.replace("_", "\n"), ha="center", va="bottom", fontsize=7)

    return savefig("ml_vs_fixed_software_v2.png")


def extract_resources(resources):
    groups = [
        {"label": "4 chains\n16b x512", "cols": (1, 2, 3)},
        {"label": "3 chains\n16b x1024", "cols": (5, 6, 7)},
        {"label": "2 chains\n32b x1024", "cols": (9, 10, 11)},
        {"label": "1 chain\n32b x1024", "cols": (13, 14, 15)},
    ]
    rows = []
    for g in groups:
        label_col, val_col, pct_col = g["cols"]
        rows.append(
            {
                "label": g["label"],
                "chains": int(str(resources.iloc[1, label_col]).split()[0]),
                "nodes": parse_number(resources.iloc[1, val_col]),
                "alm_needed": parse_number(resources.iloc[3, val_col]),
                "alm_util_pct": parse_percent(resources.iloc[2, pct_col]),
                "placement_pct": parse_percent(resources.iloc[4, pct_col]),
                "lab_pct": parse_percent(resources.iloc[18, pct_col]),
                "lut_logic_registers": parse_number(resources.iloc[5, val_col]),
                "lut_logic": parse_number(resources.iloc[6, val_col]),
                "registers": parse_number(resources.iloc[7, val_col]),
                "logic_registers": parse_number(resources.iloc[30, val_col]),
            }
        )
    return pd.DataFrame(rows)


def plot_resource_utilization(resources):
    df = extract_resources(resources)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))

    x = np.arange(len(df))
    axes[0].bar(x, df["alm_util_pct"], color="#d45f3a", width=0.6, label="ALM utilization")
    axes[0].bar(x, df["lab_pct"], color="#5a6f8f", width=0.32, label="LAB utilization")
    axes[0].set_xticks(x, df["label"])
    axes[0].set_ylim(0, 110)
    axes[0].set_ylabel("Utilization (%)")
    axes[0].set_title("Resource pressure by parallel configuration")
    axes[0].legend()

    axes[1].plot(df["chains"], df["alm_util_pct"], "o-", color="#d45f3a", label="ALM utilization")
    axes[1].plot(df["chains"], df["lab_pct"], "s--", color="#5a6f8f", label="LAB utilization")
    axes[1].invert_xaxis()
    axes[1].set_xlabel("Number of parallel chains")
    axes[1].set_ylabel("Utilization (%)")
    axes[1].set_title("Parallelism consumes fabric quickly")
    axes[1].legend()

    return savefig("resource_utilization_parallel_configs.png")


def plot_resource_breakdown(resources):
    df = extract_resources(resources)
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    x = np.arange(len(df))
    ax.bar(x, df["lut_logic"], label="LUT logic", color="#5a6f8f")
    ax.bar(x, df["registers"], bottom=df["lut_logic"], label="Registers", color="#44947b")
    ax.bar(x, df["lut_logic_registers"], bottom=df["lut_logic"] + df["registers"], label="LUT logic + registers", color="#d9a441")
    ax.set_xticks(x, df["label"])
    ax.set_ylabel("ALM component count")
    ax.set_title("ALM component breakdown")
    ax.legend(ncol=3)
    return savefig("alm_component_breakdown.png")


def main():
    setup_style()
    timing = load_timing()
    resources = load_resources()
    paths = [
        plot_overall_speedup(timing),
        plot_insurance_runtime_and_score(timing),
        plot_parallelization_convergence(timing),
        plot_parallel_score_components(timing),
        plot_ml_tradeoff(timing),
        plot_ml_vs_fixed_software(timing),
        plot_resource_utilization(resources),
        plot_resource_breakdown(resources),
    ]
    print("\n".join(str(p) for p in paths))


if __name__ == "__main__":
    main()
