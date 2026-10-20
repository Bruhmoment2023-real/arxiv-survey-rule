"""Prior-work search, second pass: Semantic Scholar (with patient retries) and Crossref.
OpenAlex returned HTTP 429 "Insufficient budget" for this IP on 13 Oct 2026, so it is not used here.
Caches every response in data/priorwork/. Output: data/priorwork/hits2.tsv
"""
import os, json, time, urllib.parse, urllib.request, urllib.error, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "priorwork")
MAIL = "research-contact-withheld@example.invalid"
UA = f"arxiv-survey-rule-study/0.1 (mailto:{MAIL})"

S2_QUERIES = [
    ("policy-effect", "arXiv review articles position papers peer review policy"),
    ("policy-effect", "arXiv moderation survey papers policy change effect"),
    ("policy-effect", "arXiv computer science survey papers ban peer review requirement"),
    ("policy-effect", "survey paper flood arXiv large language models"),
    ("survey-growth", "AI-generated survey papers research community"),
    ("survey-growth", "automatic literature survey generation LLM AutoSurvey"),
    ("survey-growth", "explosion of survey papers machine learning meta-analysis of surveys"),
    ("survey-growth", "survey papers arXiv growth bibliometric analysis computer science"),
    ("review-inflation", "growth of review articles bibliometric proportion of reviews"),
    ("review-inflation", "mass production of systematic reviews and meta-analyses"),
    ("review-inflation", "review articles citation advantage scientometrics research agenda"),
    ("llm-writing", "Mapping the increasing use of LLMs in scientific papers"),
    ("llm-writing", "Delving into ChatGPT usage in academic writing through excess vocabulary"),
    ("llm-writing", "Scientific production in the era of large language models"),
    ("llm-writing", "Is ChatGPT transforming academics' writing style"),
    ("llm-writing", "LLM-generated text detection arXiv abstracts prevalence over time"),
    ("preprint-policy", "arXiv moderation system study reclassification rejection"),
    ("preprint-policy", "preprint server screening policy change submissions interrupted time series"),
    ("preprint-policy", "arXiv endorsement policy submissions effect"),
    ("preprint-policy", "bioRxiv medRxiv submission policy change effect on preprints"),
    ("preprint-policy", "journal policy change interrupted time series submissions displacement"),
    ("position-papers", "position paper track machine learning conference"),
    ("arxiv-scientometrics", "arXiv submission growth computer science categories analysis"),
    ("arxiv-scientometrics", "NLLG quarterly arXiv report"),
    ("classifier", "identifying review articles automatically classification document type survey papers"),
]
CROSSREF_QUERIES = [
    ("review-inflation", "growth of review articles proportion of reviews bibliometric"),
    ("review-inflation", "mass production of redundant misleading conflicted systematic reviews meta-analyses"),
    ("review-inflation", "studying review articles in scientometrics and beyond research agenda"),
    ("preprint-policy", "arXiv moderation"),
    ("preprint-policy", "preprint server policy submissions interrupted time series"),
    ("llm-writing", "excess vocabulary LLM-assisted writing biomedical publications"),
]


def get(url, cache, pause, tries=6):
    p = os.path.join(OUT, cache)
    if os.path.exists(p):
        return json.load(open(p, encoding="utf-8"))
    for a in range(tries):
        time.sleep(pause * (a + 1))
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.loads(r.read().decode("utf-8"))
            json.dump(data, open(p, "w", encoding="utf-8"))
            return data
        except urllib.error.HTTPError as e:
            print("   ", e.code, cache, "try", a + 1, flush=True)
        except Exception as e:
            print("   ", repr(e)[:80], cache, flush=True)
    return None


def main():
    rows = []
    for label, q in S2_QUERIES:
        h = hashlib.md5(q.encode()).hexdigest()[:10]
        url = "https://api.semanticscholar.org/graph/v1/paper/search?" + urllib.parse.urlencode({
            "query": q, "limit": 15, "year": "2015-",
            "fields": "title,year,publicationDate,externalIds,venue,citationCount,authors"})
        d = get(url, f"s2b_{h}.json", 8)
        for w in (d or {}).get("data") or []:
            ext = w.get("externalIds") or {}
            link = ("arXiv:" + ext["ArXiv"]) if "ArXiv" in ext else ext.get("DOI")
            rows.append(("s2", label, q, w.get("publicationDate") or w.get("year"), w.get("title"),
                         "; ".join(a["name"] for a in (w.get("authors") or [])[:3]), w.get("venue"), link,
                         w.get("citationCount")))
    for label, q in CROSSREF_QUERIES:
        h = hashlib.md5(q.encode()).hexdigest()[:10]
        url = "https://api.crossref.org/works?" + urllib.parse.urlencode({
            "query.bibliographic": q, "rows": 10, "mailto": MAIL,
            "select": "DOI,title,author,issued,container-title,is-referenced-by-count"})
        d = get(url, f"crossref_{h}.json", 2)
        for w in ((d or {}).get("message") or {}).get("items", []):
            yr = (w.get("issued", {}).get("date-parts") or [[None]])[0][0]
            rows.append(("crossref", label, q, yr, (w.get("title") or [""])[0],
                         "; ".join(a.get("family", "") for a in (w.get("author") or [])[:3]),
                         (w.get("container-title") or [""])[0], w.get("DOI"), w.get("is-referenced-by-count")))
    with open(os.path.join(OUT, "hits2.tsv"), "w", encoding="utf-8") as f:
        f.write("source\tlabel\tquery\tdate\ttitle\tauthors\tvenue\tlink\tcitations\n")
        for r in rows:
            f.write("\t".join("" if x is None else str(x).replace("\t", " ").replace("\n", " ") for x in r) + "\n")
    print(len(rows), "hits written")


if __name__ == "__main__":
    main()
