"""System architecture diagram + scaling chart for the report."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results", "benchmark_results.json")

INK, ACC, SOFT, OK, GREY = "#1b1f3b", "#4f46e5", "#eceafd", "#16a34a", "#6b7089"


def box(ax, x, y, w, h, title, body="", fc=SOFT, ec=ACC, tsize=7.6, bsize=5.9):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=fc, ec=ec, lw=1.2))
    ax.text(x + w / 2, y + h - 0.16, title, ha="center", va="top", fontsize=tsize, fontweight="bold", color=INK)
    if body:
        ax.text(x + w / 2, y + h - 0.62, body, ha="center", va="top", fontsize=bsize, color="#3b4060", linespacing=1.35)


def arrow(ax, p, q, text="", rad=0.0, color=GREY, off=(0, 0.14)):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=9, lw=1.1, color=color,
                                 connectionstyle=f"arc3,rad={rad}"))
    if text:
        ax.text((p[0] + q[0]) / 2 + off[0], (p[1] + q[1]) / 2 + off[1], text, ha="center", fontsize=5.8, color=color)


def architecture(path):
    fig, ax = plt.subplots(figsize=(7.1, 3.55), dpi=220)
    ax.set_xlim(0, 14.2)
    ax.set_ylim(0, 7.2)
    ax.axis("off")

    box(ax, 0.1, 4.9, 2.9, 2.1, "Dataset generator", "seeded RNG (reproducible)\n10 closest-pair files\n10 integer-mult files\n+ manifest.csv", fc="#fff7ed", ec="#f97316")
    box(ax, 0.1, 2.2, 2.9, 2.1, "Input file", "any .txt dataset, chosen\nin the UI or the CLI\n(points  or  two integers)", fc="#fff7ed", ec="#f97316")
    box(ax, 3.7, 3.2, 2.5, 2.1, "Parser / detector", "skips # comments\ndetects problem type\nvalidates the format", fc="#f1f5f9", ec=GREY)
    box(ax, 6.9, 4.9, 3.3, 2.1, "Closest pair  O(n log n)", "sort by x, split at median,\nrecurse, merge by y,\ncheck δ-strip (≤ 7 neighbours)\nT(n) = 2T(n/2) + O(n)", fc=SOFT, ec=ACC)
    box(ax, 6.9, 2.2, 3.3, 2.1, "Karatsuba  Θ(n^1.585)", "ab = z2*10^2m + z1*10^m + z0\n3 sub-products instead of 4\nz1 = (a1+a0)(b1+b0) - z2 - z0\nT(n) = 3T(n/2) + O(n)", fc=SOFT, ec=ACC)
    box(ax, 10.9, 2.2, 3.2, 4.8, "Result & trace recorder", "divide / combine / base-case\nevents, operation counters,\npartial results, final answer", fc="#ecfdf5", ec=OK)
    box(ax, 6.9, 0.1, 3.3, 1.6, "Verifier", "brute force / big-int product\n-> PASS / FAIL for every file", fc="#ecfdf5", ec=OK)
    box(ax, 10.9, 0.1, 3.2, 1.6, "Interactive visualizer", "canvas animation, step log,\nplay / step / speed controls", fc="#eef2ff", ec="#4338ca")

    arrow(ax, (1.55, 4.9), (1.55, 4.32))
    arrow(ax, (3.0, 3.25), (3.7, 3.75))
    arrow(ax, (6.2, 4.75), (6.9, 5.7))
    arrow(ax, (6.2, 3.75), (6.9, 3.25))
    arrow(ax, (10.2, 5.95), (10.9, 5.95))
    arrow(ax, (10.2, 3.25), (10.9, 3.25))
    arrow(ax, (8.55, 2.2), (8.55, 1.72), "result", off=(0.45, 0))
    arrow(ax, (12.5, 2.2), (12.5, 1.72), "events", off=(0.45, 0))
    arrow(ax, (10.2, 0.9), (10.9, 0.9))
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def scaling(path):
    rows = json.load(open(RES))
    mul = [r for r in rows if r["problem"] == "Integer multiplication"]
    cp = [r for r in rows if r["problem"] == "Closest pair"]
    fig, axs = plt.subplots(1, 2, figsize=(7.1, 2.1), dpi=220)

    n = [r["size"] for r in mul]
    k = [int(r["dc_ops"].split()[0]) for r in mul]
    s = [int(r["brute_ops"].split()[0]) for r in mul]
    ax = axs[0]
    ax.loglog(n, s, "o-", color="#f97316", lw=1.6, ms=3.5, label="grade school  Θ(n²)")
    ax.loglog(n, k, "o-", color=ACC, lw=1.6, ms=3.5, label="Karatsuba  Θ(n^1.585)")
    ax.set_xlabel("digits per operand", fontsize=7.5)
    ax.set_ylabel("single-digit products", fontsize=7.5)
    ax.set_title("Integer multiplication", fontsize=8.5, color=INK)
    ax.legend(fontsize=6.5, frameon=False)

    n2 = [r["size"] for r in cp]
    d = [r["dc_ms"] for r in cp]
    b = [r["brute_ms"] for r in cp]
    ax = axs[1]
    ax.loglog(n2, b, "o-", color="#f97316", lw=1.6, ms=3.5, label="brute force  Θ(n²)")
    ax.loglog(n2, d, "o-", color=ACC, lw=1.6, ms=3.5, label="divide & conquer  Θ(n log n)")
    ax.set_xlabel("number of points", fontsize=7.5)
    ax.set_ylabel("running time (ms)", fontsize=7.5)
    ax.set_title("Closest pair of points", fontsize=8.5, color=INK)
    ax.legend(fontsize=6.5, frameon=False)
    for a in axs:
        a.tick_params(labelsize=6.5)
        for sp in ("top", "right"):
            a.spines[sp].set_visible(False)
        a.grid(alpha=0.25, which="both", lw=0.4)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    architecture(os.path.join(HERE, "fig_architecture.png"))
    scaling(os.path.join(HERE, "fig_scaling.png"))
    print("figures written")
