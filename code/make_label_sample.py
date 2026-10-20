"""Draw the stratified hand-labelling sample from the random-day data (data/days.jsonl.gz).

Population: papers with at least one cs.* category on the 57 random sample days.
Strata: classifier output (strict / broad-only / neither) x period (pre / post policy).
Sizes are fixed below. The labelling sheet is shuffled and shows ONLY title + abstract
(abstracts longer than 720 characters are shown as first 500 + last 200 characters)
(no id, date, category or classifier output) so that labels are blind to period and to the rules.

Outputs:
  data/labels/sample_key.csv        key, id, period, stratum, rules   (not looked at while labelling)
  data/labels/sheet_partNN.txt      blind labelling sheets (50 items each)
  data/labels/strata_sizes.json     population size of every stratum (weights for recall)
"""
import gzip, json, os, random, csv, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from classify import classify

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POLICY = "2025-11-01"          # first full day after the 31 Oct 2025 announcement
N = {("strict", "pre"): 50, ("strict", "post"): 50,
     ("broad_only", "pre"): 40, ("broad_only", "post"): 40,
     ("neither", "pre"): 110, ("neither", "post"): 110}
SEED = 20251031


def main():
    rng = random.Random(SEED)
    pop = {k: [] for k in N}
    for line in gzip.open(os.path.join(ROOT, "data", "days.jsonl.gz"), "rt", encoding="utf-8"):
        r = json.loads(line)
        if not any(c.startswith("cs.") for c in r["cats"]):
            continue
        c = classify(r["title"], r["abstract"])
        s = "strict" if c["strict"] else "broad_only" if c["broad"] else "neither"
        p = "post" if r["published"] >= POLICY else "pre"
        r["_rules"] = "+".join(c["rules"])
        pop[(s, p)].append(r)
    out = os.path.join(ROOT, "data", "labels")
    os.makedirs(out, exist_ok=True)
    json.dump({f"{s}|{p}": len(v) for (s, p), v in pop.items()},
              open(os.path.join(out, "strata_sizes.json"), "w"), indent=1)
    items = []
    for k, n in N.items():
        v = sorted(pop[k], key=lambda r: r["id"])
        for r in rng.sample(v, n):
            items.append((k, r))
    rng.shuffle(items)
    with open(os.path.join(out, "sample_key.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["key", "id", "period", "stratum", "rules", "published", "primary"])
        for i, ((s, p), r) in enumerate(items, 1):
            w.writerow([f"L{i:03d}", r["id"], p, s, r["_rules"], r["published"], r["primary"]])
    for part in range(0, len(items), 50):
        with open(os.path.join(out, f"sheet_part{part // 50 + 1:02d}.txt"), "w", encoding="utf-8") as f:
            for i, (_, r) in enumerate(items[part:part + 50], part + 1):
                a = r["abstract"]
                if len(a) > 720:      # excerpt: opening 500 characters + closing 200 characters
                    a = a[:500] + " [...] " + a[-200:]
                f.write(f"L{i:03d} | {r['title']}\n{a}\n\n")
    print({f"{s}|{p}": len(v) for (s, p), v in pop.items()}, len(items), "items")


if __name__ == "__main__":
    main()
