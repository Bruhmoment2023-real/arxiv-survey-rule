"""Print versions of the paper's Figs 1-7 for Springer (Scientometrics): 174 mm wide, 300 dpi TIFF and PNG, Arial,
no figure titles, series told apart by line style as well as colour. Runs code/analyze.py unchanged; its tables,
figures and analysis_output.md go to results/print_run/ (so results/ is not overwritten), and plt.subplots /
savefig are wrapped here. Paper figure numbers: Fig1 = seasonality, Fig2 = strict share, Fig3 = counts,
Fig4 = controls, Fig5 = spill-over groups, Fig6 = relabelling, Fig7 = peer-review evidence (Fig8: fig8_timeline.py).
Run:  python -I code/make_print_figures.py      (needs data/net.jsonl.gz and data/counts_core.json)"""
import os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUTF = os.path.join(ROOT, "results", "figures", "print")
os.makedirs(OUTF, exist_ok=True)
W_IN = 174 / 25.4
plt.rcParams.update({"font.family": "Arial", "svg.fonttype": "none"})

MAP = {"fig7_seasonality.png": "Fig1", "fig1_cs_strict_share.png": "Fig2", "fig2_cs_counts.png": "Fig3",
       "fig3_controls_title_only.png": "Fig4", "fig4_spillover_shares.png": "Fig5", "fig5_relabelling.png": "Fig6",
       "fig6_peer_review_evidence.png": "Fig7"}
STYLES = ["-", (0, (5, 2)), (0, (1, 1.5))]

_sub = plt.subplots


def subplots(*a, figsize=(8, 4), dpi=160, **k):
    w, h = figsize
    return _sub(*a, figsize=(W_IN, h * W_IN / w), dpi=300, **k)


plt.subplots = subplots
_save = Figure.savefig


def savefig(self, fname, *a, **k):
    name = os.path.basename(str(fname))
    axes = self.get_axes()
    if self._suptitle is not None:
        self._suptitle.set_text("")
    if len(axes) == 1:
        ax = axes[0]
        for loc in ("left", "center", "right"):
            ax.set_title("", loc=loc)
        lines = [l for l in ax.get_lines() if not l.get_label().startswith("_")]
        if len(lines) > 1 and all(l.get_linestyle() == "-" for l in lines):
            for l, s in zip(lines, STYLES):
                l.set_linestyle(s)
            leg = ax.get_legend()
            if leg is not None:
                loc = leg._loc
                ax.legend(frameon=False, fontsize=8, loc=loc)
    if len(axes) > 1:   # the in-panel "rule announced" note overlaps the data; the caption explains the dashed line
        for ax in axes:
            for t in list(ax.texts):
                if t.get_text().startswith("rule announced"):
                    t.remove()
    for ax in axes:
        for t in ax.texts:
            if t.get_fontsize() < 8:
                t.set_fontsize(8)
    self.tight_layout()
    _save(self, fname, *a, **k)
    if name in MAP:
        png = os.path.join(OUTF, MAP[name] + ".png")
        _save(self, png, dpi=300)
        im = Image.open(png).convert("RGB")
        im.save(png, dpi=(300, 300))
        im.save(os.path.join(OUTF, MAP[name] + ".tif"), compression="tiff_lzw", dpi=(300, 300))
        print("wrote", MAP[name], im.size)


Figure.savefig = savefig
sys.path.insert(0, HERE)
import analyze
analyze.RES = os.path.join(ROOT, "results", "print_run")
analyze.TAB = os.path.join(analyze.RES, "tables")
analyze.FIG = os.path.join(analyze.RES, "figures")
for _d in (analyze.TAB, analyze.FIG):
    os.makedirs(_d, exist_ok=True)
analyze.main()
