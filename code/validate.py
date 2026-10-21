"""Classifier validation against the hand labels.

Inputs : data/labels/sample_key.csv, data/labels/labels.csv, data/labels/strata_sizes.json
Outputs: results/classifier_validation.md, results/classifier_validation.json,
         results/label_disagreements.csv (false positives and false negatives of the strict rule)
         With a labels file as argument (e.g. data/labels/labels_checked.csv) the outputs get the suffix "_checked".

Positive class (main): label S or P.   Sensitivity: M also counted as positive.
Precision: Wilson 95% interval within the sampled stratum.
Recall   : stratified estimate.  For period p,
           TP = N_strict,p * rate(pos | strict,p)
           FN = N_broad_only,p * rate(pos | broad_only,p) + N_neither,p * rate(pos | neither,p)
           recall = TP / (TP + FN); 95% interval from a stratified bootstrap (5,000 resamples).
"""
import csv, json, os, random, math

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = os.path.join(ROOT, "data", "labels")
RES = os.path.join(ROOT, "results")
os.makedirs(RES, exist_ok=True)
B = 5000
random.seed(20251031)


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"),) * 3
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0, c - h), min(1, c + h)


def load(labels=None):
    key = {r["key"]: r for r in csv.DictReader(open(os.path.join(L, "sample_key.csv"), encoding="utf-8"))}
    for r in csv.DictReader(open(labels or os.path.join(L, "labels.csv"), encoding="utf-8")):
        key[r["key"]]["label"] = r["label"]
        key[r["key"]]["note"] = r["note"]
    sizes = json.load(open(os.path.join(L, "strata_sizes.json")))
    return list(key.values()), sizes


def est(rows, sizes, periods, pos, measure):
    """Return precision/recall point estimates for `measure` in ('strict','broad')."""
    tp = fp = fn = 0.0
    for p in periods:
        for s in ("strict", "broad_only", "neither"):
            sub = [r for r in rows if r["period"] == p and r["stratum"] == s]
            if not sub:
                continue
            rate = sum(r["label"] in pos for r in sub) / len(sub)
            n = sizes[f"{s}|{p}"]
            flagged = (s == "strict") or (measure == "broad" and s == "broad_only")
            if flagged:
                tp += n * rate
                fp += n * (1 - rate)
            else:
                fn += n * rate
    prec = tp / (tp + fp) if tp + fp else float("nan")
    rec = tp / (tp + fn) if tp + fn else float("nan")
    prev = (tp + fn) / sum(sizes[f"{s}|{p}"] for p in periods for s in ("strict", "broad_only", "neither"))
    return prec, rec, prev


def boot(rows, sizes, periods, pos, measure):
    strata = {}
    for r in rows:
        strata.setdefault((r["stratum"], r["period"]), []).append(r)
    out = []
    for _ in range(B):
        samp = []
        for k, v in strata.items():
            samp += random.choices(v, k=len(v))
        out.append(est(samp, sizes, periods, pos, measure))
    res = []
    for j in range(3):
        xs = sorted(x[j] for x in out if not math.isnan(x[j]))
        res.append((xs[int(0.025 * len(xs))], xs[int(0.975 * len(xs)) - 1]))
    return res, out


def main(labels=None, suffix=""):
    rows, sizes = load(labels)
    md = ["# Classifier validation (rules v1.0 against 400 hand labels)", "",
          (f"Labels: {os.path.basename(labels)} (first-pass labels after the author's non-blind check; see checks/). "
           if labels else "") +
          "Labeller: AI assistant, first pass, blind to id, date, category and classifier output. "
          "A human second labeller is still needed (see 00-STATUS.md).", "",
          f"Population stratum sizes (CS papers on the 57 random days): `{json.dumps(sizes)}`", ""]
    js = {}
    for posname, pos in (("main: S or P", ("S", "P")), ("sensitivity: S, P or M", ("S", "P", "M"))):
        md += [f"## Positive class = {posname}", "",
               "### Raw counts in each sampled stratum", "",
               "| stratum | period | labelled | positive | share positive (Wilson 95%) |", "|---|---|---|---|---|"]
        for s in ("strict", "broad_only", "neither"):
            for p in ("pre", "post"):
                sub = [r for r in rows if r["period"] == p and r["stratum"] == s]
                k = sum(r["label"] in pos for r in sub)
                pr, lo, hi = wilson(k, len(sub))
                md.append(f"| {s} | {p} | {len(sub)} | {k} | {pr:.3f} ({lo:.3f}-{hi:.3f}) |")
        md += ["", "### Precision, recall and prevalence (stratum-weighted; bootstrap 95% intervals)", "",
               "| measure | period | precision | recall | true prevalence of S/P among CS papers |", "|---|---|---|---|---|"]
        for measure in ("strict", "broad"):
            keep = {}
            for name, periods in (("pre", ["pre"]), ("post", ["post"]), ("pooled", ["pre", "post"])):
                e = est(rows, sizes, periods, pos, measure)
                ci, draws = boot(rows, sizes, periods, pos, measure)
                keep[name] = draws
                js[f"{posname}|{measure}|{name}"] = {"precision": e[0], "recall": e[1], "prevalence": e[2],
                                                     "ci_precision": ci[0], "ci_recall": ci[1], "ci_prevalence": ci[2]}
                md.append(f"| {measure} | {name} | {e[0]:.3f} ({ci[0][0]:.3f}-{ci[0][1]:.3f}) | "
                          f"{e[1]:.3f} ({ci[1][0]:.3f}-{ci[1][1]:.3f}) | {e[2]:.4f} ({ci[2][0]:.4f}-{ci[2][1]:.4f}) |")
            # pre-post differences (independent bootstrap draws)
            for j, nm in ((0, "precision"), (1, "recall")):
                d = sorted(b[j] - a[j] for a, b in zip(keep["pre"], keep["post"])
                           if not (math.isnan(a[j]) or math.isnan(b[j])))
                pt = est(rows, sizes, ["post"], pos, measure)[j] - est(rows, sizes, ["pre"], pos, measure)[j]
                lo, hi = d[int(0.025 * len(d))], d[int(0.975 * len(d)) - 1]
                js[f"{posname}|{measure}|post-minus-pre {nm}"] = {"diff": pt, "ci": (lo, hi)}
                md.append(f"| {measure} | post minus pre, {nm} | {pt:+.3f} ({lo:+.3f} to {hi:+.3f}) | | |")
        md.append("")
    # among true positives, how were they caught
    md += ["## How hand-labelled S/P papers were caught (unweighted sample counts)", "",
           "| period | stratum | true S | true P |", "|---|---|---|---|"]
    for p in ("pre", "post"):
        for s in ("strict", "broad_only", "neither"):
            sub = [r for r in rows if r["period"] == p and r["stratum"] == s]
            md.append(f"| {p} | {s} | {sum(r['label'] == 'S' for r in sub)} | {sum(r['label'] == 'P' for r in sub)} |")
    md.append("")
    with open(os.path.join(RES, f"label_disagreements{suffix}.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["key", "id", "period", "stratum", "rules", "label", "type", "note"])
        for r in rows:
            pos = r["label"] in ("S", "P")
            if r["stratum"] == "strict" and not pos:
                w.writerow([r["key"], r["id"], r["period"], r["stratum"], r["rules"], r["label"], "strict false positive", r["note"]])
            if r["stratum"] != "strict" and pos:
                w.writerow([r["key"], r["id"], r["period"], r["stratum"], r["rules"], r["label"], "strict miss", r["note"]])
    open(os.path.join(RES, f"classifier_validation{suffix}.md"), "w", encoding="utf-8").write("\n".join(md))
    json.dump(js, open(os.path.join(RES, f"classifier_validation{suffix}.json"), "w"), indent=1)
    print("\n".join(md))


if __name__ == "__main__":
    # python code/validate.py                      -> first-pass labels (data/labels/labels.csv)
    # python code/validate.py data/labels/labels_checked.csv  -> results/classifier_validation_checked.*
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1], "_checked")
    else:
        main()
