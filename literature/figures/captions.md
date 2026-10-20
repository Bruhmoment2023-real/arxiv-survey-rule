# Figure captions

39 figures. Each entry: what it shows, the data and settings that produced it, and one caution.
PNG files are 220 dpi. Scripts: `R/02_bibliometrix.R` (files starting with a letter code and a number, e.g. R02_),
`python/figures_py.py` (P..), `python/vosviewer_export.py` (V_..), plus any task-specific script named in the entry.

## B01_keyword_bursts.png
- **Title:** Keyword bursts (Kleinberg), OpenAlex keywords
- **Shows:** Keywords whose share of documents jumps above their long-run share for a run of years.
- **Data and settings:** Corpus of 1480 documents; yearly document counts per term; Kleinberg discrete two-state burst detection (base rate = overall share, burst rate = 2x base, transition cost gamma*ln(T)); terms in at least 8 documents; the 20 heaviest bursts are drawn, full table in tables/B01_keyword_bursts.csv.
- **Caution:** A burst means a term's share jumps relative to its own overall share, not that it is important; last-year bursts rest on a part year and small yearly counts, and keywords come from OpenAlex's automatic tagging, which covers only the documents that have an OpenAlex record.
- **Also saved as:** B01_keyword_bursts.svg

## B02_title_phrase_bursts.png
- **Title:** Title-phrase bursts (Kleinberg)
- **Shows:** Two-word title phrases whose share jumps above their long-run share for a run of years.
- **Data and settings:** Corpus of 1480 documents; yearly document counts per term; Kleinberg discrete two-state burst detection (base rate = overall share, burst rate = 2x base, transition cost gamma*ln(T)); terms in at least 8 documents; the 20 heaviest bursts are drawn, full table in tables/B02_title_phrase_bursts.csv.
- **Caution:** A burst means a term's share jumps relative to its own overall share, not that it is important; last-year bursts rest on a part year and small yearly counts, and keywords come from OpenAlex's automatic tagging, which covers only the documents that have an OpenAlex record.
- **Also saved as:** B02_title_phrase_bursts.svg

## P01_citation_network.png
- **Title:** Direct citation network (PNG, and interactive HTML of the same name)
- **Shows:** Corpus documents as nodes, citations between them as links; colour = sub-literature, size = citations received from inside the corpus.
- **Data and settings:** Corpus: 1483 documents, 1994-2026. Top 300 documents by local citations; 229 are connected (216 in the largest component). Reference lists from Semantic Scholar/OpenAlex; networkx spring layout seed 7; pyvis for the HTML.
- **Caution:** Distances come from a force-directed layout and have no scale; papers without a reference list in the database look isolated even if they cite the field.
- **Also saved as:** P01_citation_network.html

## P02_key_paper_timeline.png
- **Title:** Timeline of key papers
- **Shows:** The 30 most locally cited documents (and any named seed papers) placed at their publication date.
- **Data and settings:** Corpus: 1483 documents, 1994-2026. Ranked by citations from other corpus documents; date = Semantic Scholar publication date (mid-year if only the year is known).
- **Caution:** 'Key' means most cited inside this corpus; very recent papers (2025-26) cannot have accumulated citations yet and are under-represented.
- **Also saved as:** P02_key_paper_timeline.svg

## P03_publications_by_year_and_subfield.png
- **Title:** Publications by year and sub-literature
- **Shows:** Stacked annual counts, each document assigned to one sub-literature.
- **Data and settings:** Corpus: 1483 documents, 1994-2026. Sub-literature assigned by the keyword rules in search-protocol.md; a document matching several rules is counted under the first in the stated priority order (non-exclusive counts in tables/P03_year_by_sublit_nonexclusive.csv).
- **Caution:** The split depends on the priority order and on the wording of the rules; the latest year is incomplete.
- **Also saved as:** P03_publications_by_year_and_subfield.svg

## P04_coverage_heatmap.png
- **Title:** Preprint servers and venues by theme: documents mentioning both (title or abstract)
- **Shows:** Number of corpus documents whose title or abstract mentions both the row term and the column term.
- **Data and settings:** Corpus: 1483 documents, 1994-2026. Coding by regular expressions listed in config.json -> heatmap (title + abstract; 1425 documents have an abstract). Cells are not exclusive.
- **Caution:** Mention is not focus: a paper that names arXiv once in passing counts the same as a study of arXiv, and only title and abstract are read.
- **Also saved as:** P04_coverage_heatmap.svg

## P05_main_path.png
- **Title:** Main path (key-route) through the direct citation network
- **Shows:** The chain(s) of papers that carry the most citation 'traffic' from the earliest to the latest documents in the corpus.
- **Data and settings:** Corpus: 1483 documents, 1994-2026. Direct citations between corpus documents made acyclic (links running backwards in time dropped, 1715 links kept); search path count (SPC) weight per link; global key-route search from the 8 highest-SPC links, extended forwards and backwards along the highest-SPC neighbour. Tables: tables/P05_main_path_nodes.csv and _edges.csv.
- **Caution:** A main path is one summary of the citation structure, driven by where reference lists are available; it is not a ranking of quality and it omits whole branches of the field.
- **Also saved as:** P05_main_path.svg

## P06_publications_per_year_policy.png
- **Title:** Publications per year by sub-literature with the policy date marked
- **Shows:** Annual counts of corpus documents in each of the four sub-literatures; the dashed line is the arXiv blog announcement of 31 Oct 2025.
- **Data and settings:** Corpus: 1483 documents, 1994-2026. Non-exclusive sub-literature membership from the search rules (tables/P06_year_by_sublit_policy.csv); policy date from the arXiv blog post saved in ../data/sources/ of the paper folder (01-policy-record.md).
- **Caution:** This is a map of the research literature about the topic, NOT arXiv submission counts: it cannot show whether the rule changed submission patterns, and 2025-26 counts are depressed by indexing lag and, for 2026, a part year.
- **Also saved as:** P06_publications_per_year_policy.svg

## R02_annual_production.png
- **Title:** Annual scientific production
- **Shows:** Number of corpus documents per publication year, with compound annual growth rates.
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). Counts of M$PY; growth from full years only. Table: tables/ R02_annual_production .csv
- **Caution:** Growth reflects what the search rules and the databases capture, and recent years are inflated by preprints that older years lack; it is not a clean measure of the field's true growth.
- **Also saved as:** R02_annual_production.svg

## R03_average_citations_per_year.png
- **Title:** Average citations per year
- **Shows:** Mean total citations per document divided by years since publication, for each publication year.
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). Citations = database citation count at the pull date; citable years = 2026 - PY + 1.
- **Caution:** A few very highly cited papers drive the peaks; years with few documents are unstable (point size shows n).

## R04_most_relevant_sources.png
- **Title:** Most relevant sources
- **Shows:** The 20 venues (journals, conferences, preprint servers) with the most corpus documents.
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). Source = venue string as supplied by the database, upper-cased.
- **Caution:** Venue names are not fully harmonised (workshops and proceedings volumes can be split or merged), and a preprint server counts as one 'source'.

## R04_bradford_law.png
- **Title:** Bradford's law
- **Shows:** Sources ranked by productivity; the shaded core zone holds about one third of all documents.
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). bibliometrix::bradford(); zones in tables/ R04_bradford_zones .csv
- **Caution:** Bradford zones describe concentration only; a 'core' source is the most frequent, not necessarily the best or the most relevant.

## R05_source_dynamics.png
- **Title:** Source dynamics
- **Shows:** Cumulative number of corpus documents over time in the eight most frequent sources.
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). bibliometrix::sourceGrowth(top = 8, cdf = TRUE).
- **Caution:** A steep recent line for a preprint server partly reflects papers that have not yet appeared in their final venue.

## R06_most_productive_authors.png
- **Title:** Most productive authors
- **Shows:** Authors with the most documents in the corpus (each co-author counted once per paper).
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). Author strings 'SURNAME INITIALS' built from database author names; table also gives fractional counts and citations.
- **Caution:** Authors are matched by surname and initials only, so different people with the same short name are merged and one person with name variants is split.

## R06_most_cited_authors.png
- **Title:** Most cited authors
- **Shows:** Authors ranked by the summed global citation counts of their documents in the corpus.
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). Sum of database citation counts over each author's corpus papers; every co-author receives the full count.
- **Caution:** One heavily cited multi-author paper lifts all of its co-authors; this is not a measure of individual contribution.

## R06_lotka_law.png
- **Title:** Lotka's law
- **Shows:** Share of authors by number of corpus documents, against the inverse-square law.
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). bibliometrix::lotka(); table in tables/ R06_lotka .csv
- **Caution:** A good fit says only that most authors appear once; name ambiguity (see author caption) distorts the tail.

## R06_authors_production_over_time.png
- **Title:** Authors' production over time
- **Shows:** For the 15 most productive authors: bubble size = documents that year, colour intensity = citations per year.
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). bibliometrix::authorProdOverTime(k = 15).
- **Caution:** Same name-matching caveat as the author ranking; a gap in a line may be a missing record, not inactivity.

## R07_most_relevant_affiliations.png
- **Title:** Most relevant affiliations
- **Shows:** Institutions appearing on the most corpus documents (once per document).
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). Affiliation/country data exist for 82% of documents (1218 of 1480). Institution names as disambiguated by the source database.
- **Caution:** Coverage is partial and uneven: preprints and workshop papers often carry no affiliation in the database, so institutions that publish mainly that way are under-counted.

## R07_corresponding_author_countries.png
- **Title:** Corresponding-author countries
- **Shows:** Documents by country of the corresponding (or first) author, split into single-country and multi-country papers.
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). Affiliation/country data exist for 82% of documents (1218 of 1480). Country from the institution country codes in the database.
- **Caution:** Only documents with affiliation data are counted, so shares are of the covered subset, not of the whole corpus.

## R07_country_collaboration_map.png
- **Title:** Country collaboration map
- **Shows:** Countries shaded by number of documents; red links join countries whose authors co-sign documents.
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). Affiliation/country data exist for 82% of documents (1218 of 1480). bibliometrix::biblioNetwork(collaboration, countries); links table in tables/.
- **Caution:** Countries with no affiliation data in the database appear empty even if they publish in this field; a link is co-authorship, not funding or influence.

## R08_most_global_cited_documents.png
- **Title:** Most globally cited documents
- **Shows:** Corpus documents with the most citations from anywhere in the database.
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). Citation count as reported by the source database at the pull date.
- **Caution:** Global citations reward age and breadth: a general-purpose model or benchmark paper outranks a narrowly relevant study.

## R08_most_local_cited_documents.png
- **Title:** Most locally cited documents
- **Shows:** Documents most cited by other documents inside the corpus - the field's own reference points.
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). Local citations counted by exact database identifiers where available (column LCS_exact_id_match); bibliometrix::localCitations() string matching is reported alongside as a cross-check.
- **Caution:** Local counts depend on reference lists being available: documents whose citing papers have no reference list in the database are under-counted.

## R08_most_cited_references.png
- **Title:** Most cited references
- **Shows:** The works the corpus cites most often, including works outside the corpus (the field's knowledge base).
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). bibliometrix::citations(field = 'article') over the reference strings.
- **Caution:** Method and tool papers (models, toolkits, metrics) dominate such lists because nearly everyone cites them; frequency is not topical closeness.

## R09_rpys.png
- **Title:** Reference publication year spectroscopy
- **Shows:** How many cited references were published in each year, and where that count jumps above its 5-year median (labelled peaks = historical roots).
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). bibliometrix::rpys(timespan 1950-2026, centred median window).
- **Caution:** In a fast field almost all references are from the last few years, so the curve mostly mirrors the field's own growth; only the early, isolated peaks point to roots.

## R10_most_frequent_keywords.png
- **Title:** Most frequent keywords
- **Shows:** The 30 most frequent OpenAlex keywords.
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). Field ID; coverage 98%. OpenAlex keywords are assigned by an algorithm from title and abstract, not chosen by the authors.
- **Caution:** Keyword counts depend on who assigned them: algorithmic keywords are consistent but coarse, author keywords are precise but unstandardised.

## R10_wordcloud.png
- **Title:** Keyword word cloud
- **Shows:** The 120 most frequent OpenAlex keywords; size proportional to document count.
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). wordcloud::wordcloud(), seed 42.
- **Caution:** A word cloud shows frequency only; position and colour carry no meaning, and long terms look bigger than short ones at equal counts.

## R10_keyword_treemap.png
- **Title:** Keyword treemap
- **Shows:** Area of each tile = number of documents carrying the keyword (top 40).
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). treemapify::geom_treemap().
- **Caution:** Documents carry several keywords, so areas overlap in meaning and do not sum to the corpus.

## R10_trend_topics.png
- **Title:** Trend topics
- **Shows:** For each year, the keywords whose median year of use falls there; bubble size = frequency, bar = interquartile range of years.
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). bibliometrix::fieldByYear(n.items = 4).
- **Caution:** A term placed in a recent year is 'recent on average', not necessarily new: older steady terms can be hidden by the per-year cap of four items.

## R11_keyword_cooccurrence_network.png
- **Title:** Keyword co-occurrence network
- **Shows:** Keywords (nodes, sized by frequency) linked when they appear on the same document; colours are Louvain communities.
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). biblioNetwork(co-occurrences), association-strength normalisation, top 60 nodes, edges with at least 2 co-occurrences, Fruchterman-Reingold layout, seed 123.
- **Caution:** Clusters change with the number of nodes, the normalisation and the random seed; read them as a rough grouping, not a fixed taxonomy.

## R12_thematic_map.png
- **Title:** Thematic map
- **Shows:** Keyword clusters placed by centrality (links to other clusters) and density (internal cohesion): motor, niche, basic and emerging/declining themes.
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). bibliometrix::thematicMap(n = 250 keywords, minfreq = 5 per thousand documents, Louvain, seed 1234); cluster table in tables/.
- **Caution:** Quadrant positions are relative ranks within this corpus only; a cluster near an axis can switch quadrant with a small change in settings.

## R13_thematic_evolution.png
- **Title:** Thematic evolution
- **Shows:** Keyword clusters in each time slice and how they flow into clusters of the next slice (line width = share of shared keywords). Interactive version: same name .html; per-slice thematic maps: thematic_map_sliceN.png.
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). bibliometrix::thematicEvolution(cut years 2020, 2024, n = 250, minFreq = 5, Louvain, seed 1234).
- **Caution:** Cut years are a choice; early slices hold few documents, so their themes rest on small numbers and the flows from them are fragile.
- **Also saved as:** R13_thematic_evolution.html

## R14_cocitation_references_network.png
- **Title:** Co-citation network of references
- **Shows:** Cited works (nodes) linked when corpus documents cite them together; clusters approximate the intellectual bases of the field.
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). biblioNetwork(co-citation, references) on references cited at least twice; top 60 nodes, edges with at least 3 co-citations, Louvain, Fruchterman-Reingold.
- **Caution:** Only documents with a reference list in the database contribute, and reference strings are matched by first author, year and source, so variants of one work can appear as two nodes.

## R14_cocitation_sources_network.png
- **Title:** Co-citation network of sources
- **Shows:** Venues (nodes) linked when works published in them are cited together by corpus documents.
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). metaTagExtraction(CR_SO) then biblioNetwork(co-citation, sources); top 40 nodes.
- **Caution:** Source names come from cited-reference strings and are unharmonised; 'ARXIV' is a single huge node that pulls everything towards it.

## R15_bibliographic_coupling_network.png
- **Title:** Bibliographic coupling
- **Shows:** Corpus documents linked when their reference lists overlap; clusters are current research fronts.
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). biblioNetwork(coupling, references), Salton normalisation, top 60 nodes, Louvain.
- **Caution:** Coupling favours documents with long reference lists (surveys) and ignores documents whose references are missing from the database.

## R16_historiograph.png
- **Title:** Historiograph (direct citation network)
- **Shows:** The 25 most locally cited documents arranged by year, with arrows for direct citations between them.
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). bibliometrix::histNetwork(min.citations = 12.25) and histPlot(n = 25).
- **Caution:** The picture keeps only 25 nodes; an absent arrow can mean a missing reference list rather than no intellectual link.

## R17_collaboration_network_authors.png
- **Title:** Author collaboration network
- **Shows:** Authors linked by co-authorship; clusters are research groups.
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). biblioNetwork(collaboration, authors); top 60 authors; isolates removed.
- **Caution:** Short author names merge namesakes, which can create false bridges between groups.

## R17_collaboration_network_institutions.png
- **Title:** Institution collaboration network
- **Shows:** Institutions linked when their authors co-sign documents.
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). Affiliation/country data exist for 82% of documents (1218 of 1480). biblioNetwork(collaboration, universities); top 50.
- **Caution:** Built only from the documents that carry affiliations in the database (see coverage); absent institutions are not necessarily inactive.

## R17_collaboration_network_countries.png
- **Title:** Country collaboration network
- **Shows:** Countries linked by internationally co-authored documents.
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). Affiliation/country data exist for 82% of documents (1218 of 1480). biblioNetwork(collaboration, countries); top 35; circle layout.
- **Caution:** Same coverage limit as the country map; large countries sit in the centre because they publish more, not because they 'lead'.

## R18_three_field_plot.html
- **Title:** Three-field plot (interactive HTML)
- **Shows:** Sankey diagram linking author countries (left), keywords (middle) and sources (right).
- **Data and settings:** Corpus: arXiv survey rule literature map (n = 1480 documents, 1994-2026). bibliometrix::threeFieldsPlot(n = 12, 15, 12). Saved as HTML because the plotly widget cannot be rendered to PNG without a browser.
- **Caution:** Only the top items of each field are shown, so flows describe the most frequent combinations, not the whole corpus.
