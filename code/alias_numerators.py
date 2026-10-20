"""How many strict-rule papers are missing from the CS numerators because they are listed only
through the alias categories (cs.SY stored as eess.SY, cs.NA stored as math.NA) with no cs.* label.

eess.* is inside the study group, so the strict rule (title and abstract) can be applied to
eess.SY papers. math.NA is outside it, so only the title-only rule is available there.
Counts are compared with the strict and title-only CS counts in results/tables/monthly_series.csv.
Usage: python -I alias_numerators.py <pack_dir>
"""
import csv, gzip, importlib.util, json, os, sys, collections

PACK = sys.argv[1]
spec = importlib.util.spec_from_file_location("classify_v1", os.path.join(PACK, "code", "classify.py"))
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
per = lambda m: "pre" if m <= "2025-10" else "post"
same = lambda m: "Nov24-Sep25" if "2024-11" <= m <= "2025-09" else "Nov25-Sep26" if "2025-11" <= m <= "2026-09" else None
cnt = collections.Counter()
for line in gzip.open(os.path.join(PACK, "data", "net.jsonl.gz"), "rt", encoding="utf-8"):
    r = json.loads(line)
    m = r["published"][:7]
    if not ("2022-01" <= m <= "2026-09") or any(c.startswith("cs.") for c in r["cats"]):
        continue
    sy, na = "eess.SY" in r["cats"], "math.NA" in r["cats"]
    if not (sy or na):
        continue
    if sy and C.classify(r["title"], r["abstract"])["strict"]:
        for k in (per(m), same(m)):
            if k: cnt[("eess.SY strict", k)] += 1
    if (sy or na) and C.title_only(r["title"]):
        for k in (per(m), same(m)):
            if k: cnt[("alias title-only", k)] += 1
ms = list(csv.DictReader(open(os.path.join(PACK, "results", "tables", "monthly_series.csv"))))
cs = collections.Counter()
for r in ms:
    for k in (per(r["month"]), same(r["month"])):
        if k:
            cs[("strict", k)] += int(r["Y_cs_any|strict"]); cs[("title", k)] += int(r["Y_cs_any|title"])
for k in ("pre", "post", "Nov24-Sep25", "Nov25-Sep26"):
    a, b = cnt[("eess.SY strict", k)], cs[("strict", k)]
    c, d = cnt[("alias title-only", k)], cs[("title", k)]
    print(f"{k}: alias-only eess.SY strict {a} vs CS strict {b} ({100*a/b:.1f}% of CS strict); "
          f"alias-only title-only (eess.SY or math.NA) {c} vs CS title-only {d} ({100*c/d:.1f}%)")
