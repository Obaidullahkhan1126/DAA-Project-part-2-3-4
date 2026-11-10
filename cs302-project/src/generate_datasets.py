"""
Part 2 - generate 10 + 10 reproducible input files (every file has size > 100).

  datasets/closest_pair/closest_pair_01.txt .. _10.txt
        line 1 : n  (number of points)
        lines  : "x y"  (one point per line, 3 decimals)
  datasets/integer_multiplication/int_mult_01.txt .. _10.txt
        line 1 : first  operand (D decimal digits)
        line 2 : second operand (D decimal digits)

Lines starting with '#' are comments (generator, seed, parameters) and are ignored by the readers.
A manifest (datasets/manifest.csv) lists seed, size, distribution and value ranges of every file.
"""
import csv
import math
import os
import random
import sys

sys.set_int_max_str_digits(0)

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "datasets")
BASE_SEED = 302_2026

# (points, distribution) - sizes grow so the files have "varying complexity"
CP_SPECS = [
    (101, "uniform"), (150, "uniform"), (250, "gaussian"), (400, "clusters"), (600, "uniform"),
    (1000, "grid-jitter"), (1500, "clusters"), (2500, "near-collinear"), (4000, "uniform"), (6000, "gaussian"),
]
SPAN = 10_000.0                                     # coordinates lie in [0, 10000]

# digits of each operand
MUL_DIGITS = [101, 128, 200, 256, 400, 512, 800, 1024, 2048, 4096]


def clamp(v):
    return min(max(v, 0.0), SPAN)


def gen_points(n, dist, rng):
    pts = []
    if dist == "uniform":
        pts = [(rng.uniform(0, SPAN), rng.uniform(0, SPAN)) for _ in range(n)]
    elif dist == "gaussian":
        pts = [(clamp(rng.gauss(SPAN / 2, SPAN / 6)), clamp(rng.gauss(SPAN / 2, SPAN / 6))) for _ in range(n)]
    elif dist == "clusters":
        centres = [(rng.uniform(1000, 9000), rng.uniform(1000, 9000)) for _ in range(6)]
        for _ in range(n):
            cx, cy = rng.choice(centres)
            pts.append((clamp(rng.gauss(cx, 350)), clamp(rng.gauss(cy, 350))))
    elif dist == "grid-jitter":                      # regular grid with small noise: many near-equal distances
        side = math.ceil(math.sqrt(n))
        step = SPAN / side
        cells = [(i, j) for i in range(side) for j in range(side)]
        rng.shuffle(cells)
        for i, j in cells[:n]:
            pts.append((clamp(i * step + rng.uniform(0, step * 0.4)), clamp(j * step + rng.uniform(0, step * 0.4))))
    elif dist == "near-collinear":                   # almost all points on a line: stresses the strip step
        for _ in range(n):
            x = rng.uniform(0, SPAN)
            pts.append((x, clamp(SPAN / 2 + 0.02 * (x - SPAN / 2) + rng.gauss(0, 40))))
    else:
        raise ValueError(dist)
    return [(round(x, 3), round(y, 3)) for x, y in pts]


def main():
    cp_dir = os.path.join(ROOT, "closest_pair")
    mul_dir = os.path.join(ROOT, "integer_multiplication")
    os.makedirs(cp_dir, exist_ok=True)
    os.makedirs(mul_dir, exist_ok=True)
    rows = []

    for k, (n, dist) in enumerate(CP_SPECS, start=1):
        seed = BASE_SEED + k
        rng = random.Random(seed)
        pts = gen_points(n, dist, rng)
        name = f"closest_pair_{k:02d}.txt"
        with open(os.path.join(cp_dir, name), "w") as f:
            f.write(f"# closest-pair dataset {k:02d} | seed={seed} | distribution={dist} | coordinates in [0, {SPAN:g}]\n")
            f.write(f"{n}\n")
            for x, y in pts:
                f.write(f"{x:.3f} {y:.3f}\n")
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        rows.append(dict(problem="closest_pair", file=name, seed=seed, size=n, distribution=dist,
                         range=f"x:[{min(xs):.3f},{max(xs):.3f}] y:[{min(ys):.3f},{max(ys):.3f}]",
                         first_values="; ".join(f"({x:.3f},{y:.3f})" for x, y in pts[:3])))

    for k, digits in enumerate(MUL_DIGITS, start=1):
        seed = BASE_SEED + 100 + k
        rng = random.Random(seed)
        a = rng.randrange(10 ** (digits - 1), 10 ** digits)
        b = rng.randrange(10 ** (digits - 1), 10 ** digits)
        name = f"int_mult_{k:02d}.txt"
        with open(os.path.join(mul_dir, name), "w") as f:
            f.write(f"# integer-multiplication dataset {k:02d} | seed={seed} | {digits} digits per operand\n")
            f.write(f"{a}\n{b}\n")
        rows.append(dict(problem="integer_multiplication", file=name, seed=seed, size=digits,
                         distribution="uniform random digits (leading digit != 0)",
                         range=f"[10^{digits-1}, 10^{digits})",
                         first_values=f"{str(a)[:12]}...; {str(b)[:12]}..."))

    with open(os.path.join(ROOT, "manifest.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} files + manifest.csv to {os.path.normpath(ROOT)}")


if __name__ == "__main__":
    main()
