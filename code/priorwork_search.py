"""Prior-work search through OpenAlex (free, no key; polite pool via mailto) and Semantic Scholar
(free, no key; heavily rate limited, so failures are logged and skipped).
Every raw response is cached in data/priorwork/. Output: data/priorwork/hits.tsv
Usage: python priorwork_search.py
"""
import os, json, time, urllib.parse, urllib.request, hashlib, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "priorwork")
os.makedirs(OUT, exist_ok=True)
MAIL = "research-contact-withheld@example.invalid"
UA = f"arxiv-survey-rule-study/0.1 (mailto:{MAIL})"

QUERIES = [
    # (label, query, from_year)
    ("policy-effect", "arXiv review articles position papers peer review requirement computer science", 2025),
    ("policy-effect", "arXiv moderation policy survey papers peer review 2025", 2025),
    ("policy-effect", "arXiv ban review articles position papers", 2025),
    ("policy-effect", "arXiv policy change survey papers interrupted time series", 2025),
    ("survey-growth", "AI-generated survey papers flood arXiv", 2023),
    ("survey-growth", "growth of survey papers machine learning arXiv", 2019),
    ("survey-growth", "survey of surveys large language models", 2023),
    ("survey-growth", "automatic survey generation large language models", 2024),
    ("survey-growth", "proliferation of review articles literature reviews scientometric", 2015),
    ("review-inflation", "review article inflation number of review articles growth bibliometric", 2010),
    ("review-inflation", "too many review articles", 2010),
    ("llm-writing", "mapping the increasing use of LLMs in scientific papers", 2024),
    ("llm-writing", "excess vocabulary ChatGPT academic writing", 2024),
    ("llm-writing", "LLM-generated text arXiv abstracts prevalence", 2023),
    ("llm-writing", "large language models scientific output productivity preprints", 2024),
    ("preprint-policy", "preprint server policy change submissions effect", 2015),
    ("preprint-policy", "arXiv moderation rejection reclassification study", 2015),
    ("preprint-policy", "arXiv endorsement policy effect submissions", 2015),
    ("preprint-policy", "bioRxiv medRxiv screening policy submissions displacement", 2018),
    ("position-papers", "position papers machine learning conference track analysis", 2023),
    ("arxiv-scientometrics", "arXiv submissions growth computer science categories scientometric analysis", 2018),
]


def get(url, cache_name, pause):
    p = os.path.join(OUT, cache_name)
    if os.path.exists(p):
        return json.load(open(p, encoding="utf-8"))
    time.sleep(pause)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print("   FAILED", cache_name, repr(e)[:120])
        return None
    json.dump(data, open(p, "w", encoding="utf-8"))
    return data


def main():
    rows = []
    for label, q, yr in QUERIES:
        h = hashlib.md5(q.encode()).hexdigest()[:10]
        url = ("https://api.openalex.org/works?" + urllib.parse.urlencode({
            "search": q, "filter": f"from_publication_date:{yr}-01-01", "per-page": 25,
            "select": "id,doi,title,publication_date,type,cited_by_count,primary_location,authorships",
            "mailto": MAIL}))
        d = get(url, f"openalex_{h}.json", 1.0)
        for w in (d or {}).get("results", []):
            au = [a["author"]["display_name"] for a in w.get("authorships", [])[:3]]
            src = ((w.get("primary_location") or {}).get("source") or {}).get("display_name")
            lp = (w.get("primary_location") or {}).get("landing_page_url")
            rows.append(("openalex", label, q, w.get("publication_date"), w.get("title"), "; ".join(au),
                         src, w.get("doi") or lp, w.get("cited_by_count")))
        url = ("https://api.semanticscholar.org/graph/v1/paper/search?" + urllib.parse.urlencode({
            "query": q, "limit": 20, "year": f"{yr}-",
            "fields": "title,year,publicationDate,externalIds,venue,citationCount,authors"}))
        d = get(url, f"s2_{h}.json", 6.0)
        for w in (d or {}).get("data", []) or []:
            au = [a["name"] for a in (w.get("authors") or [])[:3]]
            ext = w.get("externalIds") or {}
            link = ("arXiv:" + ext["ArXiv"]) if "ArXiv" in ext else ext.get("DOI")
            rows.append(("s2", label, q, w.get("publicationDate") or w.get("year"), w.get("title"),
                         "; ".join(au), w.get("venue"), link, w.get("citationCount")))
    with open(os.path.join(OUT, "hits.tsv"), "w", encoding="utf-8") as f:
        f.write("source\tlabel\tquery\tdate\ttitle\tauthors\tvenue\tlink\tcitations\n")
        for r in rows:
            f.write("\t".join("" if x is None else str(x).replace("\t", " ").replace("\n", " ") for x in r) + "\n")
    print(len(rows), "hits written")


if __name__ == "__main__":
    main()
