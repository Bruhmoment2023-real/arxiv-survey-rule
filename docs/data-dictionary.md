# Data dictionary: paper 09 (arXiv survey and position-paper rule), `D:\Research-Publishing\09-arxiv-survey-rule\`

Inventory taken 17 Oct 2026 while another agent was still rebuilding the paper's research pack in this folder; files added after this date are not covered (see "Missing or not inventoried" at the end). `bibliometrics\` (literature map) is documented in section B. Variables below were read from the files' headers.

## A. Study data (research pack)

| Path | Source and access | Rows and content | Variables / meaning | Known problems |
|---|---|---|---|---|
| `data\raw\days\` (114 files), `data\days.jsonl.gz` | arXiv legacy API (metadata only, CC0), 57 random sample days; harvest log `data\harvest.log` | 22,442 papers in the study group on the sampled days | `id`, `v` (version field from the parser; meaning not documented in code\README.md), `published` (first version, UTC), `updated`, `title`, `abstract`, `primary` (primary category), `cats` (all categories), `comment` (author comments), `journal_ref`, `doi`, `n_authors`, `sample_day` | Title, abstract, comments, journal-ref and DOI are those of the latest version at harvest time, not at posting. |
| `data\raw\net\` (525 files), `data\net.jsonl.gz` | arXiv API; the keyword "candidate net" (superset of the classifier) | 197,664 papers | same as above without `sample_day` | Not a census: papers no keyword catches are not in the net (net found 641 of 647 strict positives on the 57 full sample days, 99.1 percent, `results\net_coverage.md`). |
| `data\counts_core.json` (+ `counts_run*.out/.err`) | arXiv API monthly totals | one entry per `<group>\|<YYYY-MM>` | monthly paper totals per category group (CS, mathematics without CS listing, physics without CS listing, and six spill-over groups: stat, eess, q-bio, econ, q-fin, physics.soc-ph) | The status file says spill-over series were completed 2024-03 to 2026-09 on 17 Oct 2026. |
| `data\harvest.log` | harvester log | text | request log | |
| `data\labels\` | hand-label exercise | `labels.csv` 400 rows (`key`, `label`, `labeller`, `note`); `sample_key.csv` 400 rows (`key`, `id`, `period` pre/post, `stratum`, `rules`, `published`, `primary`); `strata_sizes.json` (strict pre 469, strict post 93, broad-only pre 457, broad-only post 203, neither pre 13,672, neither post 4,885); blind sheets `sheet_part01-08.txt`; `RUBRIC.md` | label = hand classification as survey/position or not per the rubric | Labels are a first pass by an AI labeller; no human second labeller yet (so no kappa). |
| `data\priorwork\` | Crossref and Semantic Scholar prior-work searches, 13 Oct 2026 | `crossref_*.json`, `s2_*.json`, `hits.tsv`, `hits2.tsv`, `s2_run.log`, `pdf\` (open PDFs and text of prior work) | raw API responses and hit lists | Semantic Scholar and OpenAlex answered only partly on that day. |
| `data\sources\` (30 files) | arXiv's own pages, saved 13 Oct 2026 | HTML of the policy blog posts (10 Sep 2025, 31 Oct 2025, 21 Nov 2025, 10 Dec 2025, 21 Jan 2026, 26 Jun 2026) and API terms pages | quotations in `01-policy-record.md` come from these | Pages are copies as of the access date. |

### Results (`results\`)
| File | Content |
|---|---|
| `tables\monthly_series.csv` (57 months) | Columns `month`; `N_<group>` = monthly paper totals; `Y_<group>\|<rule>` = monthly counts of papers flagged by each rule (strict, survey, position, broad, broad_only, title, and CS-primary/non-CS-primary splits) |
| `tables\its_results.csv` (18 series) | Interrupted time-series results per series: pre/post counts, level ratio with 95 percent interval, p, observed/counterfactual ratio and interval, same-month share ratio and interval, slope change, pre-trend, dispersion |
| `tables\compliance.csv` | Share of strict CS papers with journal-ref, DOI, accepted/published in comments, or any, in three windows |
| `tables\placement_primary.csv` | Primary category mix of strict papers before and after the rule |
| `figures\fig1-fig7*.png` | Strict share, counts, title-only controls, spill-over shares, relabelling, peer-review evidence, seasonality |
| `analysis_output.md`, `RESULTS-SUMMARY.md` | Full numbers and summary (analysis run 17 Oct 2026) |
| `classifier_validation.md/.json`, `label_disagreements.csv` (38 rows), `net_coverage.md` | Classifier precision/recall against the 400 hand labels; disagreements; coverage of the candidate net |

Unit of observation note: all series count papers that appeared (first version month, UTC), not submissions; moderator rejections are invisible.

## B. Literature map (`bibliometrics\data\`)
| File | Content |
|---|---|
| `raw\{s2,crossref,arxiv,openalex}\`, `raw\candidates_*.jsonl` | Cached API responses and candidate records, access 13-17 Oct 2026 |
| `clean\master.csv` (1,483 rows) | One row per document; same variables as paper 08's `master.csv` (`id`, `title`, `abstract`, `year`, `pub_date`, `venue`, `doc_type`, `authors`, `doi`, `arxiv_id`, `cited_by`, `local_citations`, `sublits` A-D, `primary_sublit`, `institutions`, `countries`, `openalex_keywords`, `oa_pdf_url`, and Bibliometrix-style `AU`, `SO`, `SR`) |
| `clean\references.csv` (37,274 rows) | `citing`, `cited`, `cited_title`, `cited_year`, `cited_first_author`, `cited_venue`, `cited_doi`, `in_corpus`, `cr` |
| `clean\M.rds`, `master.rds` | Bibliometrix frame (1,480 rows) and master as R objects |
| `clean\manual_exclusions.csv` (140 rows), `excluded_by_rule.csv`, `prisma_stage*.json`, `search_counts.json`, `coverage.json` | Hand-screen exclusions with rule codes X1-X3, rule exclusions, counts |
| `clean\evidence_notes.csv`, `evidence_candidates_with_abstracts.csv` | Hand-written evidence notes; top-50 abstracts |
Known problems: 58 records lack abstracts; 867 of 1,483 have reference lists; one named seed (OSF preprint 10.31222/osf.io/xs64q_v1) not found in Semantic Scholar; DBLP skipped (anti-bot page); the hand screen is rule-based on titles.

## C. Missing or not inventoried
- Any `followup\` folder, new documents or other files created by the agent rebuilding this pack after 17 Oct 2026 are not listed here.
- The hand labels have no second labeller; the status file marks this as a condition before submission.
- No Moderator-rejection data, no other preprint servers' data (SSRN, TechRxiv, OpenReview, Preprints.org, Zenodo), as stated in `results\RESULTS-SUMMARY.md`.
- `data\priorwork\pdf` contents were not itemised here.
