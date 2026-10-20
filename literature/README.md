# 09 arXiv survey rule: literature map (bibliometrics)

Question: did arXiv's October 2025 moderation rule for review/survey and position papers in computer science change submission patterns?
Map: (A) scientometrics of preprint servers and arXiv; (B) growth of review and survey articles; (C) detection and prevalence of LLM-generated or LLM-assisted scientific writing; (D) effects of editorial and moderation policy on submissions.

- **Corpus:** 1,483 documents (1991-2026) after 17,683 unique candidates, a rule screen (1,407 included), one snowball round (+205) and 140 hand-screen exclusions (`data/clean/manual_exclusions.csv`, reasons X1-X3: AI applied to clinical/engineering/marketing tasks, education-only AI use, statistical "moderation"). Bibliometrix frame 1,480 rows.
- **Date of pull:** 2026-10-13 to 2026-10-17 (2026 is a part year). Policy date used: 31 Oct 2025 (arXiv blog post; see `../01-policy-record.md`).
- **Topic chart:** `figures/P06_publications_per_year_policy.png` (publications per year by sub-literature, policy date marked). It counts literature about the topic, not arXiv submissions.
- Other headline files: `gap-analysis.md`, `evidence-table.csv` (50 rows; `pdfs/` has the open copies found), `figures/captions.md`.

## Folder map
Same layout as paper 08: `search-protocol.md`, `scopus-queries.md`, `data/raw` (cached API responses), `data/clean` (master.csv, references.csv, M.rds, PRISMA json, exclusions), `R/`, `python/`, `figures/` (R* Bibliometrix, P* Python), `tables/`, `vosviewer/`, `pdfs/`.

## Regenerate
```
cd python
..\..\..\_tools\biblio-venv\Scripts\python.exe pipeline.py all ; python handscreen09.py ; python pipeline.py build   # cached; OpenAlex lookups are backed off
cd ..\R ; Rscript 01_build_M.R ; Rscript 02_bibliometrix.R M.rds R ID "arXiv survey rule literature map" 2020,2024   # about 10 min
cd ..\python ; python figures_py.py ; python vosviewer_export.py ; python notes09.py ; python evidence.py pdfs ; python make_docs.py
```

## Limits
- Discovery: Semantic Scholar + Crossref + arXiv API + ACL Anthology. OpenAlex search was refused for budget on 2026-10-13 and its list queries now need a key for deep paging, so OpenAlex was used for DOI lookups only. DBLP returned an anti-bot page and was skipped (no workaround attempted).
- Screening is regular-expression based plus an AI hand check of titles (rules X1-X3); no human re-screen. Sub-literature C and B stay broad (clinical systematic-review quality studies, education-use papers partly remain).
- One named seed (an OSF preprint, DOI 10.31222/osf.io/xs64q_v1) was not found in Semantic Scholar. 58 records lack abstracts; 867 of 1,483 have reference lists, so citation networks under-represent the rest.
- Evidence-table "method"/"relation" notes were written from abstract openings only; rows without an abstract are marked title-only. 16 of the 28 core papers have a legal open copy in `pdfs/`.
- This pack's earlier code sent a personal e-mail address as a courtesy identifier; removed 2026-10-13.
- This folder is the bibliometrics layer only; the paper's own research pack is maintained elsewhere.

## Added network analyses (depth layer 3)
- Burst detection (Kleinberg): `figures/B01_keyword_bursts.png` and `figures/B02_title_phrase_bursts.png`, tables `tables/B01_keyword_bursts.csv` and `B02_title_phrase_bursts.csv`; script `D:\Research-Publishing\_tools\burst.py` (`python burst.py <this folder>`); captions in `figures/captions.md`.
- Main-path (key-route) analysis: `figures/P05_main_path.png`, papers on the path in `tables/P05_main_path_nodes.csv` and links in `P05_main_path_edges.csv`.
- Other layers (reading notes, citation library, data and code appendix) are in `..\depth\`.

## Check against `../02-prior-work.md`
Of the identifiers named in the prior-work file, all but four are in the corpus. Not in the corpus (Semantic Scholar had no record, or the item is not a study): the preprint "The Marker Drift Problem: Measuring LLM-Assisted Writing with Unstable Lexical Indicators" (MetaArXiv, 10.31222/osf.io/xs64q_v1, a named seed that Semantic Scholar did not return); arXiv 2609.04872 "The Generative AI Gold Rush in Theoretical and Computational Research" (cs.DL, 2026); the corrigendum 10.1093/ije/dyaa118 (not a study); and the NeurIPS proceedings DOI 10.52202/079017-3655 (the arXiv version of the same paper, 2406.10252, is in the corpus). All four are in `../depth/citations/references.bib`.
