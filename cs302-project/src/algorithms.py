"""
CS302 - Design and Analysis of Algorithms (Fall 2026)
Divide-and-conquer algorithms used by the project (Parts 1, 2 and 3).

Every algorithm also returns an operation count (comparisons, multiplications,
probes, ...) so that the analysis in the report can be checked empirically.
"""
from __future__ import annotations

import math
import random
import sys

try:                                   # Python >= 3.11 limits int<->str size
    sys.set_int_max_str_digits(0)
except AttributeError:                 # pragma: no cover
    pass

INF = float("inf")


# --------------------------------------------------------------------------
# 1(a)  Largest and smallest element  (Levitin Ex. 5.1-2)
# --------------------------------------------------------------------------
def min_max_dc(a):
    """Divide-and-conquer min/max. Returns (minimum, maximum, comparisons)."""
    cnt = [0]

    def rec(lo, hi):
        if lo == hi:                       # one element: 0 comparisons
            return a[lo], a[lo]
        if hi - lo == 1:                   # two elements: 1 comparison
            cnt[0] += 1
            return (a[lo], a[hi]) if a[lo] < a[hi] else (a[hi], a[lo])
        mid = (lo + hi) // 2
        mn1, mx1 = rec(lo, mid)
        mn2, mx2 = rec(mid + 1, hi)
        cnt[0] += 2                        # one compare for min, one for max
        return (mn1 if mn1 < mn2 else mn2), (mx1 if mx1 > mx2 else mx2)

    mn, mx = rec(0, len(a) - 1)
    return mn, mx, cnt[0]


def min_max_brute(a):
    """Brute force: 2(n-1) comparisons."""
    cnt = 0
    mn = mx = a[0]
    for v in a[1:]:
        cnt += 1
        if v < mn:
            mn = v
        cnt += 1
        if v > mx:
            mx = v
    return mn, mx, cnt


# --------------------------------------------------------------------------
# 1(b)  Exponentiation a^n  (Levitin Ex. 5.1-3)
# --------------------------------------------------------------------------
def power_dc(a, n):
    """
    Textbook divide and conquer: a^n = a^floor(n/2) * a^ceil(n/2).
    Both halves are computed recursively.  Returns (value, multiplications).
    M(n) = M(floor(n/2)) + M(ceil(n/2)) + 1,  M(1) = 0   ->   M(n) = n - 1
    """
    cnt = [0]

    def rec(k):
        if k == 1:
            return a
        left = rec(k // 2)
        right = rec(k - k // 2)
        cnt[0] += 1
        return left * right

    return rec(n), cnt[0]


def power_dc_reuse(a, n):
    """
    Improved divide and conquer: compute a^floor(n/2) ONCE and square it.
    M(n) = M(floor(n/2)) + 1 (+1 if n is odd)   ->   Theta(log n)
    """
    cnt = [0]

    def rec(k):
        if k == 1:
            return a
        half = rec(k // 2)
        cnt[0] += 1
        res = half * half
        if k % 2:
            cnt[0] += 1
            res *= a
        return res

    return rec(n), cnt[0]


def power_brute(a, n):
    """Brute force: n-1 multiplications."""
    res, cnt = a, 0
    for _ in range(n - 1):
        res *= a
        cnt += 1
    return res, cnt


# --------------------------------------------------------------------------
# 1(c)  Counting inversions  (Levitin Ex. 5.1-9)
# --------------------------------------------------------------------------
def count_inversions(a):
    """Merge-sort based O(n log n) inversion count. Returns (sorted, inversions)."""
    n = len(a)
    if n <= 1:
        return list(a), 0
    mid = n // 2
    left, x = count_inversions(a[:mid])
    right, y = count_inversions(a[mid:])
    merged, i, j, z = [], 0, 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:                              # left[i..] are all > right[j]
            merged.append(right[j])
            z += len(left) - i
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, x + y + z


def count_inversions_brute(a):
    n = len(a)
    return sum(1 for i in range(n) for j in range(i + 1, n) if a[i] > a[j])


# --------------------------------------------------------------------------
# 1(d)  Quicksort  (Levitin Sec. 5.2) - instrumented with comparison counter
# --------------------------------------------------------------------------
def quicksort(a, pivot="first"):
    """
    In-place-style quicksort (Lomuto partition, explicit stack so that the
    quadratic worst case does not hit Python's recursion limit).
    pivot = "first"  -> pivot is the first element  (worst case: sorted input)
    pivot = "median" -> pivot is forced to be the true median of the sub-array
                        (demonstrates the best case, perfectly balanced splits)
    Returns (sorted_list, key_comparisons).
    """
    a = list(a)
    cnt = 0
    stack = [(0, len(a) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue
        if pivot == "median":
            seg = sorted(a[lo:hi + 1])                     # not counted: forces best case
            med = seg[(len(seg) - 1) // 2]
            k = a.index(med, lo, hi + 1)
            a[lo], a[k] = a[k], a[lo]
        p = a[lo]
        i = lo
        for j in range(lo + 1, hi + 1):
            cnt += 1
            if a[j] < p:
                i += 1
                a[i], a[j] = a[j], a[i]
        a[lo], a[i] = a[i], a[lo]
        stack.append((lo, i - 1))
        stack.append((i + 1, hi))
    return a, cnt


# --------------------------------------------------------------------------
# 1(e)  1-D closest pair  (Levitin Ex. 5.5-1)
# --------------------------------------------------------------------------
def _quickselect(a, k):
    """k-th smallest (0-based), expected O(n)."""
    a = list(a)
    while True:
        p = random.choice(a)
        lo = [x for x in a if x < p]
        eq = [x for x in a if x == p]
        if k < len(lo):
            a = lo
        elif k < len(lo) + len(eq):
            return p
        else:
            k -= len(lo) + len(eq)
            a = [x for x in a if x > p]


def closest_pair_1d(a):
    """
    Divide and conquer on the value axis.
      divide : split at the median into L (<= m) and R (> m)
      conquer: closest pair inside L and inside R
      combine: the only new candidate is (max L, min R)
    T(n) = 2T(n/2) + Theta(n)  ->  Theta(n log n).
    Returns (distance, (x, y)).
    """
    def rec(v):
        n = len(v)
        if n == 2:
            x, y = (v[0], v[1]) if v[0] <= v[1] else (v[1], v[0])
            return y - x, (x, y)
        if n == 3:
            s = sorted(v)
            c1, c2 = s[1] - s[0], s[2] - s[1]
            return (c1, (s[0], s[1])) if c1 <= c2 else (c2, (s[1], s[2]))
        m = _quickselect(v, (n - 1) // 2)
        left = [x for x in v if x < m]
        eq = [x for x in v if x == m]
        if len(eq) > 1:                    # two identical numbers: distance 0
            return 0, (m, m)
        left.append(m)
        right = [x for x in v if x > m]
        dl, pl = rec(left)
        dr, pr = rec(right)
        best = (dl, pl) if dl <= dr else (dr, pr)
        lmax, rmin = max(left), min(right)
        if rmin - lmax < best[0]:
            best = (rmin - lmax, (lmax, rmin))
        return best

    return rec(list(a))


def closest_pair_1d_brute(a):
    best = (INF, None)
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            d = abs(a[i] - a[j])
            if d < best[0]:
                best = (d, tuple(sorted((a[i], a[j]))))
    return best


# --------------------------------------------------------------------------
# 1(f)  Kleinberg, Solved Exercise 1 (p.242): peak of a unimodal array
# --------------------------------------------------------------------------
def unimodal_peak(a):
    """
    A[0] < ... < A[p] > ... > A[n-1].  Binary search, O(log n) reads.
    Returns (p, array_reads).
    """
    lo, hi, reads = 0, len(a) - 1, 0
    while lo < hi:
        mid = (lo + hi) // 2
        reads += 2
        if a[mid] < a[mid + 1]:            # still climbing: peak is to the right
            lo = mid + 1
        else:                              # descending: peak is at mid or left
            hi = mid
    return lo, reads


# --------------------------------------------------------------------------
# 1(g)  Kleinberg, Solved Exercise 2 (p.244): best days to buy and sell
# --------------------------------------------------------------------------
def best_trade_dc(p):
    """
    Pair (i<j) maximising p[j]-p[i].  Divide and conquer exactly as in the
    textbook: best pair in the left half, best pair in the right half, or
    buy at the cheapest left day and sell at the dearest right day.
    The cross term is found by a linear scan  ->  T(n) = 2T(n/2)+O(n) = O(n log n).
    Returns (i, j, profit)  (profit may be <= 0 if prices only fall).
    """
    def rec(lo, hi):
        if hi - lo < 1:
            return None
        if hi - lo == 1:
            return lo, hi
        mid = (lo + hi) // 2
        cands = [rec(lo, mid), rec(mid + 1, hi)]
        i = min(range(lo, mid + 1), key=lambda k: p[k])
        j = max(range(mid + 1, hi + 1), key=lambda k: p[k])
        cands.append((i, j))
        cands = [c for c in cands if c]
        return max(cands, key=lambda c: p[c[1]] - p[c[0]])

    i, j = rec(0, len(p) - 1)
    return i, j, p[j] - p[i]


def best_trade_dc_linear(p):
    """Refinement: each call also returns (min, max) so the combine is O(1) -> O(n)."""
    def rec(lo, hi):
        if lo == hi:
            return None, lo, lo            # best pair, argmin, argmax
        mid = (lo + hi) // 2
        bl, mnl, mxl = rec(lo, mid)
        br, mnr, mxr = rec(mid + 1, hi)
        mn = mnl if p[mnl] <= p[mnr] else mnr
        mx = mxl if p[mxl] >= p[mxr] else mxr
        cands = [c for c in (bl, br, (mnl, mxr)) if c]
        best = max(cands, key=lambda c: p[c[1]] - p[c[0]])
        return best, mn, mx

    (i, j), _, _ = rec(0, len(p) - 1)
    return i, j, p[j] - p[i]


def best_trade_brute(p):
    best = None
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if best is None or p[j] - p[i] > best[2]:
                best = (i, j, p[j] - p[i])
    return best


# --------------------------------------------------------------------------
# 1(h)  Three exercises from Kleinberg, Chapter 5 (pp.246-249)
# --------------------------------------------------------------------------
# ---- Exercise 1: median of two databases with O(log n) queries -----------
class Database:
    """Sorted database that can only be accessed through k-th smallest queries."""

    def __init__(self, values):
        self._v = sorted(values)
        self.queries = 0

    def __len__(self):
        return len(self._v)

    def query(self, k):                     # 1-based k
        self.queries += 1
        return self._v[k - 1]


def median_two_databases(db1, db2):
    """
    n values in each database (all distinct).  Returns the n-th smallest of the
    2n values using about 2*log2(n)+2 queries.
    Repeatedly look at the (k/2)-th remaining value of each database: the
    smaller one, and everything below it, cannot be the answer's successor
    so up to k/2 candidates are discarded from that database.
    """
    n = len(db1)
    a_off = b_off = 0                       # elements already discarded
    k = n                                   # we still need the k-th smallest of the rest
    while k > 1:
        h = k // 2
        a = db1.query(a_off + h) if a_off + h <= n else INF
        b = db2.query(b_off + h) if b_off + h <= n else INF
        if a < b:
            a_off += h
        else:
            b_off += h
        k -= h
    a = db1.query(a_off + 1) if a_off < n else INF
    b = db2.query(b_off + 1) if b_off < n else INF
    return min(a, b)


# ---- Exercise 2: significant inversions  L[i] > 2*L[j], i<j ---------------
def count_significant_inversions(a):
    """O(n log n): count cross pairs with a two-pointer sweep BEFORE merging."""
    n = len(a)
    if n <= 1:
        return list(a), 0
    mid = n // 2
    left, x = count_significant_inversions(a[:mid])
    right, y = count_significant_inversions(a[mid:])
    z, j = 0, 0
    for v in left:                          # left is sorted ascending
        while j < len(right) and v > 2 * right[j]:
            j += 1
        z += j
    return sorted(left + right), x + y + z  # Timsort merges two runs in linear time


def count_significant_inversions_brute(a):
    n = len(a)
    return sum(1 for i in range(n) for j in range(i + 1, n) if a[i] > 2 * a[j])


# ---- Exercise 3: bank cards -- is there an equivalence class with > n/2? --
class EquivalenceTester:
    """Cards are opaque; the only operation is 'are these two equivalent?'."""

    def __init__(self, accounts):
        self._acc = list(accounts)          # hidden account id of every card
        self.tests = 0

    def __len__(self):
        return len(self._acc)

    def same(self, i, j):
        self.tests += 1
        return self._acc[i] == self._acc[j]


def majority_card(tester, idx=None):
    """
    Returns the index of a card belonging to a class with MORE than half of the
    cards in idx (None if there is none).  T(n) = 2T(n/2) + 2n -> O(n log n).
    """
    if idx is None:
        idx = list(range(len(tester)))
    n = len(idx)
    if n == 1:
        return idx[0]
    mid = n // 2
    cands = []
    for part in (idx[:mid], idx[mid:]):
        c = majority_card(tester, part)
        if c is not None:
            cands.append(c)
    for c in cands:                          # a global majority must be a majority of a half
        eq = sum(1 for i in idx if i == c or tester.same(c, i))
        if eq > n / 2:
            return c
    return None


# --------------------------------------------------------------------------
# Part 2 problem (i): closest pair of points in the plane  O(n log n)
# --------------------------------------------------------------------------
def closest_pair_2d(points):
    """
    points: list of (x, y).  Returns (distance, p, q).
    Classic algorithm: sort by x once, recurse, merge by y, check the strip.
    """
    pts = [(x, y, i) for i, (x, y) in enumerate(points)]
    px = sorted(pts)
    py = sorted(pts, key=lambda t: (t[1], t[0], t[2]))

    def dist(a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def rec(px, py):
        n = len(px)
        if n <= 3:
            best = (INF, None, None)
            for i in range(n):
                for j in range(i + 1, n):
                    d = dist(px[i], px[j])
                    if d < best[0]:
                        best = (d, px[i], px[j])
            return best
        mid = n // 2
        midx = px[mid][0]
        left_ids = {t[2] for t in px[:mid]}
        pyl = [t for t in py if t[2] in left_ids]
        pyr = [t for t in py if t[2] not in left_ids]
        best = min(rec(px[:mid], pyl), rec(px[mid:], pyr), key=lambda r: r[0])
        d = best[0]
        strip = [t for t in py if abs(t[0] - midx) < d]
        for i in range(len(strip)):
            for j in range(i + 1, min(i + 8, len(strip))):
                if strip[j][1] - strip[i][1] >= d:
                    break
                dd = dist(strip[i], strip[j])
                if dd < d:
                    d = dd
                    best = (dd, strip[i], strip[j])
        return best

    d, p, q = rec(px, py)
    return d, (p[0], p[1]), (q[0], q[1])


def closest_pair_2d_brute(points):
    best = (INF, None, None)
    n = len(points)
    for i in range(n):
        xi, yi = points[i]
        for j in range(i + 1, n):
            d = math.hypot(xi - points[j][0], yi - points[j][1])
            if d < best[0]:
                best = (d, points[i], points[j])
    return best


# --------------------------------------------------------------------------
# Part 2 problem (ii): integer multiplication (Karatsuba)  O(n^1.585)
# --------------------------------------------------------------------------
def _ndigits(x):
    return len(str(x)) if x else 1


def karatsuba(x, y):
    """
    Karatsuba multiplication of non-negative integers.
    Returns (product, single_digit_multiplications).
    x*y = z2*10^(2m) + (z1)*10^m + z0   with only THREE recursive products.
    """
    cnt = [0]

    def rec(x, y):
        if x < 10 or y < 10:
            small, big = (x, y) if x < 10 else (y, x)
            cnt[0] += _ndigits(big) if small else 1     # grade-school digit products
            return x * y
        m = max(_ndigits(x), _ndigits(y)) // 2
        p = 10 ** m
        x1, x0 = divmod(x, p)
        y1, y0 = divmod(y, p)
        z2 = rec(x1, y1)
        z0 = rec(x0, y0)
        z1 = rec(x1 + x0, y1 + y0) - z2 - z0
        return z2 * p * p + z1 * p + z0

    res = rec(x, y)
    return res, cnt[0]


def grade_school_digit_products(x, y):
    """Number of single-digit products of the pencil-and-paper method = n * m."""
    return _ndigits(x) * _ndigits(y)
