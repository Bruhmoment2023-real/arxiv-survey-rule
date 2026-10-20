"""Resumable, rate-limited harvester for the arXiv legacy API (export.arxiv.org/api/query).

Follows arXiv's API Terms of Use (https://info.arxiv.org/help/api/tou.html):
  * no more than one request every three seconds  -> we wait 3.2 s after every response
  * a single connection at a time                  -> strictly sequential, one process
  * identifies itself with a User-Agent and contact address
Only descriptive metadata (CC0) is fetched. No PDFs or source files.

Every raw response is cached as gzip XML under data/raw/<task>/ . A request whose cache file
exists is never repeated, so the script can be stopped (Ctrl-C) and restarted at any time.
A lock file prevents two copies running at once (which would break the rate limit).

Tasks (run in the order given on the command line):
  counts_core   monthly totals for the main category groups (1 request per group-month)
  net           full metadata for every paper matching the broad candidate net
  days          full metadata for ALL papers in the study group G on one random day per month
  counts_cs     monthly totals for the largest individual cs.* categories (optional)

Usage:  python harvest_api.py counts_core net days counts_cs  [--start 2022-01] [--end 2026-09]
                                [--groups cs_any,math_notcs] [--delay 5]
"""
import sys, os, time, gzip, json, random, calendar, re, urllib.parse, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
API = "https://export.arxiv.org/api/query"
UA = "arxiv-survey-rule-study/0.1 (mailto:research-contact-withheld@example.invalid)"
DELAY = [5.0]        # seconds between requests (ToU: at most one every three seconds; we use 5)
PAGE = 1000
LOCK = os.path.join(ROOT, "data", "harvest.lock")
SEED = 20251031      # date of the announcement; fixes the random sample days

# ---------------------------------------------------------------- category groups
G_PARTS = ["cat:cs.*", "cat:stat.*", "cat:eess.*", "cat:q-bio.*", "cat:econ.*", "cat:q-fin.*",
           "cat:physics.soc-ph"]
G = "(" + " OR ".join(G_PARTS) + ")"
PHYS = "(cat:astro-ph.* OR cat:cond-mat.* OR cat:hep-th OR cat:hep-ph OR cat:quant-ph OR cat:gr-qc)"
GROUPS_CORE = {
    "cs_any":      "cat:cs.*",
    "G_any":       G,
    "stat_notcs":  "(cat:stat.* ANDNOT cat:cs.*)",
    "eess_notcs":  "(cat:eess.* ANDNOT cat:cs.*)",
    "qbio_notcs":  "(cat:q-bio.* ANDNOT cat:cs.*)",
    "econ_notcs":  "(cat:econ.* ANDNOT cat:cs.*)",
    "qfin_notcs":  "(cat:q-fin.* ANDNOT cat:cs.*)",
    "socph_notcs": "(cat:physics.soc-ph ANDNOT cat:cs.*)",
    "math_notcs":  "(cat:math.* ANDNOT cat:cs.*)",
    "phys_notcs":  "(" + PHYS + " ANDNOT cat:cs.*)",
}
CS_CATS = ["cs.AI", "cs.CL", "cs.LG", "cs.CV", "cs.CY", "cs.SE", "cs.CR", "cs.HC", "cs.RO", "cs.IR"]
GROUPS_CS = {c: "cat:" + c for c in CS_CATS}

# ---------------------------------------------------------------- the candidate net
# The API search index stems words and drops stop-words, so each entry is a root token.
# The net must be a SUPERSET of everything the rule classifier (classify.py) can fire on;
# check_net.py verifies this on the full-day samples.
TI_CORE = ["survey", "review", "overview", "roadmap", "taxonomy", "perspective", "tutorial",
           "primer", '"position paper"']                      # searched in ALL of arXiv
TI_G = ["position", "landscape", "sok", "viewpoint", "manifesto", "vision",
        "challenges", "opportunities", "retrospective", "introduction", "guide",
        "directions", "problems", "should", "must", "need", "systematization",
        '"state of the art"', "mapping", "lessons", "rethinking", "call", "trends",
        "advances", "progress"]                               # searched only inside group G
ABS_TERMS = ["survey", "review", "overview", "taxonomy", "tutorial", "roadmap", "argue",
             "advocate", '"position paper"', "perspective", "viewpoint", "manifesto",
             '"vision paper"', "contend", '"call for"', "primer", "systematization"]
NET = ("((" + " OR ".join("ti:" + t for t in TI_CORE) + ") OR (" + G + " AND (" +
       " OR ".join(["ti:" + t for t in TI_G] + ["abs:" + t for t in ABS_TERMS]) + ")))")


def months(start, end):
    y, m = map(int, start.split("-"))
    ey, em = map(int, end.split("-"))
    while (y, m) <= (ey, em):
        yield y, m
        m += 1
        if m == 13:
            y, m = y + 1, 1


def drange(y, m, d1, d2):
    return f"submittedDate:[{y}{m:02d}{d1:02d}0000 TO {y}{m:02d}{d2:02d}2359]"


LAST = [0.0]


def fetch(query, start, maxr, sort=True):
    """One polite request. Returns response bytes. Retries with back-off on errors."""
    params = {"search_query": query, "start": start, "max_results": maxr}
    if sort:
        params["sortBy"] = "submittedDate"
        params["sortOrder"] = "ascending"
    url = API + "?" + urllib.parse.urlencode(params)
    for attempt in range(60):
        wait = DELAY[0] - (time.time() - LAST[0])
        if wait > 0:
            time.sleep(wait)
        back = min(600, 20 * (2 ** min(attempt, 5)))
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=180) as r:
                data = r.read()
            LAST[0] = time.time()
            if os.path.exists(LOCK):
                os.utime(LOCK)          # keep the lock fresh while we are alive
            if b"<opensearch:totalResults" in data:
                return data
            err = "no totalResults in response"
        except urllib.error.HTTPError as e:
            LAST[0] = time.time()
            err = f"HTTP {e.code}"
            if e.code == 429:           # rate limited (the limit is shared by everything on this
                back = 120              # network address): wait two minutes, flat, then try again
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            LAST[0] = time.time()
            err = repr(e)
        print(f"   retry {attempt + 1} after {back}s: {err}", flush=True)
        if os.path.exists(LOCK):
            os.utime(LOCK)
        time.sleep(back)
    raise RuntimeError("giving up on " + url)


def total_of(data):
    m = re.search(rb"<opensearch:totalResults[^>]*>(\d+)<", data)
    return int(m.group(1))


def n_entries(data):
    return data.count(b"<entry>")


def cache_path(task, key):
    d = os.path.join(RAW, task)
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, key + ".xml.gz")


def save(path, data):
    tmp = path + ".tmp"
    with gzip.open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, path)


def load(path):
    with gzip.open(path, "rb") as f:
        return f.read()


def do_counts(task, groups, start, end):
    out = os.path.join(ROOT, "data", task + ".json")
    res = json.load(open(out)) if os.path.exists(out) else {}
    for y, m in months(start, end):
        last = calendar.monthrange(y, m)[1]
        for g, q in groups.items():
            key = f"{g}|{y}-{m:02d}"
            if key in res:
                continue
            data = fetch(q + " AND " + drange(y, m, 1, last), 0, 1, sort=False)
            res[key] = total_of(data)
            print(f"[{task}] {key} = {res[key]}", flush=True)
            tmp = out + ".tmp"
            json.dump(res, open(tmp, "w"), indent=0, sort_keys=True)
            os.replace(tmp, out)


def do_paged(task, key, query):
    """Fetch every record of `query` in pages; each page cached. Returns (total, got)."""
    start, total, got = 0, None, 0
    while True:
        p = cache_path(task, f"{key}_s{start:06d}")
        if os.path.exists(p):
            data = load(p)
        else:
            data = None
            for attempt in range(5):          # the API sometimes returns a short/empty page
                data = fetch(query, start, PAGE)
                t = total_of(data)
                expect = min(PAGE, max(0, t - start))
                if n_entries(data) >= expect:
                    break
                print(f"   short page ({n_entries(data)}/{expect}) for {key} s{start}; retry", flush=True)
                time.sleep(30 * (attempt + 1))
            else:
                print(f"   !! page still short, NOT cached: {key} s{start}", flush=True)
                return total_of(data), got
            save(p, data)
        total = total_of(data)
        got += n_entries(data)
        start += PAGE
        if start >= total:
            return total, got


def do_net(start, end):
    for y, m in months(start, end):
        last = calendar.monthrange(y, m)[1]
        for d1, d2 in ((1, 7), (8, 14), (15, 21), (22, last)):
            key = f"net_{y}{m:02d}{d1:02d}-{d2:02d}"
            done = cache_path("net", key + ".done")
            if os.path.exists(done):
                continue
            total, got = do_paged("net", key, NET + " AND " + drange(y, m, d1, d2))
            print(f"[net] {key}: {got}/{total}", flush=True)
            if got >= total:
                save(done, json.dumps({"total": total, "got": got}).encode())


def sample_days(start, end):
    rng = random.Random(SEED)
    days = []
    for y, m in months(start, end):
        days.append((y, m, rng.randint(1, calendar.monthrange(y, m)[1])))
    return days


def do_days(start, end):
    days = sample_days("2022-01", "2026-09")      # fixed list, independent of --start/--end
    json.dump([f"{y}-{m:02d}-{d:02d}" for y, m, d in days],
              open(os.path.join(ROOT, "data", "sample_days.json"), "w"))
    # visit days nearest the policy date first so a partial run is still balanced
    days.sort(key=lambda t: abs((t[0] - 2025) * 12 + t[1] - 10.5))
    for y, m, d in days:
        key = f"day_{y}{m:02d}{d:02d}"
        done = cache_path("days", key + ".done")
        if os.path.exists(done):
            continue
        total, got = do_paged("days", key, G + " AND " + drange(y, m, d, d))
        print(f"[days] {key}: {got}/{total}", flush=True)
        if got >= total:
            save(done, json.dumps({"total": total, "got": got}).encode())


def main():
    args = sys.argv[1:]
    start, end = "2022-01", "2026-09"
    if "--start" in args:
        start = args[args.index("--start") + 1]
    if "--end" in args:
        end = args[args.index("--end") + 1]
    if "--delay" in args:
        DELAY[0] = max(3.2, float(args[args.index("--delay") + 1]))
    groups = dict(GROUPS_CORE)
    if "--groups" in args:
        want = args[args.index("--groups") + 1].split(",")
        groups = {g: GROUPS_CORE[g] for g in want}
    tasks = [a for a in args if a in ("counts_core", "net", "days", "counts_cs")]
    lock = LOCK
    if os.path.exists(lock) and time.time() - os.path.getmtime(lock) < 900:
        sys.exit("another harvester seems to be running (data/harvest.lock is fresh); stop it first")
    try:
        for t in tasks:
            open(lock, "w").write(str(os.getpid()))
            print(f"=== task {t} {start}..{end}", flush=True)
            if t == "counts_core":
                do_counts("counts_core", groups, start, end)
            elif t == "counts_cs":
                do_counts("counts_cs", GROUPS_CS, start, end)
            elif t == "net":
                do_net(start, end)
            elif t == "days":
                do_days(start, end)
        print("=== all requested tasks finished", flush=True)
    finally:
        if os.path.exists(lock):
            os.remove(lock)


if __name__ == "__main__":
    main()
