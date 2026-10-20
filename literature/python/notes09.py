"""Writes data/clean/evidence_notes.csv for paper 09 (method / relation notes written from the opening of each abstract;
rank = row in data/clean/evidence_candidates_with_abstracts.csv). Rows with no abstract are marked title-only."""
import csv
import pandas as pd

d = pd.read_csv('../data/clean/evidence_candidates_with_abstracts.csv', dtype=str, keep_default_na=False)
N = {
1: ("empirical", "Compares LLM-text signals in arXiv review and non-review papers around the CS rule", "Closest prior work: tests the rule's LLM-prevalence premise on arXiv itself; check its data window and detector."),
2: ("position / perspective", "Argues AI-generated survey papers overload the research community", "Frames the problem the October 2025 rule addresses."),
3: ("empirical", "Quantifies AI-generated text presence in arXiv papers", "arXiv-scale LLM prevalence estimate; method to borrow or compare."),
4: ("empirical", "Popularity of arXiv among computer scientists", "Baseline for CS arXiv adoption and growth."),
5: ("empirical", "Linguistic shifts in academic writing before and after ChatGPT", "Before/after design for LLM writing signals."),
6: ("empirical", "Study of pros and cons of posting preprints on arXiv", "Context on author behaviour toward arXiv."),
7: ("empirical", "COVID-19 preprints, dissemination and journal outcomes", "Preprint growth shock precedent for server submission patterns."),
8: ("review", "Benefits and challenges of medical preprints", "Background on preprint servers."),
9: ("review", "Evolution of preprints and their interaction with journals", "Background on preprint growth."),
10: ("empirical", "Over-citation and over-representation of review papers among most cited papers", "Evidence on review-article share and citation impact (sub-literature B)."),
11: ("method", "Tutorial on interrupted time series regression", "Method for a policy-date design: segmented regression and checks."),
12: ("method", "Segmented regression for interrupted time series (title only, no abstract in database)", "Classic ITS reference; method to borrow."),
13: ("research agenda", "Research agenda on review articles in scientometrics", "Frames review articles as a genre to measure."),
14: ("model", "Model of arXiv preprints and journal review articles in physics", "Historical link between arXiv and review articles."),
15: ("empirical", "Large-scale analysis of AI-generated text in scientific writing", "Prevalence method and numbers across sciences."),
16: ("empirical", "Cross-sectional analysis of 57 preprint servers' policies", "Comparator for server policy variation (sub-literature D)."),
17: ("empirical", "arXiv e-prints and the journal of record, combined arXiv and Web of Science data", "Linkage design between arXiv and published versions."),
18: ("empirical", "Maps increasing LLM use across scientific papers", "Distributional-estimate method for LLM-modified text over time, including arXiv."),
19: ("empirical", "Quasi-experimental evidence on arXiv's January 2026 endorsement tightening", "Closest design precedent: a causal study of an arXiv moderation change; check identification and data."),
20: ("commentary", "Science policy note on scientific production in the LLM era", "Short abstract only."),
21: ("empirical", "AI-assisted peer reviews and acceptance rates", "LLM effects on the review stage."),
22: ("empirical", "Journals' AI policies and the rise of AI-assisted writing", "Policy effect on LLM use; relevant to whether editorial rules change behaviour."),
23: ("review", "Mass production of redundant, misleading and conflicted systematic reviews", "Core source for review inflation (sub-literature B)."),
24: ("policy analysis", "arXiv and the REF open-access policy", "Policy-effect precedent on arXiv deposits."),
25: ("empirical", "Popularity and outcomes of all bioRxiv preprints", "Server-level scientometric dataset design."),
26: ("empirical", "Quantifying LLM usage in scientific papers (title only, no abstract in database)", "Distributional LLM-usage estimation across arXiv, bioRxiv and journals; read in full."),
27: ("empirical", "LLM-assisted writing and citation advantage before and after ChatGPT", "Joins LLM use with citation outcomes."),
28: ("method", "Book on interrupted time series analysis", "Method reference."),
29: ("empirical", "E-prints in the literature of physicists and astronomers", "Early arXiv adoption evidence."),
30: ("empirical", "Preprints as accelerator of scholarly communication in mathematics", "arXiv scientometrics in a single field."),
31: ("review", "Comparative review of editorial AI-use policies", "Policy landscape for sub-literature D."),
32: ("empirical", "AAAI-26 AI review pilot", "Venue-level AI policy experiment."),
33: ("review", "LLMs in medical writing and publishing", "Background on LLM-assisted writing."),
34: ("empirical", "Submissions and downloads in the first year of medRxiv, before/after COVID-19", "Submission-pattern measurement with a shock; design precedent."),
35: ("empirical", "Effects of promoting papers via arXiv and X", "arXiv exposure effects."),
36: ("commentary", "Mass production of systematic reviews (title only, no abstract in database)", "Commentary on review inflation."),
37: ("empirical", "arXiv deposit and citation advantage in mathematics journals", "Classic arXiv citation-advantage estimate."),
38: ("empirical", "Positional effects on citation and readership in arXiv", "Announcement-order effects; arXiv interface as a determinant of attention."),
39: ("survey", "arXiv usage habits among Slovenian scientists", "Author behaviour survey."),
40: ("empirical", "Excess vocabulary as a marker of LLM-assisted writing in biomedical papers", "Method for detecting LLM use at corpus level."),
41: ("description", "Description of arXiv's moderation system", "Background on arXiv moderation."),
42: ("policy", "Journal editorial policy on citing preprints", "Editorial policy example."),
43: ("empirical", "Privacy analysis of comments in arXiv files (title only, no abstract in database)", "Peripheral."),
44: ("news", "ESA changes arXiv policy (title only, no abstract in database)", "Peripheral."),
45: ("empirical", "Large-scale evidence of non-existent citations from LLM hallucination", "Quality side effect of LLM use in science."),
46: ("method / model", "SurveyForge: LLM-based automatic survey generation", "Shows how easily LLMs produce surveys (the rule's premise)."),
47: ("description", "bioRxiv: the preprint server for biology", "Server description."),
48: ("case study", "Personal experience with AI-generated peer reviews", "Anecdotal."),
49: ("empirical", "Open access and citation impact in arXiv condensed matter (title only, no abstract in database)", "Classic arXiv citation study."),
50: ("review", "Thirty-year history of online preprint services", "Background."),
}
rows = []
for i, (t, m, rel) in N.items():
    r = d.iloc[i - 1]
    st = "abstract read (opening sentences only; full text not read)" if r.abstract else "title only - no abstract available"
    rows.append({'id': r.id, 'study_type': t, 'data': '', 'models': '', 'method': m, 'read_status': st, 'relation': rel})
with open('../data/clean/evidence_notes.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
print(len(rows))
