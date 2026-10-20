"""Tiny HTML -> plain text converter (stdlib only) used to read saved policy pages.
Usage: python -I html2text.py page.html [start_marker]
"""
import sys, re, html
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.out = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "nav", "svg"):
            self.skip += 1
        if tag in ("p", "br", "li", "h1", "h2", "h3", "h4", "div", "tr", "time"):
            self.out.append("\n")
        if tag == "a":
            href = dict(attrs).get("href")
            if href and href.startswith("http"):
                self.out.append("[")
                self._href = href
            else:
                self._href = None
        if tag == "time":
            dt = dict(attrs).get("datetime")
            if dt:
                self.out.append(f"<time {dt}> ")
    def handle_endtag(self, tag):
        if tag in ("script", "style", "nav", "svg"):
            self.skip = max(0, self.skip - 1)
        if tag == "a" and getattr(self, "_href", None):
            self.out.append(f"]({self._href})")
            self._href = None
    def handle_data(self, d):
        if not self.skip:
            self.out.append(d)

def main():
    raw = open(sys.argv[1], encoding="utf-8", errors="replace").read()
    p = P()
    p.feed(raw)
    t = html.unescape("".join(p.out))
    t = re.sub(r"[ \t\r]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    if len(sys.argv) > 2 and sys.argv[2] in t:
        t = t[t.index(sys.argv[2]):]
    sys.stdout.reconfigure(encoding="utf-8")
    print(t)

if __name__ == "__main__":
    main()
