"""Parse cached Atom responses (data/raw/<task>/*.xml.gz) into one de-duplicated JSON-lines file.

Usage: python parse.py days   -> data/days.jsonl.gz
       python parse.py net    -> data/net.jsonl.gz
Fields: id, v (latest version number), published (v1 timestamp, UTC), updated (latest version
timestamp), title, abstract, primary, cats (all categories), comment, journal_ref, doi, n_authors.
Note: the API returns the metadata of the LATEST version only.
"""
import sys, os, glob, gzip, json, re
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = "{http://www.w3.org/2005/Atom}"
X = "{http://arxiv.org/schemas/atom}"


def clean(s):
    return re.sub(r"\s+", " ", s or "").strip()


def parse_file(path):
    with gzip.open(path, "rb") as f:
        data = f.read()
    root = ET.fromstring(data)
    for e in root.iter(A + "entry"):
        full = e.findtext(A + "id").rsplit("/abs/", 1)[1]
        m = re.match(r"(.+?)v(\d+)$", full)
        yield {
            "id": m.group(1), "v": int(m.group(2)),
            "published": e.findtext(A + "published"), "updated": e.findtext(A + "updated"),
            "title": clean(e.findtext(A + "title")), "abstract": clean(e.findtext(A + "summary")),
            "primary": e.find(X + "primary_category").get("term"),
            "cats": [c.get("term") for c in e.findall(A + "category")],
            "comment": clean(e.findtext(X + "comment")),
            "journal_ref": clean(e.findtext(X + "journal_ref")),
            "doi": clean(e.findtext(X + "doi")),
            "n_authors": len(e.findall(A + "author")),
        }


def main():
    task = sys.argv[1]
    seen, n = set(), 0
    out = os.path.join(ROOT, "data", task + ".jsonl.gz")
    with gzip.open(out + ".tmp", "wt", encoding="utf-8") as f:
        for p in sorted(glob.glob(os.path.join(ROOT, "data", "raw", task, "*_s*.xml.gz"))):
            for r in parse_file(p):
                if r["id"] in seen:
                    continue
                seen.add(r["id"])
                if task == "days":
                    r["sample_day"] = os.path.basename(p).split("_")[1]
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
                n += 1
    os.replace(out + ".tmp", out)
    print(task, n, "records ->", out)


if __name__ == "__main__":
    main()
