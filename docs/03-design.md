# 03 - Design and analysis plan (fixed before post-policy analysis)

Project: "Did arXiv's 2025 rule stop the survey flood?"
Plan written: 13 Oct 2026, about 16:30 UTC. Classifier rules v1.0 frozen at the same time
(`code/classify.py`, SHA-256 `d3a3b436f6340d1209a2588ae6f172ad2e007a58fcd5993eca397ea79ceda444`).
This file is suitable to post as a pre-registration (for example on OSF) once Sean has read it and
rewritten it in his own words. Section 9 lists honestly what had already been seen when it was written.

## 1. Background in one paragraph
- On 31 Oct 2025 arXiv announced that review (survey) articles and position papers in its computer
  science (CS) section must have completed peer review at a journal or conference before submission,
  with the journal reference and DOI supplied as evidence (see `01-policy-record.md`).
- The rule is applied by moderators before a paper appears. Papers that are refused never enter the
  public metadata. So the study measures what **appears**, not what was **submitted**.

## 2. Research questions
- **RQ1 (volume and share).** After the rule, did the monthly number and share of self-identified
  review and position papers among new arXiv CS papers fall below what the pre-policy trend predicts?
- **RQ2 (displacement).** Did such papers move elsewhere: (a) into non-CS categories with no CS
  listing (stat, eess, q-bio, econ, q-fin, physics.soc-ph), or (b) inside CS-listed papers from a CS
  primary category to a non-CS primary category with a CS cross-list?
- **RQ3 (relabelling).** Did authors stop calling surveys "surveys"? That is, did survey-like papers
  that avoid the explicit words become more common, and did the classifier's recall fall after the rule?
- **RQ4 (compliance evidence).** Do post-policy CS survey and position papers show the required
  peer-review evidence (journal-ref, DOI, or an acceptance note in `comments`) more often than before?

## 3. Data
- Source: arXiv legacy API (`export.arxiv.org/api/query`), metadata only (CC0), within the API Terms
  of Use: one request at a time, at least 3 seconds apart, identified by User-Agent with contact e-mail.
- Window: papers whose first version (v1) was submitted from 1 Jan 2022 to 30 Sep 2026
  (57 months: 46 before the rule, 11 after). Month = calendar month of the v1 timestamp (UTC).
- Three harvested pieces (`code/harvest_api.py`):
  1. **Monthly denominators**: total papers per category group per month (API `totalResults`).
  2. **Candidate net**: full metadata for every paper matching a broad keyword query that is designed to
     be a superset of everything the classifier can fire on. Title terms for survey/review are searched
     in all of arXiv; abstract terms and weaker title terms only inside the study group G.
  3. **Random full days**: every paper in G on one randomly chosen day per month (seed 20251031),
     57 days. Used for hand-labelling, for recall, and to check the net is a true superset.
- Study group G = any category in cs.*, stat.*, eess.*, q-bio.*, econ.*, q-fin.*, or physics.soc-ph.
- "CS paper" = at least one cs.* category in the API metadata. Note: the API stores eess.SY (not cs.SY)
  and math.NA (not cs.NA), so papers listed only through those aliases are not counted as CS. This makes
  the API monthly CS totals about 7% lower than arXiv's `list/cs/YYYY-MM` pages (checked for 2022-01 and 2025-10).
- Fields: id, latest version number, v1 date, latest-version date, title, abstract, primary category,
  all categories, comments, journal-ref, DOI, number of authors.

## 4. Measurement: the classifier
- **Target class (what a human would call it), from title and abstract:**
  - **S - review/survey article:** the main contribution is a synthesis of existing work (survey, review,
    systematic or scoping review, systematic mapping, SoK, overview/tutorial of a research area,
    taxonomy of existing methods, roadmap built from the literature). Meta-analyses count as S.
  - **P - position paper:** the main contribution is an argument, opinion, vision, agenda or call to
    action, without new results as the main content.
  - **N - neither:** research articles (new method, experiment, theorem, dataset, benchmark, system,
    user study, questionnaire survey of people), theses, lecture notes, proceedings, comments.
  - **Mixed papers:** if a paper both surveys and reports substantial new experiments or a new
    benchmark with results, it is labelled **M** and counted as N in the main analysis, as S in a
    sensitivity analysis.
  - **U - cannot tell** from title and abstract: counted as N in the main analysis.
- **Rule classifier v1.0** (`code/classify.py`), case-insensitive, on the latest-version title/abstract:
  - **strict** (primary measure) fires when the paper names itself: "survey" in the title (not in a
    questionnaire sense such as "user survey", "survey data"); "review" in the title in a literature sense
    ("a review", "systematic review", "review of", ": a review"; not "code review", "peer review",
    "product reviews"); "SoK:" / "systematization of knowledge" / "mapping study"; abstract
    self-identification ("this survey", "this review", "we survey", "we review", "this paper
    surveys/reviews", "comprehensive/systematic survey/review", "survey paper"); explicit position
    wording ("Position:" at the start of the title, "position paper", "vision paper", "perspective
    paper", "this perspective", "this commentary", "manifesto").
  - **broad** (sensitivity measure) = strict or weaker cues: title words such as overview, roadmap,
    taxonomy, perspective, primer, tutorial, "challenges and opportunities", "open problems", "future
    directions", "recent advances", should/must/need to, rethinking, "a call for", "the case for";
    abstract phrases such as "we argue", "this paper argues", "we advocate", "we call for",
    "literature review", "we provide an overview/taxonomy/roadmap".
  - **broad-only** = broad but not strict. This is the group where relabelled surveys would land.
  - Outside G only a **title-only** rule (survey / literature-sense review in the title) is available.
- **Validation** (`code/make_label_sample.py`, `code/validate.py`):
  - Population: CS papers on the 57 random days. Strata: strict / broad-only / neither x pre / post.
  - Sample: 50 + 50 strict, 40 + 40 broad-only, 110 + 110 neither = 400 papers, seed 20251031.
  - Labels are made blind: the sheet shows only title and abstract, shuffled; no id, date, category or
    classifier output. To keep the reading load manageable, abstracts longer than 720 characters are shown
    as their first 500 and last 200 characters. Every label is recorded in `data/labels/labels.csv`.
  - Report: precision of strict and of broad (pre, post, pooled); recall of strict and broad estimated
    with stratum weights (population stratum sizes); 95% intervals (Wilson for precision; stratified
    bootstrap, 5,000 resamples, for recall); the pre-post difference in precision and in recall.
  - **Decision rule fixed now:** if strict recall after the rule is lower than before by more than
    10 percentage points (point estimate), the headline result must be reported with a recall-corrected
    estimate (count / recall, by period) next to the raw one, and the conclusion must say the fall is
    partly a measurement artefact.

## 5. Outcomes
- **Primary:** monthly share = (strict-positive CS papers) / (all CS papers), by v1 month.
- Secondary: monthly counts; survey-only and position-only shares; broad share; broad-only share;
  CS-primary numerators only (denominator stays "any CS", because the API cannot count by primary category).
- Displacement outcomes: strict share in each spill-over group **with no CS listing** (stat, eess,
  q-bio, econ, q-fin, physics.soc-ph) and pooled; share of CS strict papers whose primary category is
  not CS; primary-category mix of CS strict papers.
- Comparison series (not subject to the rule): title-only survey share in math (no CS listing) and in a
  physics group (astro-ph, cond-mat, hep-th, hep-ph, quant-ph, gr-qc; no CS listing).
- Compliance outcome: share of strict CS papers with (i) a journal-ref, (ii) a DOI, (iii) a `comments`
  note matching accepted / published / to appear / in press / camera-ready, (iv) any of the three.

## 6. Statistical analysis (interrupted time series)
- **Intervention date:** announcement 31 Oct 2025. October 2025 is the last pre month; November 2025
  is the first post month. Sensitivity: drop October and November 2025 as a wash-out, because papers
  submitted in late October were moderated under the new practice.
- **Primary model:** segmented regression of monthly counts with a log link and an offset:
  log E[Y_t] = log N_t + b0 + b1*t + b2*post_t + b3*(months since rule)*post_t + seasonal terms,
  where Y_t = strict CS papers, N_t = all CS papers. Quasi-Poisson (over-dispersion estimated from the
  Pearson statistic). Seasonal terms: two Fourier harmonics of the 12-month cycle (4 parameters), to
  absorb conference-deadline seasonality. Standard errors: Newey-West (HAC) with lag 3.
- **Primary estimates:** (1) level change exp(b2) = ratio of the share just after the rule to the share
  predicted by the pre-trend; (2) average ratio of observed to counterfactual share over all post months,
  where the counterfactual is the pre-period model (trend + season) extended forward, with a 95%
  interval from a parametric bootstrap of the pre-period coefficients.
- **Simple robustness figure:** same-calendar-month comparison, Nov 2025-Sep 2026 versus Nov 2024-Sep
  2025 (share ratio with a 95% interval), which removes seasonality without a model.
- **Controlled comparison:** the same model on the comparison series (math, physics, title-only rule)
  and on CS with the same title-only rule; report the ratio of ratios (CS change divided by control
  change). A fall in CS that also appears in the controls is not attributed to the rule.
- **Displacement tests:** the same model for each spill-over group and pooled. Also report counts:
  CS deficit = counterfactual minus observed strict CS papers summed over post months; spill-over excess
  = observed minus counterfactual in the pooled spill-over group; displaced fraction = excess / deficit.
- **Placement inside CS:** table of primary categories of strict CS papers, Nov 2024-Sep 2025 versus
  Nov 2025-Sep 2026, with a chi-square test and the share whose primary is not CS.
- **Relabelling tests:** the ITS on the broad-only share in CS (a rise suggests relabelling); pre-post
  difference in strict recall from the hand labels; among hand-labelled true S/P papers, the share
  caught by strict before and after.
- **Compliance:** proportions with peer-review evidence before and after, with Wilson intervals. Known
  bias: older papers have had more time to gain a journal-ref or DOI, so a post-policy increase is a
  conservative finding and a decrease is uninformative.
- **Multiplicity:** one primary test (RQ1, strict share, level change). Everything else is secondary
  and is reported with unadjusted intervals and labelled exploratory.
- **What counts as an answer:** "the rule reduced appearing surveys" needs the primary ratio's 95%
  interval below 1 **and** a ratio of ratios versus controls below 1 **and** no recall collapse (section 4).
  "Displacement" needs a spill-over ratio's interval above 1. Anything else is reported as inconclusive.

## 7. Seasonality and other time effects to report
- Conference cycles (for example NeurIPS in May, ICLR in late September/October, CVPR in November, ACL
  rolling review) move CS volume month to month; the share outcome and the Fourier terms deal with this.
- Survey share itself may be seasonal (surveys are often posted outside deadline rushes). Shown in a
  month-of-year plot of the pre-period.
- Long-run growth: CS volume roughly tripled between Jan 2022 and Oct 2025, so counts alone mislead.

## 8. What cannot be seen (stated limits)
- Submissions that moderators rejected, put on hold, or that authors withdrew before announcement.
- Reclassification by moderators: only the final categories are visible, not the requested ones.
- The title and abstract at first submission: the API gives the latest version only, so later retitling
  is invisible, and the per-version dates are not in this harvest (OAI-PMH `arXivRaw` has them).
- Whether a paper was written with an LLM. This study does not measure that.
- Whether a displaced paper is "the same paper that would have gone to CS". Displacement is inferred
  from aggregate shares only.

## 9. Honest record of what was already known when this plan was fixed
- The classifier rules were written before any harvested record was read or classified.
- Test queries made while building the harvester showed, for October 2025 (a **pre**-policy month):
  14,267 CS papers, 240 with survey or review in the title.
- While drawing the labelling sample, the stratum sizes on the 57 random days were printed and seen:
  strict 469 of 14,598 CS papers before the rule, 93 of 5,181 after. This is a rough preview of the
  direction of RQ1 on 11 post-policy days. No monthly series, no model and no spill-over number had
  been computed. The plan above was not changed after seeing it.
- Later deviations, if any, are listed in `results/RESULTS.md` under "Deviations from the plan".

## 10. Threats to validity (short list)
- Measurement: keyword rules miss surveys that avoid the words, and this could change after the rule.
- Censoring: the outcome is "appeared on arXiv", so a fall cannot separate "fewer written" from
  "refused" from "posted elsewhere (SSRN, TechRxiv, OpenReview, Preprints.org, Zenodo)".
- Confounding in time: the 21 Jan 2026 endorsement change (all sections), the 10 Dec 2025 mathematics
  endorsement change, the 11 Feb 2026 English-version requirement, the 1 Oct 2026 submission rate limit
  (after the window), and general tightening of moderation against LLM-written papers.
- Short post period: 11 months, less than one full seasonal cycle.
- Controls are imperfect: mathematics and physics have different survey cultures and were hit by the
  endorsement change too (mathematics a month earlier).
- One labeller (an AI assistant) made the first labels; a second, human labeller is needed.

## 11. Deviations (added 17 Oct 2026, after the analysis ran)
- None to the analysis plan. Rules v1.0 unchanged. Post-policy numbers were first computed on 17 Oct 2026 by `code/analyze.py` as specified. The spill-over denominators were completed that day.
- Not done: pooled spill-over denominator ignores papers in two spill groups (noted in code); multiplicity is not adjusted.
