"""Same-month ratio for the wash-out row of Table 1, and Nov-Dec 2025 spill-over shares.

Uses the formula of same_month() in the pack's code/analyze.py: ratio of strict shares,
95% interval on the log scale with se = sqrt(1/y1 - 1/n1 + 1/y0 - 1/n0).
Wash-out: drop November in both years (and October, which same_month() already leaves out),
so Dec 2025-Sep 2026 is compared with Dec 2024-Sep 2025. An asymmetric variant that keeps
Nov 2024 in the comparison window is also printed.
Spill-over: pooled strict share in non-CS groups with no CS listing, Nov-Dec 2025 against
Nov-Dec 2024, with Wilson intervals for each share and the same log-scale interval for the ratio.
Usage: python -I washout_same_month.py <monthly_series.csv>
"""
import csv, math, sys

M = {r["month"]: r for r in csv.DictReader(open(sys.argv[1]))}

def months(a, b):
    (y, m), out = a, []
    while (y, m) <= b:
        out.append(f"{y}-{m:02d}")
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out

def tot(col, ms):
    return sum(int(M[k][col]) for k in ms)

def ratio(yc, nc, before, after):
    y0, n0, y1, n1 = tot(yc, before), tot(nc, before), tot(yc, after), tot(nc, after)
    r = (y1 / n1) / (y0 / n0)
    se = math.sqrt(1 / y1 - 1 / n1 + 1 / y0 - 1 / n0)
    return r, r * math.exp(-1.96 * se), r * math.exp(1.96 * se), y0, n0, y1, n1

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, c - h, c + h

def show(lab, t):
    r, lo, hi, y0, n0, y1, n1 = t
    print(f"{lab}: {r:.3f} ({lo:.3f}-{hi:.3f}); before {y0}/{n0} = {100*y0/n0:.2f}%, after {y1}/{n1} = {100*y1/n1:.2f}%")

Y, N = "Y_cs_any|strict", "N_cs_any"
show("Primary check (Nov 2025-Sep 2026 vs Nov 2024-Sep 2025)",
     ratio(Y, N, months((2024, 11), (2025, 9)), months((2025, 11), (2026, 9))))
show("Wash-out, symmetric (Dec 2025-Sep 2026 vs Dec 2024-Sep 2025)",
     ratio(Y, N, months((2024, 12), (2025, 9)), months((2025, 12), (2026, 9))))
show("Wash-out, asymmetric (Dec 2025-Sep 2026 vs Nov 2024-Sep 2025)",
     ratio(Y, N, months((2024, 11), (2025, 9)), months((2025, 12), (2026, 9))))

YS, NS = "Y_spill_pooled|strict", "N_spill_pooled"
print("\nPooled spill-over groups (no CS listing), strict share; denominator counts a paper in two groups twice")
for lab, ms in (("Nov-Dec 2024", months((2024, 11), (2024, 12))), ("Nov-Dec 2025", months((2025, 11), (2025, 12))),
                ("Jan-Oct 2025", months((2025, 1), (2025, 10))), ("Jan-Sep 2026", months((2026, 1), (2026, 9)))):
    k, n = tot(YS, ms), tot(NS, ms)
    p, lo, hi = wilson(k, n)
    print(f"{lab}: {k}/{n} = {100*p:.2f}% (Wilson 95% {100*lo:.2f}-{100*hi:.2f})")
for mo in ("2024-11", "2024-12", "2025-10", "2025-11", "2025-12"):
    k, n = int(M[mo][YS]), int(M[mo][NS]); p, lo, hi = wilson(k, n)
    print(f"  {mo}: {k}/{n} = {100*p:.2f}% ({100*lo:.2f}-{100*hi:.2f})")
show("Spill-over same-month ratio, Nov-Dec 2025 vs Nov-Dec 2024",
     ratio(YS, NS, months((2024, 11), (2024, 12)), months((2025, 11), (2025, 12))))
