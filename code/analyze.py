"""Analysis exactly as fixed in 03-design.md (section 6). Run with the project venv:

    .venv\\Scripts\\python code\\analyze.py

Inputs : data/net.jsonl.gz (candidate net, parsed), data/counts_core.json (monthly denominators)
Outputs: results/tables/*.csv, results/figures/*.png, results/analysis_output.md
"""
import gzip, json, os, sys, math, csv, collections, re
import numpy as np
import statsmodels.api as sm
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from classify import classify, title_only

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "results")
TAB = os.path.join(RES, "tables")
FIG = os.path.join(RES, "figures")
for d in (TAB, FIG):
    os.makedirs(d, exist_ok=True)

START, END = "2022-01", "2026-09"
FIRST_POST = "2025-11"
PHYS = ("astro-ph.", "cond-mat.")
PHYS_EXACT = {"hep-th", "hep-ph", "quant-ph", "gr-qc"}
SPILL = ["stat_notcs", "eess_notcs", "qbio_notcs", "econ_notcs", "qfin_notcs", "socph_notcs"]
C = {"blue": "#2a78d6", "orange": "#eb6834", "aqua": "#1baf7a", "yellow": "#eda100",
     "magenta": "#e87ba4", "green": "#008300", "violet": "#6250d6", "ink": "#0b0b0b", "muted": "#52514e"}
ACCEPT = re.compile(r"\b(accepted|published|to appear|in press|camera[- ]ready|forthcoming)\b", re.I)
rng = np.random.default_rng(20251031)
OUT = []


def say(s=""):
    OUT.append(s)
    print(s)


def month_list():
    y, m = map(int, START.split("-"))
    out = []
    while f"{y}-{m:02d}" <= END:
        out.append(f"{y}-{m:02d}")
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


MONTHS = month_list()
IDX = {m: i for i, m in enumerate(MONTHS)}
T0 = IDX[FIRST_POST]
NPRE, NPOST = T0, len(MONTHS) - T0


def groups_of(cats):
    cs = any(c.startswith("cs.") for c in cats)
    g = set()
    if cs:
        g.add("cs_any")
        return g
    if any(c.startswith("stat.") for c in cats): g.add("stat_notcs")
    if any(c.startswith("eess.") for c in cats): g.add("eess_notcs")
    if any(c.startswith("q-bio.") for c in cats): g.add("qbio_notcs")
    if any(c.startswith("econ.") for c in cats): g.add("econ_notcs")
    if any(c.startswith("q-fin.") for c in cats): g.add("qfin_notcs")
    if "physics.soc-ph" in cats: g.add("socph_notcs")
    if any(c.startswith("math.") for c in cats): g.add("math_notcs")
    if any(c.startswith(PHYS) or c in PHYS_EXACT for c in cats): g.add("phys_notcs")
    return g


def load():
    den = json.load(open(os.path.join(ROOT, "data", "counts_core.json")))
    N = collections.defaultdict(lambda: np.zeros(len(MONTHS)))
    for k, v in den.items():
        g, m = k.split("|")
        if m in IDX:
            N[g][IDX[m]] = v
    Y = collections.defaultdict(lambda: np.zeros(len(MONTHS)))
    cs_recs = []
    n = 0
    for line in gzip.open(os.path.join(ROOT, "data", "net.jsonl.gz"), "rt", encoding="utf-8"):
        r = json.loads(line)
        m = r["published"][:7]
        if m not in IDX:
            continue
        n += 1
        i = IDX[m]
        gs = groups_of(r["cats"])
        c = classify(r["title"], r["abstract"])
        to = title_only(r["title"])
        in_G = "cs_any" in gs or any(g in gs for g in SPILL)
        for g in gs:
            if to:
                Y[g + "|title"][i] += 1
            if g == "cs_any" or g in SPILL:
                if c["strict"]:
                    Y[g + "|strict"][i] += 1
                if c["broad"]:
                    Y[g + "|broad"][i] += 1
                if c["broad"] and not c["strict"]:
                    Y[g + "|broad_only"][i] += 1
                if c["kind"] in ("survey", "both"):
                    Y[g + "|survey"][i] += 1
                if c["kind"] in ("position", "both"):
                    Y[g + "|position"][i] += 1
        if in_G and "cs_any" not in gs:
            if c["strict"]:
                Y["spill_pooled|strict"][i] += 1          # a paper in two spill groups counted once
        if "cs_any" in gs and c["strict"]:
            if r["primary"].startswith("cs."):
                Y["cs_any|strict_csprimary"][i] += 1
            else:
                Y["cs_any|strict_noncsprimary"][i] += 1
            cs_recs.append({"m": m, "primary": r["primary"], "kind": c["kind"],
                            "jr": bool(r["journal_ref"]), "doi": bool(r["doi"]),
                            "acc": bool(ACCEPT.search(r["comment"] or "")), "v": r["v"]})
    N["spill_pooled"] = sum(N[g] for g in SPILL)     # approximation: ignores papers in two spill groups
    say(f"- Net records inside the window: {n:,}; strict-positive CS papers: {len(cs_recs):,}")
    return N, Y, cs_recs


def design(idx, with_post=True):
    t = np.asarray(idx, float)
    cols = [np.ones_like(t), t / 12.0]
    names = ["const", "trend_per_year"]
    if with_post:
        post = (t >= T0).astype(float)
        cols += [post, post * (t - T0) / 12.0]
        names += ["level_change", "slope_change_per_year"]
    for k in (1, 2):
        cols += [np.sin(2 * np.pi * k * t / 12), np.cos(2 * np.pi * k * t / 12)]
        names += [f"sin{k}", f"cos{k}"]
    return np.column_stack(cols), names


def its(y, n, label, drop=()):
    """Segmented quasi-Poisson regression with offset and HAC(3) errors + counterfactual ratio."""
    keep = np.array([i for i in range(len(MONTHS)) if MONTHS[i] not in drop and n[i] > 0])
    X, names = design(keep)
    fit = sm.GLM(y[keep], X, family=sm.families.Poisson(), offset=np.log(n[keep])).fit(
        cov_type="HAC", cov_kwds={"maxlags": 3})
    b, se = fit.params, fit.bse
    disp = float(np.sum((y[keep] - fit.fittedvalues) ** 2 / fit.fittedvalues) / (len(keep) - X.shape[1]))
    lvl = (math.exp(b[2]), math.exp(b[2] - 1.96 * se[2]), math.exp(b[2] + 1.96 * se[2]))
    # counterfactual from the pre-period only
    pre = keep[keep < T0]
    post = keep[keep >= T0]
    Xp, _ = design(pre, with_post=False)
    f0 = sm.GLM(y[pre], Xp, family=sm.families.Poisson(), offset=np.log(n[pre])).fit(
        cov_type="HAC", cov_kwds={"maxlags": 3})
    Xq, _ = design(post, with_post=False)
    pred = np.exp(Xq @ f0.params) * n[post]
    draws = rng.multivariate_normal(f0.params, f0.cov_params(), size=5000)
    sims = np.exp(draws @ Xq.T) * n[post]
    ratios = y[post].sum() / sims.sum(axis=1)
    cf = (y[post].sum() / pred.sum(), float(np.quantile(ratios, 0.025)), float(np.quantile(ratios, 0.975)))
    allpost = np.arange(T0, len(MONTHS))
    Xa, _ = design(allpost, with_post=False)
    cf_share = np.exp(Xa @ f0.params)
    cf_lo = np.quantile(np.exp(draws @ Xa.T), 0.025, axis=0)
    cf_hi = np.quantile(np.exp(draws @ Xa.T), 0.975, axis=0)
    return {"label": label, "level": lvl, "level_p": float(fit.pvalues[2]),
            "slope": (b[3], b[3] - 1.96 * se[3], b[3] + 1.96 * se[3]), "trend": (b[1], se[1]),
            "dispersion": disp, "cf": cf, "obs_post": float(y[post].sum()), "pred_post": float(pred.sum()),
            "cf_share": cf_share, "cf_lo": cf_lo, "cf_hi": cf_hi, "n_months": len(keep)}


def same_month(y, n):
    """Nov 2025-Sep 2026 versus Nov 2024-Sep 2025: ratio of shares, normal-approx CI on the log scale
    (binomial variance inflated by nothing; reported as a descriptive figure)."""
    a = slice(IDX["2024-11"], IDX["2025-09"] + 1)
    b = slice(IDX["2025-11"], IDX["2026-09"] + 1)
    y0, n0, y1, n1 = y[a].sum(), n[a].sum(), y[b].sum(), n[b].sum()
    if min(y0, y1) == 0:
        return (float("nan"),) * 3 + (y0, n0, y1, n1)
    r = (y1 / n1) / (y0 / n0)
    se = math.sqrt(1 / y1 - 1 / n1 + 1 / y0 - 1 / n0)
    return r, r * math.exp(-1.96 * se), r * math.exp(1.96 * se), y0, n0, y1, n1


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"),) * 3
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0, c - h), min(1, c + h)


def style(ax, title, ylabel):
    ax.set_title(title, loc="left", fontsize=11, color=C["ink"])
    ax.set_ylabel(ylabel, fontsize=9, color=C["muted"])
    ax.grid(axis="y", color="#e4e3df", linewidth=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#b9b8b2")
    ax.tick_params(colors=C["muted"], labelsize=8)
    ticks = [i for i, m in enumerate(MONTHS) if m.endswith("-01")]
    ax.set_xticks(ticks)
    ax.set_xticklabels([MONTHS[i][:4] for i in ticks])
    ax.axvline(T0 - 0.5, color=C["muted"], linewidth=0.9, linestyle=(0, (4, 3)))
    ax.set_ylim(bottom=0)


def mark_rule(ax):
    ax.annotate("rule announced\n31 Oct 2025", xy=(T0 - 0.5, ax.get_ylim()[1]), xytext=(-4, -4),
                textcoords="offset points", ha="right", va="top", fontsize=8, color=C["muted"])


def fig_spillover(x, Y, N):
    """Spill-over groups figure, sized for print at the paper's text width (6.5 in): all text 8 pt or larger."""
    fig, axes = plt.subplots(2, 3, figsize=(6.5, 4.4), dpi=300, sharex=True)
    nice = {"stat_notcs": "stat", "eess_notcs": "eess", "qbio_notcs": "q-bio", "econ_notcs": "econ",
            "qfin_notcs": "q-fin", "socph_notcs": "physics.soc-ph"}
    for ax, g in zip(axes.ravel(), SPILL):
        s_ = 100 * Y[g + "|strict"] / N[g]
        k = np.convolve(s_, np.ones(3) / 3, mode="same")
        ax.plot(x, s_, color=C["blue"], linewidth=0.6, alpha=0.45)
        ax.plot(x[1:-1], k[1:-1], color=C["blue"], linewidth=1.5)
        style(ax, f"{nice[g]} (no CS listing)", "% strict")
        ax.set_title(f"{nice[g]} (no CS listing)", loc="left", fontsize=8.5, color=C["ink"], x=-0.16)
        ax.yaxis.label.set_fontsize(8.5)
        ax.tick_params(labelsize=8)
    fig.suptitle("Spill-over groups: strict survey/position share (thin = monthly, thick = 3-month mean)", fontsize=9, x=0.01, ha="left")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig4_spillover_shares.png")); plt.close(fig)


def main():
    say("# Analysis output (generated by code/analyze.py)")
    say()
    N, Y, cs_recs = load()
    x = np.arange(len(MONTHS))
    say(f"- Months: {MONTHS[0]} to {MONTHS[-1]} ({NPRE} pre, {NPOST} post). First post month: {FIRST_POST}.")
    miss = [g for g in ["cs_any"] + SPILL + ["math_notcs", "phys_notcs"] if (N[g] == 0).any()]
    if miss:
        say(f"- WARNING: denominators missing for some months in: {miss}")

    # ---------- monthly table
    with open(os.path.join(TAB, "monthly_series.csv"), "w", newline="") as f:
        cols = ["cs_any|strict", "cs_any|survey", "cs_any|position", "cs_any|broad", "cs_any|broad_only",
                "cs_any|strict_csprimary", "cs_any|strict_noncsprimary", "cs_any|title",
                "math_notcs|title", "phys_notcs|title", "spill_pooled|strict"] + [g + "|strict" for g in SPILL]
        dens = ["cs_any", "math_notcs", "phys_notcs", "spill_pooled"] + SPILL
        w = csv.writer(f)
        w.writerow(["month"] + ["N_" + d for d in dens] + ["Y_" + c for c in cols])
        for i, m in enumerate(MONTHS):
            w.writerow([m] + [int(N[d][i]) for d in dens] + [int(Y[c][i]) for c in cols])

    # ---------- RQ1
    say()
    say("## RQ1. Strict survey/position share in CS")
    y, n = Y["cs_any|strict"], N["cs_any"]
    share = y / n
    for lab, sl in (("2022", slice(0, 12)), ("2023", slice(12, 24)), ("2024", slice(24, 36)),
                    ("2025 Jan-Oct", slice(36, 46)), ("post (Nov 2025-Sep 2026)", slice(T0, None))):
        say(f"- {lab}: {int(y[sl].sum()):,} strict of {int(n[sl].sum()):,} CS papers = {100 * y[sl].sum() / n[sl].sum():.2f}%")
    rows = []
    specs = [("cs strict (PRIMARY)", Y["cs_any|strict"], N["cs_any"], ()),
             ("cs strict, wash-out (drop Oct+Nov 2025)", Y["cs_any|strict"], N["cs_any"], ("2025-10", "2025-11")),
             ("cs survey-kind only", Y["cs_any|survey"], N["cs_any"], ()),
             ("cs position-kind only", Y["cs_any|position"], N["cs_any"], ()),
             ("cs broad", Y["cs_any|broad"], N["cs_any"], ()),
             ("cs broad-only (relabelling test)", Y["cs_any|broad_only"], N["cs_any"], ()),
             ("cs strict, CS-primary numerators", Y["cs_any|strict_csprimary"], N["cs_any"], ()),
             ("cs strict, non-CS-primary numerators", Y["cs_any|strict_noncsprimary"], N["cs_any"], ()),
             ("cs title-only rule", Y["cs_any|title"], N["cs_any"], ()),
             ("CONTROL math (no cs) title-only", Y["math_notcs|title"], N["math_notcs"], ()),
             ("CONTROL physics group (no cs) title-only", Y["phys_notcs|title"], N["phys_notcs"], ()),
             ("SPILL pooled (no cs) strict", Y["spill_pooled|strict"], N["spill_pooled"], ())]
    specs += [(f"SPILL {g} strict", Y[g + "|strict"], N[g], ()) for g in SPILL]
    R = {}
    for lab, yy, nn, drop in specs:
        r = its(yy, nn, lab, drop)
        sm_ = same_month(yy, nn)
        R[lab] = (r, sm_)
        rows.append([lab, int(yy[:T0].sum()), int(yy[T0:].sum()),
                     f"{r['level'][0]:.3f}", f"{r['level'][1]:.3f}", f"{r['level'][2]:.3f}", f"{r['level_p']:.4f}",
                     f"{r['cf'][0]:.3f}", f"{r['cf'][1]:.3f}", f"{r['cf'][2]:.3f}",
                     f"{sm_[0]:.3f}", f"{sm_[1]:.3f}", f"{sm_[2]:.3f}",
                     f"{r['slope'][0]:.3f}", f"{r['trend'][0]:.3f}", f"{r['dispersion']:.2f}"])
    hdr = ["series", "Y_pre", "Y_post", "level_ratio", "lo", "hi", "p", "obs/counterfactual", "lo", "hi",
           "same-month share ratio", "lo", "hi", "slope_change(log/yr)", "pre_trend(log/yr)", "dispersion"]
    with open(os.path.join(TAB, "its_results.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(hdr)
        w.writerows(rows)
    say()
    say("| " + " | ".join(hdr) + " |")
    say("|" + "---|" * len(hdr))
    for r in rows:
        say("| " + " | ".join(str(v) for v in r) + " |")
    say()
    say("Reading guide: level_ratio = exp(b2), the step at Nov 2025 in the segmented model; "
        "obs/counterfactual = observed post-period count divided by the count predicted from the pre-period "
        "trend and season; same-month share ratio = Nov 2025-Sep 2026 share divided by Nov 2024-Sep 2025 share. "
        "Dispersion > 1 means more month-to-month noise than a Poisson model expects.")

    # ratio of ratios vs controls
    say()
    say("## Controlled comparison (title-only rule everywhere)")
    cs_t = R["cs title-only rule"]
    for ctl in ("CONTROL math (no cs) title-only", "CONTROL physics group (no cs) title-only"):
        c_ = R[ctl]
        for nm, j in (("level ratio", "level"), ("obs/counterfactual", "cf")):
            a, b = cs_t[0][j], c_[0][j]
            se = math.sqrt(((math.log(a[2]) - math.log(a[1])) / 3.92) ** 2 + ((math.log(b[2]) - math.log(b[1])) / 3.92) ** 2)
            rr = a[0] / b[0]
            say(f"- CS / {ctl}, {nm}: ratio of ratios {rr:.3f} (95% {rr * math.exp(-1.96 * se):.3f}-{rr * math.exp(1.96 * se):.3f})")
        a, b = cs_t[1], c_[1]
        se = math.sqrt(((math.log(a[2]) - math.log(a[1])) / 3.92) ** 2 + ((math.log(b[2]) - math.log(b[1])) / 3.92) ** 2)
        rr = a[0] / b[0]
        say(f"- CS / {ctl}, same-month share ratio: ratio of ratios {rr:.3f} (95% {rr * math.exp(-1.96 * se):.3f}-{rr * math.exp(1.96 * se):.3f})")

    # displacement counts
    say()
    say("## Displacement in counts")
    p = R["cs strict (PRIMARY)"][0]
    s = R["SPILL pooled (no cs) strict"][0]
    deficit = p["pred_post"] - p["obs_post"]
    excess = s["obs_post"] - s["pred_post"]
    say(f"- CS: predicted {p['pred_post']:.0f} strict papers in the post period, observed {p['obs_post']:.0f}; deficit {deficit:.0f}.")
    say(f"- Pooled spill-over (no CS listing): predicted {s['pred_post']:.0f}, observed {s['obs_post']:.0f}; excess {excess:.0f}.")
    if deficit > 0:
        say(f"- Displaced fraction (excess / deficit): {excess / deficit:.3f} (point estimate only; both terms are model-based).")
    nc = R["cs strict, non-CS-primary numerators"][0]
    say(f"- CS-listed strict papers with a non-CS primary: predicted {nc['pred_post']:.0f}, observed {nc['obs_post']:.0f}.")

    # ---------- placement inside CS
    say()
    say("## Placement of strict CS papers by primary category (same calendar months)")
    wa = [r for r in cs_recs if "2024-11" <= r["m"] <= "2025-09"]
    wb = [r for r in cs_recs if "2025-11" <= r["m"] <= "2026-09"]
    ca, cb = collections.Counter(r["primary"] for r in wa), collections.Counter(r["primary"] for r in wb)
    top = [c for c, _ in (ca + cb).most_common(14)]
    tab = [[c, ca[c], cb[c]] for c in top] + [["other", sum(v for k, v in ca.items() if k not in top),
                                               sum(v for k, v in cb.items() if k not in top)]]
    chi = stats.chi2_contingency(np.array([[r[1], r[2]] for r in tab]).T)
    with open(os.path.join(TAB, "placement_primary.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["primary", "Nov2024-Sep2025", "share", "Nov2025-Sep2026", "share"])
        for c, a, b in tab:
            w.writerow([c, a, f"{a / len(wa):.4f}", b, f"{b / max(1, len(wb)):.4f}"])
    say(f"- Strict CS papers: {len(wa):,} in Nov 2024-Sep 2025, {len(wb):,} in Nov 2025-Sep 2026.")
    say("| primary | before | share | after | share |")
    say("|---|---|---|---|---|")
    for c, a, b in tab:
        say(f"| {c} | {a} | {100 * a / len(wa):.1f}% | {b} | {100 * b / max(1, len(wb)):.1f}% |")
    say(f"- Chi-square test of equal category mix: chi2 = {chi[0]:.1f}, df = {chi[2]}, p = {chi[1]:.2g}.")
    na, nb = sum(not r["primary"].startswith("cs.") for r in wa), sum(not r["primary"].startswith("cs.") for r in wb)
    pa, pb = wilson(na, len(wa)), wilson(nb, len(wb))
    say(f"- Share with a non-CS primary category: before {100 * pa[0]:.1f}% ({100 * pa[1]:.1f}-{100 * pa[2]:.1f}), "
        f"after {100 * pb[0]:.1f}% ({100 * pb[1]:.1f}-{100 * pb[2]:.1f}).")

    # ---------- compliance
    say()
    say("## Peer-review evidence on strict CS papers")
    say("| window | n | journal-ref | DOI | comment says accepted/published | any of the three |")
    say("|---|---|---|---|---|---|")
    comp_rows = []
    for lab, recs in (("Nov 2023-Sep 2024", [r for r in cs_recs if "2023-11" <= r["m"] <= "2024-09"]),
                      ("Nov 2024-Sep 2025", wa), ("Nov 2025-Sep 2026", wb)):
        k = [sum(r["jr"] for r in recs), sum(r["doi"] for r in recs), sum(r["acc"] for r in recs),
             sum(r["jr"] or r["doi"] or r["acc"] for r in recs)]
        cells = []
        for kk in k:
            pr = wilson(kk, len(recs))
            cells.append(f"{100 * pr[0]:.1f}% ({100 * pr[1]:.1f}-{100 * pr[2]:.1f})")
        say(f"| {lab} | {len(recs)} | " + " | ".join(cells) + " |")
        comp_rows.append([lab, len(recs)] + k)
    for kind in ("survey", "position"):
        for lab, recs in (("before", wa), ("after", wb)):
            sub = [r for r in recs if r["kind"] in (kind, "both")]
            pr = wilson(sum(r["jr"] or r["doi"] or r["acc"] for r in sub), len(sub))
            say(f"- {kind}, {lab}: n = {len(sub)}, any evidence {100 * pr[0]:.1f}% ({100 * pr[1]:.1f}-{100 * pr[2]:.1f})")
    with open(os.path.join(TAB, "compliance.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["window", "n", "journal_ref", "doi", "comment_accepted", "any"])
        w.writerows(comp_rows)
    ev = np.zeros(len(MONTHS)); tot = np.zeros(len(MONTHS))
    for r in cs_recs:
        tot[IDX[r["m"]]] += 1
        ev[IDX[r["m"]]] += (r["jr"] or r["doi"] or r["acc"])

    # ---------- seasonality
    say()
    say("## Seasonality (pre-period, Jan 2022-Oct 2025)")
    say("| calendar month | mean CS papers | mean strict share |")
    say("|---|---|---|")
    seas = []
    for mo in range(1, 13):
        ii = [i for i in range(T0) if int(MONTHS[i][5:]) == mo]
        seas.append((mo, n[ii].mean(), (y[ii] / n[ii]).mean()))
        say(f"| {mo:02d} | {n[ii].mean():.0f} | {100 * (y[ii] / n[ii]).mean():.2f}% |")
    # detrended seasonal index of volume: ratio to centred 12-month moving average
    ma = np.convolve(n, np.ones(12) / 12, mode="same")
    idx_ = [(mo, np.mean([n[i] / ma[i] for i in range(6, T0 - 6) if int(MONTHS[i][5:]) == mo])) for mo in range(1, 13)]
    say("- CS volume relative to its 12-month moving average, by calendar month: " +
        ", ".join(f"{mo:02d}: {v:.2f}" for mo, v in idx_))

    # ---------- figures
    fig, ax = plt.subplots(figsize=(8, 4), dpi=160)
    ax.plot(x, 100 * share, color=C["blue"], linewidth=2, label="observed")
    xp = np.arange(T0, len(MONTHS))
    ax.plot(xp, 100 * p["cf_share"], color=C["orange"], linewidth=2, linestyle=(0, (5, 2)),
            label="expected from pre-rule trend and season")
    ax.fill_between(xp, 100 * p["cf_lo"], 100 * p["cf_hi"], color=C["orange"], alpha=0.15, linewidth=0)
    style(ax, "Self-identified survey and position papers as a share of new arXiv CS papers", "% of CS papers (strict rule)")
    mark_rule(ax)
    ax.legend(frameon=False, fontsize=8, loc="lower left")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig1_cs_strict_share.png")); plt.close(fig)

    fig, axes = plt.subplots(2, 1, figsize=(8, 5.6), dpi=160, sharex=True)
    axes[0].plot(x, n, color=C["blue"], linewidth=2)
    style(axes[0], "All new CS papers per month (any cs.* category)", "papers")
    axes[1].plot(x, y, color=C["blue"], linewidth=2)
    style(axes[1], "Strict survey/position papers in CS per month", "papers")
    mark_rule(axes[1])
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig2_cs_counts.png")); plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4), dpi=160)
    for lab, key, den, col in (("CS", "cs_any|title", "cs_any", C["blue"]),
                               ("mathematics (no CS listing)", "math_notcs|title", "math_notcs", C["orange"]),
                               ("physics group (no CS listing)", "phys_notcs|title", "phys_notcs", C["aqua"])):
        s_ = 100 * Y[key] / N[den]
        ax.plot(x, s_, color=col, linewidth=2, label=lab)
        ax.annotate(lab.split(" (")[0], xy=(x[-1], s_[-1]), xytext=(4, 0), textcoords="offset points",
                    fontsize=8, color=C["ink"], va="center")
    style(ax, "Papers with survey/review in the title (title-only rule), by field", "% of papers")
    mark_rule(ax)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.set_xlim(right=len(MONTHS) + 6)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig3_controls_title_only.png")); plt.close(fig)

    fig_spillover(x, Y, N)

    fig, ax = plt.subplots(figsize=(8, 4), dpi=160)
    for lab, key, col in (("strict (names itself a survey/review/position paper)", "cs_any|strict", C["blue"]),
                          ("broad-only (weaker cues, no self-label)", "cs_any|broad_only", C["orange"])):
        ax.plot(x, 100 * Y[key] / n, color=col, linewidth=2, label=lab)
    style(ax, "Relabelling check in CS: strict versus broad-only share", "% of CS papers")
    mark_rule(ax)
    ax.legend(frameon=False, fontsize=8, loc="lower left")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig5_relabelling.png")); plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4), dpi=160)
    ax.plot(x, 100 * ev / np.maximum(tot, 1), color=C["blue"], linewidth=2)
    style(ax, "Strict CS papers showing peer-review evidence (journal-ref, DOI or acceptance note)", "% of strict CS papers")
    mark_rule(ax)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig6_peer_review_evidence.png")); plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6), dpi=160)
    axes[0].bar([m for m, _ in idx_], [v for _, v in idx_], color=C["blue"], width=0.7)
    axes[0].axhline(1, color=C["muted"], linewidth=0.8)
    axes[0].set_ylim(0.8, 1.2)
    axes[1].bar([s_[0] for s_ in seas], [100 * s_[2] for s_ in seas], color=C["blue"], width=0.7)
    for ax, t, yl in ((axes[0], "CS volume vs 12-month average (pre-rule)", "ratio"),
                      (axes[1], "Mean strict share by calendar month (pre-rule)", "% of CS papers")):
        ax.set_title(t, loc="left", fontsize=10); ax.set_ylabel(yl, fontsize=9, color=C["muted"])
        ax.set_xticks(range(1, 13)); ax.tick_params(colors=C["muted"], labelsize=8)
        ax.grid(axis="y", color="#e4e3df", linewidth=0.6); ax.set_axisbelow(True)
        for s_ in ("top", "right"):
            ax.spines[s_].set_visible(False)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig7_seasonality.png")); plt.close(fig)

    open(os.path.join(RES, "analysis_output.md"), "w", encoding="utf-8").write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
