"""Record of the first-pass hand labels (labeller: AI assistant, 13 Oct 2026, blind sheets).

Labels follow the rubric in 03-design.md section 4 / data/labels/RUBRIC.md:
  S survey/review, P position, M mixed (survey + substantial new results), U cannot tell, N neither.
Every item not listed below was labelled N. Writes data/labels/labels.csv (400 rows).
Notes mark the judgement calls that a second labeller should look at first.
"""
import csv, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = [2, 5, 8, 19, 20, 21, 27, 30, 40, 44, 45, 47,
     52, 54, 61, 68, 74, 75, 79, 80, 83, 87, 99,
     113, 120, 121, 122, 132, 133, 136, 137, 140,
     151, 167, 169, 177, 188, 191, 193, 195,
     202, 211, 215, 217, 226, 233, 240, 247,
     251, 254, 262, 265, 268, 270, 271, 275, 276, 282, 288, 290, 292,
     306, 311, 312, 316, 317, 320, 327, 330, 335, 338, 350,
     360, 374, 382, 391, 393, 398]
P = [10, 13, 51, 59, 71, 72, 81, 102, 109, 112, 114, 182, 204, 207,
     255, 294, 295, 301, 340, 344, 351, 357, 373]
M = [9, 84, 361]
U = [232, 242]
NOTES = {
    8: "overview of normalizing-flow variants; no 'survey' word in excerpt",
    9: "systematic evaluation + review repo; benchmark results -> mixed",
    10: "conceptual/normative proposal with use-cases; borderline P vs N",
    17: "workshop paper summarising own datasets; kept N",
    47: "survey/SoK of LLM-agent security that also 'argues'; S",
    51: "industry-style argument paper; borderline P vs N",
    54: "SLR plus a proposed framework; S",
    59: "argues for a testing view, then sketches an approach; borderline P vs N",
    61: "review of 210 benchmarks that also argues; S",
    74: "self-described 'position and survey paper'; S",
    79: "tutorial on a research area; S under the rubric",
    81: "conceptual proposal (FAIR 2.0); borderline P vs N",
    84: "systematic review + new system with results -> mixed",
    99: "literature-review-based conceptual paper; S",
    136: "book-length overview of RL; S (could be read as lecture notes)",
    139: "challenge overview report; N",
    140: "review/perspective on key-value memory; S",
    166: "empirical study that also advocates; N",
    167: "industry overview with a review; S",
    188: "feature article overviewing a line of work; S",
    191: "tutorial/perspective with historical review; S",
    204: "industrial viewpoint / vision article; P",
    207: "blueprint / vision article; borderline P vs S",
    213: "shared-task overview; N",
    216: "system paper with strong argument framing; kept N",
    231: "essay with a simulation; kept N",
    232: "abstract replaced by an arXiv admin removal notice",
    242: "reads like a project proposal; cannot tell",
    243: "short proposal of a design process; kept N",
    262: "review that includes a simulation comparison; S",
    270: "magazine-style overview (lessons learned, opportunities); S",
    290: "review/perspective; S",
    294: "magazine-style vision/overview; P (S would also be defensible)",
    295: "position-style title, ships a reproduction harness; P",
    301: "philosophy argument paper; P",
    312: "magazine-style overview with research directions; S, uncertain",
    330: "review/perspective on devices; S, uncertain",
    333: "'reviews the argument' but contributes results; N",
    351: "perspective linking regulation and attacks; borderline P vs N",
    361: "taxonomy + review + codebase + empirical evaluation -> mixed",
    363: "'perspectives' in title but reports results; N",
    364: "'we review ... using our benchmark' = evaluation; N",
    373: "argument built on an existing experiment; P",
    374: "overview that derives research desiderata; S",
    375: "philosophical conceptual-modelling paper; kept N",
    382: "overview of cloud resource management; S",
}


def main():
    lab = {i: "N" for i in range(1, 401)}
    for code, ids in (("S", S), ("P", P), ("M", M), ("U", U)):
        for i in ids:
            assert lab[i] == "N", i
            lab[i] = code
    out = os.path.join(ROOT, "data", "labels", "labels.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["key", "label", "labeller", "note"])
        for i in range(1, 401):
            w.writerow([f"L{i:03d}", lab[i], "AI-assistant-pass1", NOTES.get(i, "")])
    print("written", out, {c: sum(v == c for v in lab.values()) for c in "SPMUN"})


if __name__ == "__main__":
    main()
