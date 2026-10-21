"""Precision/recall-corrected same-month ratio (Section 3.4 of the paper).

If the strict share = true prevalence x recall / precision, the true ratio is
    observed same-month ratio x (precision_post / recall_post) / (precision_pre / recall_pre).
The interval comes from a stratified bootstrap of the hand labels (validate.py's est/boot, 5,000 resamples per
period, seed 20251031) with the same-month ratio's own uncertainty added (log-normal, from its 95% interval).

Run:  python code/corrected_ratio.py [labels.csv]      (default data/labels/labels.csv; output to stdout)
"""
import math, os, random, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import validate

RATIO, LO, HI = 0.609, 0.582, 0.637          # strict same-month ratio (analysis_output.md)


def main():
    lab = sys.argv[1] if len(sys.argv) > 1 else None
    rows, sizes = validate.load(lab)
    pos = ("S", "P")
    pre = validate.est(rows, sizes, ["pre"], pos, "strict")
    post = validate.est(rows, sizes, ["post"], pos, "strict")
    factor = (post[0] / post[1]) / (pre[0] / pre[1])
    print(f"labels: {lab or 'data/labels/labels.csv'}")
    print(f"strict precision pre {pre[0]:.3f}, post {post[0]:.3f}; recall pre {pre[1]:.3f}, post {post[1]:.3f}")
    print(f"true prevalence pre {pre[2]:.4f}, post {post[2]:.4f}; prevalence ratio {post[2] / pre[2]:.3f}")
    print(f"correction factor {factor:.3f}; corrected ratio {RATIO * factor:.3f}")
    random.seed(20251031)
    _, dpre = validate.boot(rows, sizes, ["pre"], pos, "strict")
    _, dpost = validate.boot(rows, sizes, ["post"], pos, "strict")
    se = (math.log(HI) - math.log(LO)) / (2 * 1.96)
    rnd = random.Random(20261021)
    fs, cs, pr = [], [], []
    for a, b in zip(dpre, dpost):
        if min(a[0], a[1], b[0], b[1]) <= 0 or any(math.isnan(x) for x in a + b):
            continue
        f = (b[0] / b[1]) / (a[0] / a[1])
        fs.append(f)
        cs.append(math.exp(rnd.gauss(math.log(RATIO), se)) * f)
        pr.append(b[2] / a[2])
    cs.sort(); pr.sort()
    q = lambda xs, p: xs[int(p * len(xs)) - (1 if p > 0.5 else 0)]
    print(f"bootstrap draws used: {len(cs)}")
    print(f"corrected ratio 95% interval: {q(cs, 0.025):.2f} to {q(cs, 0.975):.2f}")
    print(f"prevalence ratio 95% interval: {q(pr, 0.025):.2f} to {q(pr, 0.975):.2f}")
    print(f"share of draws with factor > 1: {sum(f > 1 for f in fs) / len(fs):.0%}")


if __name__ == "__main__":
    main()
