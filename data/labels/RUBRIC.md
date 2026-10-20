# Labelling rubric (version 1, 13 Oct 2026)

Label each paper from its **title and abstract only**. Do not look at the arXiv id, date, category,
comments or the classifier output. One label per paper.

| Label | Meaning | Decide by asking |
|---|---|---|
| **S** | Review / survey article | Is the main contribution a synthesis of **existing** work? Includes: survey, review, systematic or scoping or multivocal review, systematic mapping study, SoK, meta-analysis, overview or tutorial of a research area, taxonomy of existing methods, roadmap built from the literature, magazine-style overview. |
| **P** | Position paper | Is the main contribution an **argument**: opinion, vision, agenda, viewpoint, commentary, call to action, philosophical essay, with no new results as the main content? |
| **M** | Mixed | Does it survey the literature **and** report substantial new experiments, a new benchmark with results, or a new system with evaluation? (Counted as "not S/P" in the main analysis, as S in the sensitivity analysis.) |
| **U** | Cannot tell | Is the abstract missing, replaced by an admin notice, or too vague to decide? (Counted as "not S/P".) |
| **N** | Neither | Everything else: new method, model, theorem, dataset, benchmark, system, user study, questionnaire survey of people, shared-task or challenge report, thesis, lecture notes, comment/reply. |

## Tie-break rules
1. "Survey" meaning a questionnaire of people is **N**.
2. A paper that reviews prior work only as motivation ("we first review X, then propose Y") is **N**.
3. A paper that says "we argue" but then proposes and evaluates a method is **N**.
4. A challenge or shared-task "overview" paper is **N** (it reports new results).
5. A paper that calls itself both a survey and a position paper is **S**.
6. A tutorial on a research area is **S**; course lecture notes are **N**.
7. A conceptual or normative proposal with no results and no literature synthesis is **P**, but mark it
   as borderline in the note column (these are the least reliable labels).
8. If unsure between S and P, choose either: both are the positive class.

## Files
- `sheet_part01.txt` ... `sheet_part08.txt`: the 400 blind items (title + abstract; abstracts longer than
  720 characters are shown as first 500 + last 200 characters).
- `labels.csv`: key, label, labeller, note. First pass by the AI assistant on 13 Oct 2026.
- `sample_key.csv`: links each key to the arXiv id, period, stratum and rules fired. **Do not open before
  labelling.**
- `strata_sizes.json`: how many CS papers on the 57 random days fall in each stratum (weights).

## For Sean (second labeller)
- Label at least the 100 "strict" items and 80 "broad-only" items yourself, blind, in a new column
  `label_sean` in a copy of `labels.csv`. Find which keys those are **after** labelling, or simply label all
  400 (about 4-5 hours).
- Then compute agreement (Cohen's kappa) between the two label columns and report it. Disagreements are
  settled by reading the full abstract on arXiv and writing down the reason.
