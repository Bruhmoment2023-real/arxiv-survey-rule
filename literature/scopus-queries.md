# Scopus and Web of Science queries - paper 09 (arXiv survey and position-paper rule)

Sean has no Scopus or Web of Science login on this machine. These strings are ready to paste into
**Scopus > Advanced document search** and **Web of Science > Advanced Search** by him or a mentor with
institutional access. They mirror the four sub-literatures in `search-protocol.md`.

- `scopus-drop\` was **empty** when this map was built (13 Oct 2026), so no Scopus or WoS records are in the corpus.
- The strings follow each database's documented syntax but have **not been run** (no access). Record the date, the exact
  string and the hit count of every run.
- This topic is a better fit for Scopus/WoS than paper 08: most of it is journal literature (Scientometrics, JASIST,
  Quantitative Science Studies, Journal of Informetrics, PLOS, medical journals), which both databases index well.
  The weak spot is 2024-2026 work on LLM-written papers, much of which is still arXiv-only.

## Export settings

- **Scopus:** Export > **CSV** > tick Citation information, Bibliographical information, Abstract & keywords, Funding details,
  Other information (**Include references**).
- **Web of Science:** Export > **BibTeX** or Plain text > **Full Record and Cited References** (1,000 records per file).
- Put the files in `bibliometrics\scopus-drop\`. Load with
  `bibliometrix::convert2df(file, dbsource = "scopus", format = "csv")` (or `dbsource = "wos", format = "bibtex"`), merge with
  `mergeDbSources(..., remove.duplicated = TRUE)`, save as `.rds`, then
  `Rscript R/02_bibliometrix.R <file.rds> S DE "Scopus/WoS corpus" 2015,2021`.

## Scopus (Advanced document search)

**A. Scientometrics of preprint servers and arXiv**

```
TITLE ( arxiv OR biorxiv OR medrxiv OR chemrxiv OR ssrn OR "preprint server*" OR "preprint repositor*" OR preprint* OR "e-print*" OR eprint* )
AND TITLE-ABS-KEY ( scientometric* OR bibliometric* OR informetric* OR "meta-research" OR metascience OR "science of science"
  OR "citation advantage" OR "citation impact" OR "citation count*" OR "submission rate*" OR "submission pattern*" OR "number of submissions"
  OR "publication rate*" OR "publication fate" OR "subsequently published" OR altmetric* OR growth )
AND PUBYEAR > 1990 AND PUBYEAR < 2027
AND ( DOCTYPE ( ar ) OR DOCTYPE ( cp ) OR DOCTYPE ( re ) )
```

**B. Growth of review and survey articles; review inflation; automated surveys**

```
( TITLE ( review* OR "meta-analys*" OR survey* )
  AND TITLE-ABS-KEY ( ( ( number OR proliferation OR growth OR increase OR inflation OR "mass production" OR flood OR surge OR epidemic OR overproduction )
        W/4 ( "review article*" OR "review paper*" OR "systematic review*" OR "meta-analyses" OR "survey paper*" OR "literature review*" ) )
      OR ( ( redundant OR overlapping OR duplicate* OR unnecessary OR "too many" ) W/3 ( "systematic review*" OR "meta-analyses" OR "review article*" OR "survey paper*" ) )
      OR "research waste" )
  AND TITLE-ABS-KEY ( bibliometric* OR scientometric* OR "meta-research" OR "meta-epidemiolog*" OR "research waste" OR "publication trend*" OR pubmed OR medline OR journal* ) )
OR ( TITLE ( "review article*" OR "review paper*" OR "survey paper*" )
  AND TITLE-ABS-KEY ( "citation impact" OR "citation advantage" OR "highly cited" OR overcit* OR "document type*" )
  AND TITLE-ABS-KEY ( "research article*" OR "original article*" OR "document type*" ) )
OR ( TITLE-ABS-KEY ( "survey generation" OR "automatic literature review" OR "automated literature review" OR "literature review generation" OR autosurvey OR "survey automation" )
  AND TITLE-ABS-KEY ( "large language model*" OR llm OR llms OR chatgpt OR "generative AI" ) )
AND PUBYEAR > 1990 AND PUBYEAR < 2027
```

**C. Detection and prevalence of LLM-generated or LLM-assisted scientific writing**

```
TITLE-ABS-KEY ( ( "AI-generated" OR "LLM-generated" OR "machine-generated" OR "AI-assisted" OR "LLM-assisted" OR "AI-written" OR "ChatGPT-generated"
    OR "use of ChatGPT" OR "use of large language models" OR "use of LLMs" OR "LLM usage" OR "paper mill*" OR "tortured phrases" OR "AI detector*" )
  AND ( "scientific writing" OR "academic writing" OR "scientific paper*" OR "scientific publication*" OR "scholarly publishing" OR "scholarly communication"
    OR "peer review*" OR manuscript* OR preprint* OR arxiv OR "research paper*" OR "journal article*" OR pubmed OR abstracts )
  AND ( detect* OR prevalence OR "excess vocabulary" OR "excess words" OR "word frequenc*" OR stylometr* OR "linguistic marker*" OR lexical OR quantif* OR undisclosed ) )
AND PUBYEAR > 2021 AND PUBYEAR < 2027
AND ( DOCTYPE ( ar ) OR DOCTYPE ( cp ) OR DOCTYPE ( re ) )
```

**D. Effects of editorial and moderation policy changes on submissions**

```
( TITLE ( polic* OR editorial* OR moderat* OR mandat* OR submission* OR fee* OR guideline* OR requirement* OR ban OR endorsement OR "registered report*" OR preprint* OR arxiv )
  AND TITLE-ABS-KEY ( "editorial polic*" OR "policy change*" OR "new policy" OR "journal polic*" OR moderation OR "submission polic*" OR "submission fee*"
      OR "desk reject*" OR mandat* OR "preprint polic*" OR endorsement OR "data sharing polic*" OR "data availability polic*" OR "registered report*" )
  AND TITLE-ABS-KEY ( submission* OR "submitted manuscripts" OR "manuscripts received" )
  AND TITLE-ABS-KEY ( "interrupted time series" OR "difference-in-differences" OR "before and after" OR "natural experiment" OR "effect of" OR "impact of" OR "change* in" OR compliance )
  AND TITLE-ABS-KEY ( journal* OR "preprint server*" OR arxiv OR biorxiv OR medrxiv OR conference* OR editor* ) )
OR ( TITLE ( arxiv OR biorxiv OR medrxiv OR "preprint server*" )
  AND TITLE-ABS-KEY ( moderat* OR endorsement OR screening OR polic* OR rejection OR reclassif* OR withdraw* OR "position paper*" OR "review article*" ) )
AND PUBYEAR > 1990 AND PUBYEAR < 2027
```

**Narrow string for Sean's exact question (run first; read every hit)**

```
TITLE-ABS-KEY ( arxiv AND ( "review article*" OR "survey paper*" OR "position paper*" OR survey* ) AND ( polic* OR moderat* OR rule OR ban OR "peer review" ) )
AND PUBYEAR > 2024
```

## Web of Science Core Collection (Advanced Search)

`TI=` title, `TS=` topic (title, abstract, author keywords, Keywords Plus), `NEAR/n` proximity.

**A**

```
TI=( arxiv OR biorxiv OR medrxiv OR chemrxiv OR ssrn OR "preprint server*" OR "preprint repositor*" OR preprint* OR "e-print*" OR eprint* )
AND TS=( scientometric* OR bibliometric* OR informetric* OR "meta-research" OR metascience OR "science of science" OR "citation advantage" OR "citation impact"
  OR "citation count*" OR "submission rate*" OR "submission pattern*" OR "number of submissions" OR "publication rate*" OR "publication fate"
  OR "subsequently published" OR altmetric* OR growth )
AND PY=(1991-2026) AND DT=(Article OR Proceedings Paper OR Review Article)
```

**B**

```
( TI=( review* OR "meta-analys*" OR survey* )
  AND TS=( ( ( number OR proliferation OR growth OR increase OR inflation OR "mass production" OR flood OR surge OR epidemic OR overproduction )
        NEAR/4 ( "review article*" OR "review paper*" OR "systematic review*" OR "meta-analyses" OR "survey paper*" OR "literature review*" ) )
      OR ( ( redundant OR overlapping OR duplicate* OR unnecessary OR "too many" ) NEAR/3 ( "systematic review*" OR "meta-analyses" OR "review article*" OR "survey paper*" ) )
      OR "research waste" )
  AND TS=( bibliometric* OR scientometric* OR "meta-research" OR "meta-epidemiolog*" OR "research waste" OR "publication trend*" OR pubmed OR medline OR journal* ) )
OR ( TI=( "review article*" OR "review paper*" OR "survey paper*" )
  AND TS=( "citation impact" OR "citation advantage" OR "highly cited" OR overcit* OR "document type*" )
  AND TS=( "research article*" OR "original article*" OR "document type*" ) )
OR ( TS=( "survey generation" OR "automatic literature review" OR "automated literature review" OR "literature review generation" OR autosurvey OR "survey automation" )
  AND TS=( "large language model*" OR llm OR llms OR chatgpt OR "generative AI" ) )
AND PY=(1991-2026)
```

**C**

```
TS=( ( "AI-generated" OR "LLM-generated" OR "machine-generated" OR "AI-assisted" OR "LLM-assisted" OR "AI-written" OR "ChatGPT-generated" OR "use of ChatGPT"
    OR "use of large language models" OR "use of LLMs" OR "LLM usage" OR "paper mill*" OR "tortured phrases" OR "AI detector*" )
  AND ( "scientific writing" OR "academic writing" OR "scientific paper*" OR "scientific publication*" OR "scholarly publishing" OR "scholarly communication"
    OR "peer review*" OR manuscript* OR preprint* OR arxiv OR "research paper*" OR "journal article*" OR pubmed OR abstracts )
  AND ( detect* OR prevalence OR "excess vocabulary" OR "excess words" OR "word frequenc*" OR stylometr* OR "linguistic marker*" OR lexical OR quantif* OR undisclosed ) )
AND PY=(2022-2026) AND DT=(Article OR Proceedings Paper OR Review Article)
```

**D**

```
( TI=( polic* OR editorial* OR moderat* OR mandat* OR submission* OR fee* OR guideline* OR requirement* OR ban OR endorsement OR "registered report*" OR preprint* OR arxiv )
  AND TS=( "editorial polic*" OR "policy change*" OR "new policy" OR "journal polic*" OR moderation OR "submission polic*" OR "submission fee*" OR "desk reject*"
      OR mandat* OR "preprint polic*" OR endorsement OR "data sharing polic*" OR "data availability polic*" OR "registered report*" )
  AND TS=( submission* OR "submitted manuscripts" OR "manuscripts received" )
  AND TS=( "interrupted time series" OR "difference-in-differences" OR "before and after" OR "natural experiment" OR "effect of" OR "impact of" OR "change* in" OR compliance )
  AND TS=( journal* OR "preprint server*" OR arxiv OR biorxiv OR medrxiv OR conference* OR editor* ) )
OR ( TI=( arxiv OR biorxiv OR medrxiv OR "preprint server*" )
  AND TS=( moderat* OR endorsement OR screening OR polic* OR rejection OR reclassif* OR withdraw* OR "position paper*" OR "review article*" ) )
AND PY=(1991-2026)
```

**Narrow string**

```
TS=( arxiv AND ( "review article*" OR "survey paper*" OR "position paper*" OR survey* ) AND ( polic* OR moderat* OR rule OR ban OR "peer review" ) )
AND PY=(2025-2026)
```

## What Scopus/WoS would add here

- **Author keywords and clean affiliations** (the country ranking in this folder rests on OpenAlex affiliations, which are incomplete).
- **Complete reference lists** for the journal part, which sharpens the co-citation map and the historiograph.
- A check on sub-literature D, the thinnest one: a zero or near-zero Scopus result for the narrow string is itself reportable
  evidence that the policy question is open.
