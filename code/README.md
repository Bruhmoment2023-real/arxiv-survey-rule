# Code for "Did arXiv's 2025 rule stop the survey flood?"

Everything runs on a laptop with free software. Two Python environments are used:
- the system Python 3.12 (standard library only) for harvesting, parsing, classifying and labelling;
- the project environment `.venv` (numpy, statsmodels, scipy, matplotlib, pypdf) for the analysis.
  Recreate it with:
  `python -m venv .venv` then
  `.venv\Scripts\python -m pip install --cache-dir D:\Research-Publishing\.pip-cache numpy statsmodels matplotlib pypdf`

Run every command from the project folder `D:\Research-Publishing\09-arxiv-survey-rule`.

## Order of work

| Step | Command | What it makes |
|---|---|---|
| 1 | `python code\harvest_api.py days` | `data\raw\days\`: every paper in study group G on 57 random days |
| 2 | `python code\harvest_api.py counts_core` | `data\counts_core.json`: monthly totals per category group |
| 3 | `python code\harvest_api.py net` | `data\raw\net\`: full metadata of every paper in the candidate net |
| 4 | `python code\parse.py days` and `python code\parse.py net` | `data\days.jsonl.gz`, `data\net.jsonl.gz` |
| 5 | `python code\make_label_sample.py` | blind labelling sheets in `data\labels\` (already done; rerunning reproduces the same sample) |
| 6 | (human) label the sheets using `data\labels\RUBRIC.md` | `data\labels\labels.csv` (`code\write_labels.py` holds the first-pass labels) |
| 7 | `python code\validate.py` | `results\classifier_validation.md`, `results\label_disagreements.csv` |
| 8 | `python code\check_net.py` | `results\net_coverage.md`: is the net really a superset of the classifier? |
| 9 | `.venv\Scripts\python code\analyze.py` | `results\tables\`, `results\figures\`, `results\analysis_output.md` |

## The harvester and arXiv's rules
- `harvest_api.py` uses the arXiv legacy API. It keeps to the Terms of Use
  (https://info.arxiv.org/help/api/tou.html): one request at a time, 5 seconds apart (the rule is 3),
  a User-Agent that names the project and a contact e-mail, metadata only.
- **Resumable:** every response is saved in `data\raw\`. Stop it with Ctrl-C at any time; running the same
  command again continues where it stopped and never repeats a saved request.
- **One copy only:** `data\harvest.lock` stops a second copy starting. If the script was killed, delete the
  lock file.
- **HTTP 429:** arXiv limits by network address, and on a shared connection other programs use up the same
  allowance. The script waits two minutes and tries again, for up to two hours per request.
- Options: `--start 2024-11 --end 2026-09` (months), `--groups cs_any,math_notcs` (for `counts_core`),
  `--delay 5`.
- `counts_cs` (monthly totals for the ten largest cs.* categories) is optional and was not needed for the
  planned analysis.
- `harvest_oai.py` is the **ready-to-run** full harvest through OAI-PMH (all papers, all version dates,
  about 3 GB for `cs`). Not run yet. Never run it at the same time as `harvest_api.py`.

## The classifier
- `classify.py`, rules version 1.0, frozen on 13 Oct 2026 before post-policy numbers were computed.
  `python code\classify.py` runs seven self-tests.
- Do not edit the patterns. If the rules need to change, copy the file to `classify_v2.py`, say why in
  `03-design.md`, and report both versions.
- Known weakness found in validation: the abstract rule "this perspective / this commentary / this essay"
  fires on research papers that say "this perspective unifies ..." (6 of the 19 strict false positives).

## Other files
- `html2text.py`, `pdf2text.py`: turn saved web pages and PDFs into text for quoting.
- `priorwork_search.py`, `priorwork_s2.py`: prior-work searches (OpenAlex, Semantic Scholar, Crossref) with
  caching. On 13 Oct 2026 only Crossref answered; rerun them later.

## Data notes
- "CS paper" = at least one `cs.*` category in the API metadata. eess.SY and math.NA papers are **not** CS
  here even though arXiv lists them under cs.SY / cs.NA.
- Month = month of the first version (`published` field, UTC).
- Title, abstract, comments, journal-ref and DOI are those of the **latest** version at harvest time.
- All metadata are CC0 (arXiv API Terms of Use). The harvest cache can be shared; do not present the
  project as endorsed by arXiv.

## Run record
- 17 Oct 2026: `counts_core` finished for the six spill-over groups (`--groups stat_notcs,eess_notcs,qbio_notcs,econ_notcs,qfin_notcs,socph_notcs`; the `G_any` series is not used by analyze.py). Then `analyze.py` ran once (about 25 minutes on the 197,664-record net; most time is the classifier).
