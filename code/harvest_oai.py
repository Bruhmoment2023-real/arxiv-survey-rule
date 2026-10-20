"""READY TO RUN (not run in the first phase): full metadata harvest through arXiv's OAI-PMH interface.

Why: OAI-PMH `arXivRaw` gives EVERY paper in a set (no keyword net) and the date of EVERY version,
which the legacy API does not. It is the cleanest source for the final paper.
Why not yet: arXiv says OAI-PMH "does not support selective harvesting based on submission date", so a
set has to be harvested whole. One page of about 1,000 records is about 2.5 MB (measured 13 Oct 2026 on
the `econ` set), so `cs` alone is roughly 3 GB - over the 1 GB budget of the first phase.

Rules followed (https://info.arxiv.org/help/api/tou.html): one request at a time, >= 3 s apart (5 s here),
User-Agent with contact address, metadata only. Resumable: every page is cached with its resumption token;
restart continues from the last token. Tokens "expire daily", so if a set is interrupted for more than a
day the script restarts that set with from=<last datestamp seen>.

Usage:  python harvest_oai.py cs            (then: stat eess q-bio econ q-fin physics:physics math)
Output: data/raw/oai/<set>/page_000001.xml.gz ... and data/raw/oai/<set>/state.json
Only papers whose identifier is 2201.xxxxx or later are needed; filter by id when parsing.
"""
import sys, os, time, gzip, json, re, urllib.parse, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://oaipmh.arxiv.org/oai"
UA = "arxiv-survey-rule-study/0.1 (mailto:research-contact-withheld@example.invalid)"
DELAY = 5.0
LOCK = os.path.join(ROOT, "data", "harvest.lock")   # shared with harvest_api.py: never run both


def get(params):
    url = BASE + "?" + urllib.parse.urlencode(params)
    for attempt in range(60):
        time.sleep(DELAY)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=300) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            wait = int(e.headers.get("Retry-After", 120)) if e.code in (429, 503) else 60
            print(f"   HTTP {e.code}; waiting {wait}s", flush=True)
            time.sleep(wait)
        except Exception as e:
            print("   ", repr(e)[:100], "; waiting 60s", flush=True)
            time.sleep(60)
    raise RuntimeError("giving up")


def main():
    setspec = sys.argv[1]
    if os.path.exists(LOCK) and time.time() - os.path.getmtime(LOCK) < 900:
        sys.exit("another harvester is running (data/harvest.lock is fresh)")
    d = os.path.join(ROOT, "data", "raw", "oai", setspec.replace(":", "_"))
    os.makedirs(d, exist_ok=True)
    sp = os.path.join(d, "state.json")
    st = json.load(open(sp)) if os.path.exists(sp) else {"page": 0, "token": None, "last_datestamp": None, "done": False}
    if st["done"]:
        print("already complete")
        return
    try:
        while True:
            open(LOCK, "w").write(str(os.getpid()))
            if st["token"]:
                params = {"verb": "ListRecords", "resumptionToken": st["token"]}
            else:
                params = {"verb": "ListRecords", "metadataPrefix": "arXivRaw", "set": setspec}
                if st["last_datestamp"]:
                    params["from"] = st["last_datestamp"]
            data = get(params)
            if b"badResumptionToken" in data:          # token expired: restart from last datestamp
                st["token"] = None
                continue
            st["page"] += 1
            with gzip.open(os.path.join(d, f"page_{st['page']:06d}.xml.gz"), "wb") as f:
                f.write(data)
            stamps = re.findall(rb"<datestamp>([^<]+)</datestamp>", data)
            if stamps:
                st["last_datestamp"] = max(stamps).decode()
            m = re.search(rb"<resumptionToken[^>]*>([^<]*)</resumptionToken>", data)
            st["token"] = m.group(1).decode() if m and m.group(1) else None
            st["done"] = st["token"] is None
            json.dump(st, open(sp, "w"))
            print(f"[{setspec}] page {st['page']}: {data.count(b'<record>')} records, up to {st['last_datestamp']}", flush=True)
            if st["done"]:
                break
    finally:
        if os.path.exists(LOCK):
            os.remove(LOCK)


if __name__ == "__main__":
    main()
