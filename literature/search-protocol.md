# Search protocol - 09 arXiv survey rule: scientometrics of preprint servers, review inflation, LLM-written science, editorial/moderation policy effects

- **Date of search:** 2026-10-13 (UTC). Years covered: 1991-2026 (2026 incomplete).
- **Who screened:** rule-based screening by the regular expressions below, followed by a hand check of titles by the mapping agent (an AI assistant), not by a human reviewer. Sean should re-screen the core set himself before citing counts.
- **No API keys, no logins.** Every response is cached in `data/raw/`.

## 1. Databases and what each was used for

- Semantic Scholar Graph API bulk search (free, no key): primary discovery source; also supplies reference lists for citation networks and snowballing.
- Crossref REST API (free): relevance-ranked free-text discovery and DOI metadata.
- OpenAlex (free, keyless): used for single-work lookups by DOI (institutions, countries, keywords, topics, citation counts) and for filling missing abstracts. OpenAlex list/search requests were refused for budget on 2026-10-13 (anonymous quota shared by the network address was spent), so OpenAlex was NOT used as the discovery search for this paper; this is a coverage limit stated in README.md. All OpenAlex requests were slow, cached and carry no personal identifier.
- ACL Anthology BibTeX export and arXiv API (cs.DL and related queries), screened locally. DBLP returned an anti-bot challenge page (HTTP 202) and was skipped; no attempt was made to evade it.
- Scopus and Web of Science: no access here; ready-to-paste strings are in scopus-queries.md and bibliometrics/scopus-drop/ is empty.

## 2. Exact search strings and hits

### Semantic Scholar bulk search (title + abstract; `+` = AND, `|` = OR; year filter 1991-2026)

| Tag | Sub-literature | Query | Hits reported | Records taken |
|---|---|---|---|---|
| A0 | Scientometrics of preprint servers and arXiv | `(arXiv \| bioRxiv \| medRxiv \| SSRN \| "preprint server" \| "preprint servers" \| "preprint repository" \| "preprint repositories") + (scientometric \| scientometrics \| bibliometric \| bibliometrics \| "submission patterns" \| submissions \| "publication rate" \| "citation advantage" \| "peer-reviewed publication" \| "subsequently published" \| "growth")` | 1374 | 1374 |
| A1 | Scientometrics of preprint servers and arXiv | `(preprints \| preprint \| "e-prints" \| eprints) + (scientometric \| scientometrics \| bibliometric \| bibliometrics \| "citation advantage" \| "subsequent publication" \| "publication fate" \| "subsequently published")` | 295 | 295 |
| B0 | Growth of review and survey articles; review inflation; automated surveys | `("review articles" \| "review papers" \| "survey papers" \| "literature reviews" \| "systematic reviews" \| "meta-analyses") + (proliferation \| inflation \| "mass production" \| redundant \| overlapping \| "too many" \| "increasing number" \| "growth in the number" \| "research waste" \| "number of reviews" \| "number of systematic reviews") + (bibliometric \| scientometric \| scientometrics \| "meta-research" \| "research waste" \| "publication trends" \| "publications")` | 4534 | 4534 |
| B1 | Growth of review and survey articles; review inflation; automated surveys | `("review articles" \| "review papers" \| "survey papers") + ("citation impact" \| "citation advantage" \| citations \| "highly cited" \| overcitation) + (bibliometric \| scientometric \| scientometrics \| bibliometrics)` | 1163 | 1163 |
| B2 | Growth of review and survey articles; review inflation; automated surveys | `("survey generation" \| "automated literature review" \| "automatic literature review" \| "literature review generation" \| AutoSurvey \| "automated survey" \| "scientific survey") + ("large language models" \| "large language model" \| LLM \| LLMs)` | 79 | 79 |
| C0 | Detection and prevalence of LLM-generated or LLM-assisted scientific writing | `("large language model" \| "large language models" \| LLM \| LLMs \| ChatGPT \| "generative AI" \| "AI-generated" \| "machine-generated" \| "AI-assisted" \| "LLM-generated" \| "LLM-assisted") + ("scientific writing" \| "academic writing" \| "scientific papers" \| "scholarly" \| "scientific abstracts" \| "peer review" \| "peer reviews" \| manuscripts \| preprints \| arXiv \| "research papers" \| "scientific publications") + (detection \| detect \| detecting \| prevalence \| "excess vocabulary" \| "word frequency" \| "increasing use" \| estimate \| estimating \| "stylistic" \| "linguistic markers")` | 1625 | 1625 |
| D0 | Effects of editorial and moderation policy changes on submissions | `(journal \| journals \| "preprint server" \| arXiv \| bioRxiv \| conference \| conferences) + ("policy change" \| "editorial policy" \| "policy changes" \| "editorial policies" \| moderation \| "submission policy" \| "submission fee" \| "submission fees" \| "desk rejection" \| "preprint policy" \| "new policy") + (submissions \| "submission rates" \| "number of submissions" \| "interrupted time series" \| "difference-in-differences" \| "before and after" \| "submission behavior" \| "submission behaviour")` | 975 | 975 |
| D1 | Effects of editorial and moderation policy changes on submissions | `(arXiv \| "preprint server" \| "preprint servers" \| bioRxiv \| medRxiv) + (moderation \| endorsement \| screening \| policy \| policies \| "position papers" \| "review articles")` | 1057 | 1057 |

### Crossref `query.bibliographic` (relevance-ranked free text, no Boolean; top results taken per string, then screened locally)

| Tag | Sub-literature | Query | Hits reported | Records taken |
|---|---|---|---|---|
| A0 | Scientometrics of preprint servers and arXiv | `arXiv submissions scientometric analysis growth` | 7082091 | 600 |
| A1 | Scientometrics of preprint servers and arXiv | `preprint server bioRxiv medRxiv bibliometric analysis publication fate` | 6390813 | 600 |
| A2 | Scientometrics of preprint servers and arXiv | `preprints subsequently published peer-reviewed journals citation advantage` | 695367 | 600 |
| B0 | Growth of review and survey articles; review inflation; automated surveys | `growth of review articles number of reviews bibliometric` | 8589804 | 600 |
| B1 | Growth of review and survey articles; review inflation; automated surveys | `mass production redundant systematic reviews meta-analyses` | 3899960 | 600 |
| B2 | Growth of review and survey articles; review inflation; automated surveys | `review papers citation impact overrepresentation highly cited` | 8507890 | 600 |
| B3 | Growth of review and survey articles; review inflation; automated surveys | `automatic survey generation large language models literature review` | 10555744 | 600 |
| C0 | Detection and prevalence of LLM-generated or LLM-assisted scientific writing | `LLM-generated text scientific papers prevalence detection` | 3780311 | 600 |
| C1 | Detection and prevalence of LLM-generated or LLM-assisted scientific writing | `ChatGPT academic writing excess vocabulary abstracts` | 1475601 | 600 |
| C2 | Detection and prevalence of LLM-generated or LLM-assisted scientific writing | `AI-generated content peer reviews conferences estimate` | 2706613 | 600 |
| D0 | Effects of editorial and moderation policy changes on submissions | `editorial policy change effect on journal submissions interrupted time series` | 8629263 | 600 |
| D1 | Effects of editorial and moderation policy changes on submissions | `arXiv moderation policy endorsement` | 1150456 | 600 |
| D2 | Effects of editorial and moderation policy changes on submissions | `journal data sharing policy mandate effect submissions` | 6527053 | 600 |
| D3 | Effects of editorial and moderation policy changes on submissions | `submission fee introduction journal submissions effect` | 3722294 | 600 |

### ACL Anthology full BibTeX export with abstracts (screened locally with the rules in section 3)

| Tag | Sub-literature | Query | Hits reported | Records taken |
|---|---|---|---|---|
| anthology | - | `local regex screen of the full ACL Anthology BibTeX export (same rules as screening)` | 131695 | 126 |

### arXiv API (`abs:` = abstract field)

| Tag | Sub-literature | Query | Hits reported | Records taken |
|---|---|---|---|---|
| A0 | Scientometrics of preprint servers and arXiv | `cat:cs.DL AND (abs:arXiv OR abs:preprints) AND (abs:submissions OR abs:growth OR abs:scientometric OR abs:bibliometric)` | 57 | 57 |
| C0 | Detection and prevalence of LLM-generated or LLM-assisted scientific writing | `(abs:"LLM-generated" OR abs:"AI-generated" OR abs:ChatGPT OR abs:"LLM-assisted") AND (abs:"scientific papers" OR abs:"academic writing" OR abs:arXiv OR abs:"peer reviews") AND (abs:detection OR abs:prevalence OR abs:vocabulary)` | 67 | 67 |
| sibling_s2_files | - | `Semantic Scholar hits already cached by the paper's own agent (read-only)` | 29 | 29 |

### DBLP search API

| Tag | Sub-literature | Query | Hits reported | Records taken |
|---|---|---|---|---|
| probe | - | `romanized hindi` **(HTTP 202; body starts: '<!doctype html><html lang="en"><head><title>Making sure you&#39;re not a bot!</title><link')** | n/a | 0 |

## 3. Inclusion rules (applied to title + abstract, case-insensitive)

A record is included if it matches **at least one** sub-literature rule. Within a rule every numbered group must match.

**A. Scientometrics of preprint servers and arXiv**
  1. `\b(arxiv|biorxiv|medrxiv|chemrxiv|ssrn|psyarxiv|socarxiv|osf preprints|research square|preprint servers?|preprint repositor\w+|pre-?prints?|e-?prints?)\b` (must match in the **title**)
  2. `\b(scientometric\w*|bibliometric\w*|informetric\w*|meta-?research|meta-?science|science of science|citation (advantage|impact|counts?|analysis|rates?)|submission (rates?|patterns?|trends?|volume|behaviou?r)|number of submissions|growth|publication (rates?|fate|delay|outcomes?|status)|subsequently published|published in (a )?(peer-reviewed |scholarly )?journals?|longitudinal|large-scale (analysis|study)|quantitative (analysis|study)|altmetric\w*|adoption of preprint\w*)\b`

**B. Growth of review and survey articles; review inflation; automated surveys**
- Alternative 1 (any alternative is enough):
  1. `\b((number|numbers|proliferation|growth|increase|rise|inflation|mass production|flood|surge|explosion|epidemic|overproduction|glut|deluge) (of|in) (\w+[ -]){0,3}(review articles?|review papers?|systematic reviews?|meta-analyses|survey papers?|survey articles?|literature reviews?|reviews)|(redundant|overlapping|duplicate|duplicated|unnecessary|too many|conflicted) (\w+[ -]){0,2}(review articles?|review papers?|systematic reviews?|meta-analyses|survey papers?|survey articles?|literature reviews?|reviews)|research waste|review (article )?(inflation|proliferation))\b`
  2. `\b(bibliometric\w*|scientometric\w*|meta-?research|meta-epidemiolog\w+|research waste|publication (trends?|rates?)|pubmed|medline|published (between|from|in the)|journals?|arxiv)\b`
  3. `\b(reviews?|meta-analys\w+|surveys?)\b` (must match in the **title**)
- Alternative 2 (any alternative is enough):
  1. `\b(review articles?|review papers?|survey papers?|review literature|reviews)\b` (must match in the **title**)
  2. `\b(bibliometric\w*|scientometric\w*|citation (impact|advantage|counts?|rates?)|highly cited|overcit\w+|document types?)\b`
  3. `\b(research articles?|original (research )?articles?|non-review|document types?|share of|proportion of|primary (research|studies))\b`
- Alternative 3 (any alternative is enough):
  1. `\b(survey generation|automat\w+ (literature |scientific |academic )?(surveys?|reviews?)( generation| writing)?|autosurvey|literature review generation|(llm|ai|machine)-generated (surveys?|reviews?|survey papers?)|survey automation)\b`
  2. `\b(llms?|large language models?|generative ai|chatgpt|gpt-?\d\w*)\b`

**C. Detection and prevalence of LLM-generated or LLM-assisted scientific writing**
  1. `\b((ai|llm|machine|gpt|chatgpt)[- ](generated|assisted|written|modified|produced|authored)|(generated|written|assisted|produced) (by|with) (ai|llms?|chatgpt|large language models?|generative ai)|(use|usage|adoption|uptake|influence|impact|footprint|fingerprints?|traces?|prevalence) of (llms?|large language models?|chatgpt|generative ai|generative artificial intelligence|ai (writing )?tools?)|llm[- ]usage|chatgpt usage|paper mills?|fake papers?|tortured phrases|ai text detect\w+|ai detectors?)\b`
  2. `\b(scientific (writing|papers?|publications?|abstracts?|literature|articles?|manuscripts?|publishing)|academic (writing|papers?|publishing|abstracts?|publications?|literature|articles?)|scholarly (writing|publishing|communication|articles?|literature|publications?)|peer[- ]reviews?|manuscripts?|preprints?|arxiv|research (papers?|articles?)|journal articles?|biomedical (abstracts|publications|literature)|pubmed)\b`
  3. `\b(detect\w*|prevalence|excess (vocabulary|words?)|word frequenc\w+|increasing use|stylistic|stylometr\w+|linguistic (markers?|shifts?|features|patterns?|signatures?)|lexical|delve|quantif\w+|proportion of|fraction of|share of|widespread|undisclosed|disclos\w+)\b`

**D. Effects of editorial and moderation policy changes on submissions**
- Alternative 1 (any alternative is enough):
  1. `\b(editorial polic\w+|polic(y|ies) changes?|change in polic\w+|new polic\w+|journal polic\w+|moderation|submission (polic\w+|fees?|requirements?|guidelines|caps?|limits?)|desk[- ]reject\w*|mandat\w+|preprint polic\w+|endorsement|data[- ]sharing polic\w+|data availability polic\w+|open[- ]access polic\w+|pre-?registration requirement|registered reports?|reporting guidelines?|ban(ned|s)?)\b`
  2. `\b(submissions?|submitted (manuscripts|papers|articles)|manuscripts? received|submission (rates?|volume|numbers?))\b`
  3. `\b(interrupted time series|difference-in-differences?|before and after|pre- and post-|pre/post|natural experiment|effects? of|impact of|changes? in|declin\w+|increas\w+|decreas\w+|drop\w*|compliance)\b`
  4. `\b(journals?|preprint servers?|arxiv|biorxiv|medrxiv|conferences?|editors?|editorial)\b`
  5. `\b(polic\w+|editorial\w*|moderat\w+|mandat\w+|submission\w*|fees?|guidelines?|requirements?|ban\w*|desk|endorsement|registered reports?|preprints?|arxiv)\b` (must match in the **title**)
- Alternative 2 (any alternative is enough):
  1. `\b(arxiv|biorxiv|medrxiv|chemrxiv|ssrn|preprint servers?|preprint repositor\w+)\b` (must match in the **title**)
  2. `\b(moderat\w+|endorsement|screening|polic(y|ies)|rejection|reclassif\w+|withdraw\w+|retract\w+|quality control|position papers?|review articles?)\b`

## 4. Exclusion rules

- Publication year outside 1991-2026.
- No sub-literature rule matched on title + abstract (the database search engines match more loosely than the rules).
- Title rules: E1 front matter / errata only
  - `^(proceedings|front matter|preface|table of contents|author index|program committee|erratum|correction)`
- Hand screen: records listed in `data/clean/excluded_manual.csv`, each with its reason.
- Versions: a preprint and its published version are one record (merged by Semantic Scholar paper ID, DOI, arXiv ID, ACL ID, then by normalised title + first-author surname).

## 5. Snowballing (one round)

- Central papers: the 33 most locally cited documents after the first screen, plus named seed papers.
- Backward (their references not yet in the corpus): 853 candidates.
- Forward (papers citing them, Semantic Scholar citations endpoint, capped per paper): 8086 candidates.
- Screened with the same rules: 8829 unique candidates, 8615 excluded, **205 added**.

## 6. PRISMA-style counts

| Step | Records |
|---|---|
| Identified: acl anthology | 126 |
| Identified: arxiv | 124 |
| Identified: sibling prior work search | 29 |
| Identified: crossref | 8400 |
| Identified: semantic scholar | 11102 |
| **Identified, all sources** | **19781** |
| Duplicates removed (same ID or same title across sources and queries) | 2098 |
| Unique records screened | 17683 |
| Excluded by rule (off-topic, year, front matter, modality) | 16276 |
| &nbsp;&nbsp;&nbsp;- no sub-literature rule matched | 16276 |
| Passed the rules | 1407 |
| Further version duplicates merged after ID resolution | 0 |
| Named seed papers added although no search found them | 11 |
| Corpus after first screen | 1418 |
| Added by snowballing | 205 |
| Removed in hand screen | 140 |
| **Final corpus** | **1483** |

## 7. Coverage of the final corpus

| Field | Documents | Share |
|---|---|---|
| with abstract | 1425 | 96.1% |
| with reference list | 867 | 58.5% |
| with openalex record | 1459 | 98.4% |
| with institution | 1226 | 82.7% |
| with country | 1219 | 82.2% |
| with openalex keywords | 1451 | 97.8% |
| with doi | 1418 | 95.6% |
| with arxiv id | 269 | 18.1% |
| with acl id | 74 | 5.0% |
| with dblp key | 330 | 22.3% |
| preprint only | 99 | 6.7% |
| records with preprint and published version merged | 96 | 6.5% |

- Reference links: 37274 in total, 1717 point to another corpus document.
- By sub-literature (a document can match several): {'C': 682, 'B': 491, 'A': 191, 'D': 150}
- By document type: {'review': 982, 'article': 293, 'preprint': 99, 'conference paper': 79, 'other': 13, 'book': 1, 'conference-paper': 8, 'peer-review': 4, 'book-chapter': 1, 'editorial': 3}

## 8. Limits

