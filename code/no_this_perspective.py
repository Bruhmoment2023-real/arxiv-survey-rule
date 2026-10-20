"""Strict rule without the "this perspective" cue (sensitivity check, not part of the frozen plan).

Loads the frozen classifier (code/classify.py, rules v1.0) from the path given, and builds a
variant in which the strict abstract-position rule no longer matches "this perspective" or
"in this perspective". Every other rule is unchanged.
Part 1 (hand labels): which labelled strict papers lose the strict flag, and the precision of the
variant on the 100 labelled strict papers by period.
Part 2 (full net): strict CS counts by month under both versions, and the same-month ratio
(Nov 2025-Sep 2026 vs Nov 2024-Sep 2025) with the formula of same_month() in analyze.py, using
the monthly CS totals in results/tables/monthly_series.csv.
Usage: python -I no_this_perspective.py <pack_dir>
"""
import csv, gzip, importlib.util, json, math, os, re, sys, collections

PACK = sys.argv[1]
spec = importlib.util.spec_from_file_location("classify_v1", os.path.join(PACK, "code", "classify.py"))
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
ORIG = C.A_POSITION
VAR = re.compile(r"\b(position|vision|perspective|opinion|viewpoint) (paper|piece|article)\b|"
                 r"\bthis (position|viewpoint|commentary|essay|manifesto|opinion)\b|"
                 r"\bin this (position|viewpoint|commentary|essay)\b|"
                 r"\bthis paper (takes|argues for) the position\b|\bwe take the position\b", re.I)

def strict_both(t, a):
    C.A_POSITION = ORIG; s0 = C.classify(t, a)["strict"]
    C.A_POSITION = VAR;  s1 = C.classify(t, a)["strict"]
    C.A_POSITION = ORIG
    return s0, s1

# ---- Part 1: hand labels
L = os.path.join(PACK, "data", "labels")
key = {r["key"]: r for r in csv.DictReader(open(os.path.join(L, "sample_key.csv"), encoding="utf-8"))}
for r in csv.DictReader(open(os.path.join(L, "labels.csv"), encoding="utf-8")):
    key[r["key"]]["label"] = r["label"]
ids = {r["id"] for r in key.values()}
rec = {}
for line in gzip.open(os.path.join(PACK, "data", "days.jsonl.gz"), "rt", encoding="utf-8"):
    r = json.loads(line)
    if r["id"] in ids:
        rec[r["id"]] = r
print(f"Labelled papers found in days.jsonl.gz: {len(rec)} of {len(ids)}")
pos = {"S", "P"}
stat = collections.Counter()
for k, r in sorted(key.items()):
    if r["id"] not in rec:
        continue
    t, a = rec[r["id"]]["title"], rec[r["id"]]["abstract"]
    s0, s1 = strict_both(t, a)
    if r["stratum"] == "strict" and not s0:
        print(f"  note: {k} is in the strict stratum but v1.0 does not flag it now")
    if s0 and not s1:
        print(f"  loses strict flag: {k} {r['id']} {r['period']} stratum={r['stratum']} label={r['label']} | {t[:80]}")
    if r["stratum"] == "strict":
        p = r["period"]
        stat[(p, "n0")] += s0; stat[(p, "tp0")] += s0 and r["label"] in pos
        stat[(p, "n1")] += s1; stat[(p, "tp1")] += s1 and r["label"] in pos
fp_total = sum(1 for r in key.values() if r["stratum"] == "strict" and r["label"] not in pos)
print(f"Strict false positives among labelled strict papers (label not S or P): {fp_total}")
for p in ("pre", "post"):
    print(f"  {p}: v1.0 precision {stat[(p,'tp0')]}/{stat[(p,'n0')]} = {stat[(p,'tp0')]/stat[(p,'n0')]:.3f}; "
          f"variant {stat[(p,'tp1')]}/{stat[(p,'n1')]} = {stat[(p,'tp1')]/stat[(p,'n1')]:.3f}")

# ---- Part 2: full net, CS papers
cs_ = lambda cats: any(c.startswith("cs.") for c in cats)
Y0, Y1 = collections.Counter(), collections.Counter()
for line in gzip.open(os.path.join(PACK, "data", "net.jsonl.gz"), "rt", encoding="utf-8"):
    r = json.loads(line)
    m = r["published"][:7]
    if not ("2022-01" <= m <= "2026-09") or not cs_(r["cats"]):
        continue
    s0, s1 = strict_both(r["title"], r["abstract"])
    Y0[m] += s0; Y1[m] += s1
N = {r["month"]: int(r["N_cs_any"]) for r in csv.DictReader(open(os.path.join(PACK, "results", "tables", "monthly_series.csv")))}
Yref = {r["month"]: int(r["Y_cs_any|strict"]) for r in csv.DictReader(open(os.path.join(PACK, "results", "tables", "monthly_series.csv")))}
mism = [m for m in N if Y0[m] != Yref[m]]
print(f"\nv1.0 recount matches monthly_series.csv in {len(N) - len(mism)} of {len(N)} months" + (f"; differ: {mism}" if mism else ""))
def rng(a, b): return [m for m in N if a <= m <= b]
def sm(Y, before, after):
    y0, n0 = sum(Y[m] for m in before), sum(N[m] for m in before)
    y1, n1 = sum(Y[m] for m in after), sum(N[m] for m in after)
    r = (y1 / n1) / (y0 / n0); se = math.sqrt(1/y1 - 1/n1 + 1/y0 - 1/n0)
    return f"{r:.3f} ({r*math.exp(-1.96*se):.3f}-{r*math.exp(1.96*se):.3f}); {y0}/{n0} = {100*y0/n0:.2f}% before, {y1}/{n1} = {100*y1/n1:.2f}% after"
B, A = rng("2024-11", "2025-09"), rng("2025-11", "2026-09")
pre, post = rng("2022-01", "2025-10"), A
for lab, Y in (("v1.0", Y0), ("without 'this perspective'", Y1)):
    print(f"{lab}: strict CS pre-period {sum(Y[m] for m in pre)}, post {sum(Y[m] for m in post)}; "
          f"post share {100*sum(Y[m] for m in post)/sum(N[m] for m in post):.2f}%")
    print(f"  same-month ratio {sm(Y, B, A)}")
print(f"Papers that lose the flag: pre-period {sum(Y0[m]-Y1[m] for m in pre)}, post {sum(Y0[m]-Y1[m] for m in post)}")
