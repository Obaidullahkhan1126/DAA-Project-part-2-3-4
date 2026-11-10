"""
Part 1 demo - runs every divide-and-conquer algorithm on a user-defined input size.

    python3 part1_demo.py            # asks for n interactively
    python3 part1_demo.py --n 25     # non-interactive
    python3 part1_demo.py --n 25 --seed 7 --only a,c,g
"""
import argparse
import math
import random

from algorithms import *


def show(label, items):
    print(f"  {label:<34}{items}")


def head(txt):
    print("\n" + "=" * 74 + f"\n{txt}\n" + "=" * 74)


def preview(a, k=12):
    return str(a) if len(a) <= k else str(a[:k])[:-1] + f", ... ({len(a)} items)]"


def part_a(n):
    head("1(a)  Largest and smallest element - Levitin 5.1(2)")
    a = [random.randint(-999, 999) for _ in range(n)]
    show("input", preview(a))
    mn, mx, c = min_max_dc(a)
    _, _, cb = min_max_brute(a)
    show("divide & conquer  (min, max)", (mn, mx))
    show("comparisons: D&C / brute", f"{c} / {cb}")
    if n & (n - 1) == 0:
        show("formula 3n/2 - 2 (n = 2^k)", 3 * n // 2 - 2)
    else:
        m = 2 ** math.ceil(math.log2(n))
        mm, _, cc = min_max_dc(random.sample(range(10**5), m))
        show(f"same algorithm for n = {m} = 2^k", f"{cc} comparisons = 3*{m}/2 - 2 = {3*m//2-2}")


def part_b(n):
    head("1(b)  Exponentiation a^n - Levitin 5.1(3)")
    a = random.randint(2, 9)
    v1, c1 = power_dc(a, n)
    v2, c2 = power_dc_reuse(a, n)
    v3, c3 = power_brute(a, n)
    show("a, n", (a, n))
    show("a^n correct (all 3 methods)?", v1 == v2 == v3 == a ** n)
    show("mults: D&C a^(n/2)*a^(n/2)", f"{c1}   (recurrence M(n)=2M(n/2)+1 -> n-1 = {n-1})")
    show("mults: D&C with reuse (square)", f"{c2}   (Theta(log n))")
    show("mults: brute force", f"{c3}   (n-1)")


def part_c(n):
    head("1(c)  Counting inversions in O(n log n) - Levitin 5.1(9)")
    a = [random.randint(0, 99) for _ in range(n)]
    show("input", preview(a))
    _, inv = count_inversions(a)
    show("inversions (merge-sort based)", inv)
    show("inversions (brute force O(n^2))", count_inversions_brute(a))


def part_d(n):
    head("1(d)  Quicksort best / worst case - Levitin Sec. 5.2")
    a = random.sample(range(10**6), n)
    _, avg = quicksort(a)
    _, worst = quicksort(sorted(a))
    m = 2 ** max(2, math.ceil(math.log2(n + 1))) - 1          # n = 2^k - 1 for a perfect best case
    _, best = quicksort(random.sample(range(10**6), m), "median")
    k = int(math.log2(m + 1))
    show(f"random input, n={n}", f"{avg} comparisons (average case is Theta(n log n), ~1.39 n log2 n asymptotically)")
    show(f"worst case (sorted), n={n}", f"{worst} comparisons = n(n-1)/2 = {n*(n-1)//2}   -> Theta(n^2)")
    show(f"best case (median pivot), n={m}", f"{best} comparisons = (n+1)log2(n+1)-2n = {(m+1)*k-2*m}   -> Theta(n log n)")


def part_e(n):
    head("1(e)  Closest pair of numbers (1-D) - Levitin 5.5(1)")
    a = [round(random.uniform(0, 1000), 2) for _ in range(n)]
    show("input", preview(a))
    d, pr = closest_pair_1d(a)
    show("divide & conquer", f"distance {d:.2f} between {pr}")
    db, pb = closest_pair_1d_brute(a)
    show("brute force", f"distance {db:.2f} between {pb}")
    show("efficiency class", "T(n)=2T(n/2)+Theta(n)  ->  Theta(n log n)")
    show("good algorithm?", "No: sort + scan neighbours is also Theta(n log n) and simpler")


def part_f(n):
    head("1(f)  Kleinberg Solved Exercise 1 (p.242): peak of a unimodal array")
    p = random.randint(1, n - 2) if n > 2 else 0
    vals = sorted(random.sample(range(10**4), n))
    random.shuffle(vals)
    top = max(vals)
    rest = [v for v in vals if v != top]
    left = sorted(rest[:p])                                   # strictly increasing up to the peak
    right = sorted(rest[p:], reverse=True)                    # strictly decreasing afterwards
    a = left + [top] + right
    show("array", preview(a))
    idx, reads = unimodal_peak(a)
    show("peak index / value", (idx, a[idx]))
    show("array entries read", f"{reads}  (<= 2*ceil(log2 n) = {2*math.ceil(math.log2(n))})")


def part_g(n):
    head("1(g)  Kleinberg Solved Exercise 2 (p.244): best buy / sell days")
    p = [random.randint(20, 120) for _ in range(n)]
    show("prices (day 1..n)", preview(p))
    i, j, pr = best_trade_dc(p)
    i2, j2, pr2 = best_trade_dc_linear(p)
    ib, jb, prb = best_trade_brute(p)
    show("D&C  O(n log n)", f"buy day {i+1}, sell day {j+1}, profit {pr}")
    show("D&C  O(n) refinement", f"buy day {i2+1}, sell day {j2+1}, profit {pr2}")
    show("brute force O(n^2)", f"buy day {ib+1}, sell day {jb+1}, profit {prb}")
    if pr <= 0:
        show("note", "prices never rise: no way to make money")


def part_h(n):
    head("1(h)  Kleinberg Chapter 5 exercises 1, 2 and 3 (pp.246-247)")
    print("  -- Exercise 1: median of two databases with O(log n) queries --")
    vals = random.sample(range(10**6), 2 * n)
    d1, d2 = Database(vals[:n]), Database(vals[n:])
    med = median_two_databases(d1, d2)
    show("n per database", n)
    show("median found / true median", f"{med} / {sorted(vals)[n-1]}")
    show("queries used", f"{d1.queries + d2.queries}  (bound 2*ceil(log2 n)+2 = {2*math.ceil(math.log2(n))+2})")
    print("  -- Exercise 2: significant inversions  L[i] > 2 L[j], i < j --")
    a = [random.randint(1, 50) for _ in range(n)]
    show("input", preview(a))
    show("D&C count / brute force", f"{count_significant_inversions(a)[1]} / {count_significant_inversions_brute(a)}")
    print("  -- Exercise 3: bank cards, is there a class with > n/2 cards? --")
    for label, accs in (("with a majority account",
                         [7 if random.random() < 0.65 else random.randint(0, 20) for _ in range(n)]),
                        ("without majority", [random.randint(0, 5) for _ in range(n)])):
        t = EquivalenceTester(accs)
        c = majority_card(t)
        top = max(set(accs), key=accs.count)
        truth = accs.count(top) > n / 2
        show(label, f"found={'yes' if c is not None else 'no'} (truth {'yes' if truth else 'no'}), "
                    f"{t.tests} equivalence tests (n log2 n = {n*math.log2(n):.0f})")


PARTS = {"a": part_a, "b": part_b, "c": part_c, "d": part_d, "e": part_e,
         "f": part_f, "g": part_g, "h": part_h}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n", type=int, help="input size (>= 10)")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--only", default="a,b,c,d,e,f,g,h", help="comma separated subset, e.g. a,c,g")
    args = ap.parse_args()
    n = args.n
    while n is None or n < 10:
        try:
            n = int(input("Enter the input size n (at least 10): "))
        except ValueError:
            n = None
        if n is not None and n < 10:
            print("n must be at least 10")
    random.seed(args.seed)
    for key in args.only.split(","):
        PARTS[key.strip()](n)
    print()


if __name__ == "__main__":
    main()
