# CS302 – Design and Analysis of Algorithms · Fall 2026 · Divide-and-Conquer Project

| Part | Marks | Where |
|---|---|---|
| 1 · Implement (a)–(h), user-defined input size ≥ 10 | 40 | `src/algorithms.py`, `src/part1_demo.py`, written answers in `docs/PART1_ANSWERS.md` |
| 2 · 10 + 10 random input files, every size > 100 | 10 | `src/generate_datasets.py` → `datasets/` (+ `datasets/manifest.csv`) |
| 3 · Apply the algorithms to the datasets | 5 | `src/run_benchmarks.py` → `results/benchmark_results.{csv,md,json}` |
| 4 · User interface (pick any file, watch both algorithms) | 30 | `ui/visualizer.html` – just double-click it |
| 5 · 3-page report | 15 | `docs/CS302_Project_Report.docx` (+ `.pdf`) |

Requirements: Python 3.9+ (no third-party packages needed to run the algorithms), any modern browser for the UI.
`python-docx` and `matplotlib` are only needed to rebuild the report and its figures.

## Run it

```bash
# Part 1 – all eight problems on an input size you choose (asks interactively if --n is omitted)
python3 src/part1_demo.py --n 25
python3 src/part1_demo.py --n 64 --only a,d,h        # only some parts

# self-checks: every algorithm against brute force
python3 src/tests.py

# Part 2 – regenerate the 20 dataset files (deterministic seeds)
python3 src/generate_datasets.py

# Part 3 – run both algorithms on all 20 files and verify them
python3 src/run_benchmarks.py

# Part 4 – open ui/visualizer.html in a browser, click the drop area, choose any dataset file
```

## File formats

* `closest_pair_XX.txt` – optional `#` comment lines, then `n`, then `n` lines `x y`.
* `int_mult_XX.txt` – optional `#` comment lines, then two lines, each one non-negative integer.

The visualizer detects the type automatically.

## Reproducibility

Dataset seeds are `3022027…3022036` (points) and `3022127…3022136` (integers); each file’s first line records its seed.
Results of the last run are in `results/`.

## Rebuilding the report

```bash
cd docs && python3 make_figures.py && python3 build_report.py      # then open / export the .docx
```

Fill in the group-member names on the first page of the report before submitting, and re-run `src/run_benchmarks.py`
on the presentation computer if you want the timings in Table 2 to reflect that machine.
