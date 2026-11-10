"""
Part 3 - apply both algorithms to all 20 dataset files and verify the answers.

  closest pair : divide & conquer  vs  brute force  (distance must match)
  multiplication: Karatsuba        vs  Python's built-in big-int product (must match)

Output: results/benchmark_results.csv, results/benchmark_results.md, results/benchmark_results.json
"""
import csv
import glob
import json
import math
import os
import time

from algorithms import (closest_pair_2d, closest_pair_2d_brute, grade_school_digit_products, karatsuba)

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "datasets")
OUT = os.path.join(HERE, "..", "results")


def read_lines(path):
    with open(path) as f:
        return [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]


def read_points(path):
    lines = read_lines(path)
    n = int(lines[0])
    pts = [tuple(float(t) for t in ln.split()) for ln in lines[1:1 + n]]
    assert len(pts) == n
    return pts


def read_ints(path):
    lines = read_lines(path)
    return int(lines[0]), int(lines[1])


def timed(fn, *args):
    t = time.perf_counter()
    r = fn(*args)
    return r, (time.perf_counter() - t) * 1000.0


def main():
    os.makedirs(OUT, exist_ok=True)
    rows = []

    for path in sorted(glob.glob(os.path.join(DATA, "closest_pair", "*.txt"))):
        pts = read_points(path)
        (d, p, q), t_dc = timed(closest_pair_2d, pts)
        (db, pb, qb), t_bf = timed(closest_pair_2d_brute, pts)
        ok = math.isclose(d, db, rel_tol=1e-12, abs_tol=1e-9)
        rows.append(dict(problem="Closest pair", file=os.path.basename(path), size=len(pts),
                         result=f"d = {d:.4f} between ({p[0]:.3f},{p[1]:.3f}) and ({q[0]:.3f},{q[1]:.3f})",
                         dc_ms=round(t_dc, 2), brute_ms=round(t_bf, 2),
                         dc_ops="-", brute_ops=f"{len(pts)*(len(pts)-1)//2} pair checks",
                         correct="PASS" if ok else "FAIL"))
        print(rows[-1]["file"], rows[-1]["correct"], rows[-1]["result"])

    for path in sorted(glob.glob(os.path.join(DATA, "integer_multiplication", "*.txt"))):
        a, b = read_ints(path)
        (prod, ops), t_dc = timed(karatsuba, a, b)
        ref, t_bf = timed(lambda x, y: x * y, a, b)
        school = grade_school_digit_products(a, b)
        ok = prod == ref
        s = str(prod)
        rows.append(dict(problem="Integer multiplication", file=os.path.basename(path), size=len(str(a)),
                         result=f"{len(s)}-digit product {s[:8]}...{s[-6:]}",
                         dc_ms=round(t_dc, 2), brute_ms=round(t_bf, 4),
                         dc_ops=f"{ops} digit mults (Karatsuba)", brute_ops=f"{school} digit mults (grade school)",
                         correct="PASS" if ok else "FAIL"))
        print(rows[-1]["file"], rows[-1]["correct"], rows[-1]["result"], f"| {ops} vs {school}")

    with open(os.path.join(OUT, "benchmark_results.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(OUT, "benchmark_results.json"), "w") as f:
        json.dump(rows, f, indent=2)
    with open(os.path.join(OUT, "benchmark_results.md"), "w") as f:
        f.write("| Problem | File | Size | D&C result | D&C ms | Reference ms | Operation counts | Check |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        for r in rows:
            ops = r["brute_ops"] if r["dc_ops"] == "-" else f"{r['dc_ops']} vs {r['brute_ops']}"
            f.write(f"| {r['problem']} | {r['file']} | {r['size']} | {r['result']} | {r['dc_ms']} | "
                    f"{r['brute_ms']} | {ops} | {r['correct']} |\n")
    bad = [r["file"] for r in rows if r["correct"] != "PASS"]
    print("\nALL 20 FILES CORRECT" if not bad else f"\nFAILED: {bad}")


if __name__ == "__main__":
    main()
