"""Hand-screen for paper 09: writes data/clean/manual_exclusions.csv (documented title-level rules, then eyeballed lists)."""
import csv, re
import pandas as pd
m = pd.read_csv('../data/clean/master.csv', encoding='utf-8-sig', dtype=str, keep_default_na=False)
TXT = re.compile(r"text|writ|author|plagiar|essay|manuscript|paper|abstract|generated|detector|disclos|mill|fake|fabricat|peer|scholar|publication|publish|vocabular|delve|stylom|watermark|fingerprint|chatgpt|llm|corpus|journal|science|scientific|research|academic|integrity|citation|review|word|language|linguistic|lexical|prose|bibliograph|reference|policy|policies|editor|literature|phrase|retract|citing|cite", re.I)
EDU = re.compile(r"student|learner|efl\b|esl\b|classroom|teach|pedagog|undergraduate|lecturer|higher education|universit|school|tutor|curricul", re.I)
SCI = re.compile(r"scientific|scholarly|manuscript|publication|journal|peer|preprint|arxiv|research (paper|article|writing)|academic (writing|publish|paper|journal)", re.I)
rows = []
for r in m.itertuples():
    sl = set(r.sublits.split(';'))
    why = None
    if sl == {'C'}:
        if not TXT.search(r.title):
            why = 'rule X1: sub-literature C only and title shows no text/writing/publishing cue (AI applied to clinical, engineering or marketing tasks)'
        elif EDU.search(r.title) and not SCI.search(r.title):
            why = 'rule X2: sub-literature C only; education/classroom use of AI writing tools, not scientific writing'
    if sl == {'D'} and (re.search(r"RETRACTED ARTICLE", r.title) or re.search(r"moderation role|moderating|moderated|ECOWAS|mediating", r.title, re.I)):
        why = 'rule X3: sub-literature D only; statistical "moderation" or retracted article unrelated to editorial moderation'
    if why:
        rows.append((r.id, r.title, why))
with open('../data/clean/manual_exclusions.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['id', 'reason'])
    for i, t, y in rows: w.writerow([i, y])
with open('../data/clean/_manual_exclusions_titles.tsv', 'w', encoding='utf-8') as f:
    for i, t, y in rows: f.write(f"{y[:7]}\t{t}\n")
print(len(rows))
