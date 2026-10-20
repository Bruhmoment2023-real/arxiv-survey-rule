# Results summary (analysis run 17 Oct 2026; plan fixed in 03-design.md before this run)

Source: `results/analysis_output.md` (full numbers), `results/tables/`, `results/figures/`, `results/classifier_validation.md`.
Window Jan 2022 - Sep 2026 (46 pre months, 11 post months). All intervals are 95%. Everything is "papers that appeared", not "papers submitted".

## RQ1 volume and share in CS (strict rule v1.0)
- Strict survey/position share of CS papers: 3.24% (2022), 3.33% (2023), 3.38% (2024), 3.24% (Jan-Oct 2025), 2.00% (Nov 2025-Sep 2026). Pre-period trend is flat (about +0.1% per year).
- Strict count in the 11 post months: 3,291 observed against about 5,499 predicted from the pre-trend and season (deficit about 2,208).
- Primary ITS level change at Nov 2025: ratio 0.622 (0.573-0.675). Observed/counterfactual over all post months: 0.599 (0.568-0.630). Same-calendar-month share ratio (Nov 2025-Sep 2026 vs Nov 2024-Sep 2025): 0.609 (0.582-0.637). Wash-out (drop Oct and Nov 2025): 0.621 (0.561-0.687).
- Surveys fell more than positions: survey-kind ratio 0.528 (0.474-0.587); position-kind 1.042 (0.821-1.323), same-month ratio 1.165 (1.056-1.286), i.e. no fall for position papers.
- Title-only rule ("survey" or literature-sense "review" in the title): CS share fell to about one third (same-month ratio 0.334, 0.310-0.360). It fell far more than the strict rule, which also uses abstracts.
- Quasi-Poisson dispersion about 2.5, so intervals use HAC errors; they are not tight evidence of a causal effect.

## Controls
- Mathematics (no CS listing), title-only: level ratio 1.18 (0.95-1.45), but observed/counterfactual 0.72 and same-month 0.77 (0.59-1.01). Physics group, title-only: level 1.10, observed/counterfactual 0.93, same-month 0.895 (0.81-0.99). Controls therefore also drifted down somewhat; counts are small (math 106 post).
- Ratio of ratios, CS over controls (same-month): 0.43 (0.33-0.58) vs math, 0.37 (0.33-0.42) vs physics. The CS fall exceeds the controls' fall.
- Not separable from this rule: the 21 Jan 2026 endorsement change (all sections) and general tightening against AI-written papers.

## RQ2 displacement
- Pooled spill-over groups (stat, eess, q-bio, econ, q-fin, physics.soc-ph with no CS listing), strict: level ratio 1.29 (1.15-1.45) but observed/counterfactual 0.971 (0.906-1.038) and same-month 0.992 (0.884-1.113). The level step is offset by a negative slope change; overall counts show no excess (observed 637, predicted 656).
- Displaced fraction (excess/deficit) about -0.01: no evidence that the missing CS surveys reappeared in these groups.
- By group (observed/counterfactual): stat 1.07, eess 1.14 (0.97-1.32), q-bio 0.76, econ 0.93, q-fin 1.45 (1.06-1.86, only 31 papers), physics.soc-ph 0.88. Only q-fin is above 1, small numbers, unadjusted for multiple looks: exploratory.
- Inside CS, share of strict papers with a non-CS primary: 9.6% (8.8-10.6) before, 10.9% (9.9-12.0) after. Count of such papers fell (obs 358 vs predicted 469). Mix by primary category changed (chi-square 156.7, df 14): cs.AI up (8.5% to 13.3%), cs.CL (12.9% to 8.6%) and cs.CV (11.3% to 7.5%) down.
- Not tested: other preprint servers (SSRN, TechRxiv, OpenReview, Preprints.org, Zenodo).

## RQ3 relabelling and measurement
- Broad-only share (weaker cues like "overview", "roadmap", "we argue") rose: level 1.16 (1.02-1.32), observed/counterfactual 1.27 (1.19-1.35). Compatible with relabelling, but this class has only 20-22% true surveys/positions in the labelled sample, so it could also be new LLM-style phrasing of research papers.
- Classifier v1.0 vs 400 hand labels (first pass by an AI labeller, not yet human second-labelled): strict precision 0.86 pre, 0.76 post (difference -0.10, -0.26 to +0.06); strict recall 0.53 pre, 0.45 post (difference -0.08, -0.455 to +0.30). The pre-fixed trigger was a recall fall above 10 points: not met by the point estimate, but the interval is too wide to rule it out.
- Hand-label estimate of true S/P prevalence in CS: 5.2% (3.2-8.0) before, 3.0% (1.8-5.2) after: ratio about 0.58, matching the strict-rule ratio, but with a wide interval.
- Rule flaw found: "this perspective ..." fires on research abstracts (6 of 19 strict false positives).
- Coverage: the candidate net found 99.1% of strict positives on the 57 random full days (641 of 647); 15 missed are listed in `results/net_coverage.md`.

## RQ4 peer-review evidence on strict CS papers
- Any of journal-ref, DOI or "accepted/published" in comments: 32.9% (Nov 2023-Sep 2024), 28.3% (Nov 2024-Sep 2025), 27.3% (Nov 2025-Sep 2026; 25.8-28.8). No rise after the rule.
- Journal-ref 12.3% -> 10.5% -> 8.5%; DOI 20.2% -> 15.6% -> 11.0%; comments note 16.3% -> 15.5% -> 18.6%.
- Interpretation caution: newer papers have had less time to gain a journal-ref/DOI, so the fall in those fields is expected. The finding that compliance evidence is NOT visibly higher fits the policy being enforced at moderation (rejected papers never appear) only weakly: the survivors still mostly lack metadata evidence, so authors may be putting the evidence in the PDF or moderators accept other proof. Not resolved.

## Seasonality
- CS volume peaks in May and October (about 1.2 times the annual average) and dips in January (0.80). Strict share is higher in Jan-Feb (about 3.8-3.9%) and lowest in Sep-Oct (about 2.8-2.9%). The post period contains Nov-Sep only, so a same-calendar-month comparison is the cleanest check, and it agrees with the model.

## What this does not show
- Moderator rejections are invisible; a fall in appearing papers cannot be split into fewer submitted, more refused, or posted elsewhere.
- Causal attribution to the rule alone: the endorsement change (Jan 2026), the English-version rule (Feb 2026), and AI-paper tightening overlap. Controls are small and imperfect.
- The strict rule misses about half of true surveys/positions; the estimate is of the share of explicitly named ones.
