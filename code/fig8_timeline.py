"""Fig. 8 of the paper (timeline of the study window and the arXiv policy changes in or next to it).
No data file: the events, dates and period lengths are those cited in the paper (arXiv 2025a, 2025b, 2026a, 2026b).
Layout follows the v15 figure (redrawn 21 Oct 2026 from the v16 script 09-fig8.py), at Springer's 174 mm width.
Run:  python -I code/fig8_timeline.py [output folder]    (default results/figures/print; writes Fig8.png and Fig8.tif)"""
import datetime as dt, os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from PIL import Image

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results", "figures", "print")
os.makedirs(OUT, exist_ok=True)
W = 174 / 25.4
plt.rcParams.update({"font.family": "Arial", "font.size": 8.5})


def save(fig, name):
    png = os.path.join(OUT, name + ".png")
    fig.savefig(png, dpi=300, facecolor="white")
    plt.close(fig)
    im = Image.open(png).convert("RGB")
    im.save(png, dpi=(300, 300))
    im.save(os.path.join(OUT, name + ".tif"), compression="tiff_lzw", dpi=(300, 300))
    print(name, im.size)


# ---------- 09 Fig 8: timeline (events and periods cited in the paper)
def X(y, m, d):
    t = dt.date(y, m, d); s = dt.date(y, 1, 1); e = dt.date(y + 1, 1, 1)
    return y + (t - s).days / (e - s).days


ev = [(X(2025, 10, 31), "31 Oct 2025: CS rule on review and position papers", 1.1),
      (X(2025, 12, 10), "10 Dec 2025: mathematics endorsement change", -1.1),
      (X(2026, 1, 21), "21 Jan 2026: endorsement tightened in all sections", 1.9),
      (X(2026, 2, 1), "Feb 2026: English-version requirement", -1.9),
      (X(2026, 10, 1), "1 Oct 2026: rate limit (after the window)", 2.7)]
pre = (X(2022, 1, 1), X(2025, 10, 31)); post = (X(2025, 11, 1), X(2026, 10, 1))
fig, ax = plt.subplots(figsize=(W, 2.8))
ax.fill_between(pre, -0.12, 0.12, color="#c8d6ea", lw=0)
ax.fill_between(post, -0.12, 0.12, color="#f0cbbb", hatch="////", edgecolor="#d9a48f", lw=0)
ax.plot([pre[0], post[1]], [0, 0], color="black", lw=1.2)
for y in range(2022, 2027):
    ax.plot([y, y], [-0.18, 0.18], color="black", lw=1)
    ax.text(y, -0.3, str(y), ha="center", va="top", fontsize=9)
for x, lb, hh in ev:
    ax.plot([x, x], [0, hh], color="#555555", lw=0.7, zorder=1)
    ax.plot(x, 0, "o", color="#b22222", ms=5, zorder=3)
    ax.text(x - 0.02, hh, lb, ha="right", va="center", fontsize=8.5)
ax.legend(handles=[Patch(color="#c8d6ea", label="Pre-rule period, Jan 2022 to Oct 2025 (46 months)"),
                   Patch(facecolor="#f0cbbb", hatch="////", edgecolor="#d9a48f", label="Post period, Nov 2025 to Sep 2026 (11 months)")],
          loc="lower left", bbox_to_anchor=(0.0, -0.02), ncol=1, frameon=False, fontsize=8.5, handlelength=1.6)
ax.set_xlim(2021.85, 2026.9); ax.set_ylim(-3.2, 3.0); ax.axis("off")
fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
save(fig, "Fig8")
