"""Self-checks: every divide-and-conquer routine is compared with brute force."""
import math
import random

from algorithms import *

random.seed(302)


def test_min_max():
    for n in [1, 2, 3, 10, 17, 64, 100, 1000]:
        a = [random.randint(-10**6, 10**6) for _ in range(n)]
        mn, mx, c = min_max_dc(a)
        assert (mn, mx) == (min(a), max(a))
    for k in range(1, 11):                     # n = 2^k  ->  3n/2 - 2
        n = 2 ** k
        a = random.sample(range(10**6), n)
        assert min_max_dc(a)[2] == 3 * n // 2 - 2
        assert min_max_brute(a)[2] == 2 * (n - 1)


def test_power():
    for _ in range(200):
        a, n = random.randint(2, 9), random.randint(1, 60)
        v, c = power_dc(a, n)
        v2, c2 = power_dc_reuse(a, n)
        v3, c3 = power_brute(a, n)
        assert v == v2 == v3 == a ** n
        assert c == c3 == n - 1
        assert c2 <= 2 * math.floor(math.log2(n)) if n > 1 else c2 == 0


def test_inversions():
    for _ in range(200):
        a = [random.randint(0, 50) for _ in range(random.randint(0, 60))]
        assert count_inversions(a)[1] == count_inversions_brute(a)


def test_quicksort():
    for _ in range(100):
        a = [random.randint(0, 99) for _ in range(random.randint(0, 80))]
        assert quicksort(a)[0] == sorted(a)
        assert quicksort(a, "median")[0] == sorted(a)
    n = 200
    assert quicksort(list(range(n)))[1] == n * (n - 1) // 2          # worst case
    for k in range(2, 10):                                             # best case
        n = 2 ** k - 1
        b = random.sample(range(10**5), n)
        assert quicksort(b, "median")[1] == (n + 1) * k - 2 * n


def test_closest_1d():
    for _ in range(300):
        a = [round(random.uniform(0, 100), 2) for _ in range(random.randint(2, 40))]
        assert math.isclose(closest_pair_1d(a)[0], closest_pair_1d_brute(a)[0], abs_tol=1e-9)


def test_peak():
    for _ in range(200):
        n = random.randint(1, 100)
        p = random.randint(0, n - 1)
        vals = random.sample(range(10**6), n)
        left = sorted(vals[:p])
        right = sorted(vals[p:], reverse=True)
        a = left + right
        if left and right and left[-1] > right[0]:      # force a[p] to be the max
            continue
        assert unimodal_peak(a)[0] == a.index(max(a))


def test_trade():
    for _ in range(300):
        p = [random.randint(1, 100) for _ in range(random.randint(2, 40))]
        b = best_trade_brute(p)[2]
        assert best_trade_dc(p)[2] == b
        assert best_trade_dc_linear(p)[2] == b


def test_median_two_dbs():
    for n in [1, 2, 3, 8, 10, 33, 100, 1000]:
        vals = random.sample(range(10**7), 2 * n)
        d1, d2 = Database(vals[:n]), Database(vals[n:])
        assert median_two_databases(d1, d2) == sorted(vals)[n - 1]
        assert d1.queries + d2.queries <= 2 * math.ceil(math.log2(max(n, 2))) + 4


def test_sig_inv():
    for _ in range(200):
        a = [random.randint(1, 60) for _ in range(random.randint(0, 50))]
        assert count_significant_inversions(a)[1] == count_significant_inversions_brute(a)


def test_cards():
    for _ in range(200):
        n = random.randint(1, 40)
        k = random.randint(1, 4)
        accs = [random.randint(0, k) for _ in range(n)]
        if random.random() < 0.5:
            accs = [0 if random.random() < 0.7 else random.randint(1, 9) for _ in range(n)]
        t = EquivalenceTester(accs)
        c = majority_card(t)
        top = max(set(accs), key=accs.count)
        has = accs.count(top) > n / 2
        assert (c is not None) == has
        if has:
            assert accs[c] == top


def test_closest_2d():
    for _ in range(100):
        pts = [(round(random.uniform(0, 100), 1), round(random.uniform(0, 100), 1))
               for _ in range(random.randint(2, 120))]
        assert math.isclose(closest_pair_2d(pts)[0], closest_pair_2d_brute(pts)[0], abs_tol=1e-9)
    # duplicates and collinear points
    pts = [(1, 1)] * 5 + [(2, 2), (3, 3)]
    assert closest_pair_2d(pts)[0] == 0
    pts = [(i, 5) for i in range(50)]
    assert math.isclose(closest_pair_2d(pts)[0], 1)


def test_karatsuba():
    for _ in range(300):
        d1, d2 = random.randint(1, 80), random.randint(1, 80)
        x = random.randint(0, 10 ** d1)
        y = random.randint(0, 10 ** d2)
        assert karatsuba(x, y)[0] == x * y
    for x, y in [(0, 0), (0, 12345), (9, 9), (99, 99), (10**40, 10**40), (10**30 - 1, 10**30 - 1)]:
        assert karatsuba(x, y)[0] == x * y


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)
    print("all tests passed")
