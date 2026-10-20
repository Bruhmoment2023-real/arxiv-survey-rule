"""Check that the candidate net (data/net.jsonl.gz) is a superset of what the classifier fires on.

For every paper in the random-day data (data/days.jsonl.gz, which holds ALL papers of group G on
57 days) that the classifier marks strict or broad, test whether the same paper is in the net.
Only months whose net slices are complete (a .done file exists) are checked.
Also reports the title-only rule. Output: results/net_coverage.md
"""
import gzip, json, os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from classify import classify, title_only

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    done = set()
    for p in glob.glob(os.path.join(ROOT, "data", "raw", "net", "*.done.xml.gz")):
        b = os.path.basename(p).split("_")[1].split(".")[0]          # 20251001-07
        ym, rng = b[:6], b[6:]
        d1, d2 = int(rng.split("-")[0]), int(rng.split("-")[1])
        for d in range(d1, d2 + 1):
            done.add(f"{ym[:4]}-{ym[4:]}-{d:02d}")
    net = set()
    for line in gzip.open(os.path.join(ROOT, "data", "net.jsonl.gz"), "rt", encoding="utf-8"):
        net.add(json.loads(line)["id"])
    tot = {"strict": [0, 0], "broad_only": [0, 0], "title_only": [0, 0]}
    missed = []
    days = set()
    for line in gzip.open(os.path.join(ROOT, "data", "days.jsonl.gz"), "rt", encoding="utf-8"):
        r = json.loads(line)
        day = r["published"][:10]
        if day not in done:
            continue
        days.add(day)
        c = classify(r["title"], r["abstract"])
        kinds = []
        if c["strict"]:
            kinds.append("strict")
        elif c["broad"]:
            kinds.append("broad_only")
        if title_only(r["title"]):
            kinds.append("title_only")
        for k in kinds:
            tot[k][0] += 1
            if r["id"] in net:
                tot[k][1] += 1
            else:
                missed.append((k, r["id"], "+".join(c["rules"]), r["title"][:90]))
    out = ["# Net coverage check", "",
           f"Sample days with a completed net slice: {len(days)} of 57.", "",
           "| classifier output | papers on those days (group G) | found in the net | coverage |", "|---|---|---|---|"]
    for k, (n, f) in tot.items():
        out.append(f"| {k} | {n} | {f} | {100 * f / n:.2f}% |" if n else f"| {k} | 0 | 0 | - |")
    out += ["", "## Classifier-positive papers missing from the net", ""]
    out += [f"- {k} | {i} | {ru} | {t}" for k, i, ru, t in missed[:80]] or ["- none"]
    open(os.path.join(ROOT, "results", "net_coverage.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("\n".join(out[:12]), "\nmissing:", len(missed))


if __name__ == "__main__":
    main()
