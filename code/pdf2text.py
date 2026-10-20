"""PDF -> text (pypdf). Usage: .venv\Scripts\python -I code\pdf2text.py in.pdf out.txt"""
import sys
from pypdf import PdfReader
r = PdfReader(sys.argv[1])
open(sys.argv[2], "w", encoding="utf-8").write("\n\n".join((p.extract_text() or "") for p in r.pages))
print(len(r.pages), "pages")
