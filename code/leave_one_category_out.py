"""Approximate leave-one-category-out check on the same-month comparison.

Inputs : results/tables/monthly_series.csv   (monthly CS totals N_cs_any and strict counts Y_cs_any|strict)
         results/tables/placement_primary.csv (strict papers by primary category, two windows)
Output : results/leave_one_category_out.csv (also printed)

Same-month ratio (as in analyze.py, same_month): share of CS papers that are strict surveys/position papers in
Nov 2025-Sep 2026 divided by the share in Nov 2024-Sep 2025.

Approximation: the harvest has no monthly total per primary category, so when one category is dropped it is removed
from the strict count (numerator) only. The CS denominator is left unchanged. Standard library only.
"""
import csv, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAB = os.path.join(ROOT, "results", "tables")
OUT = os.path.join(ROOT, "results", "leave_one_category_out.csv")
W0 = ("2024-11", "2025-09")  # baseline window
W1 = ("2025-11", "2026-09")  # post-rule window

with open(os.path.join(TAB, "monthly_series.csv"), newline="") as f:
    series = list(csv.DictReader(f))


def window(w, col):
    return sum(int(r[col]) for r in series if w[0] <= r["month"] <= w[1])


n0, n1 = window(W0, "N_cs_any"), window(W1, "N_cs_any")
y0, y1 = window(W0, "Y_cs_any|strict"), window(W1, "Y_cs_any|strict")

with open(os.path.join(TAB, "placement_primary.csv"), newline="") as f:
    place = list(csv.DictReader(f))
p0 = sum(int(r["Nov2024-Sep2025"]) for r in place)
p1 = sum(int(r["Nov2025-Sep2026"]) for r in place)
assert (p0, p1) == (y0, y1), f"placement totals {p0},{p1} differ from strict counts {y0},{y1}"


def ratio(a0, a1):
    return (a1 / n1) / (a0 / n0)


rows = [("all categories", y0, y1, ratio(y0, y1))]
for r in place:
    if r["primary"] == "other":
        continue
    a0, a1 = y0 - int(r["Nov2024-Sep2025"]), y1 - int(r["Nov2025-Sep2026"])
    rows.append((f"without {r['primary']}", a0, a1, ratio(a0, a1)))

print(f"CS denominators: {n0} (Nov 2024-Sep 2025), {n1} (Nov 2025-Sep 2026), held fixed (approximation).")
with open(OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["case", "strict_Nov2024-Sep2025", "strict_Nov2025-Sep2026", "same_month_ratio"])
    for case, a0, a1, rr in rows:
        w.writerow([case, a0, a1, f"{rr:.3f}"])
        print(f"{case:<20} strict {a0:>5} -> {a1:>5}   ratio {rr:.3f}")
drop = [r[3] for r in rows[1:]]
print(f"Range when dropping one category: {min(drop):.2f}-{max(drop):.2f} (all categories {rows[0][3]:.2f}).")
print("Approximation: the CS denominator is unchanged; no per-category totals exist in the harvest.")
