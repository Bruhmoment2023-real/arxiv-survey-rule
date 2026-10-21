# Paper 09 check: are the survey / position-paper labels right?

## What this is for
The paper tests its survey-detecting rule against 400 arXiv computer-science papers that were labelled once,
from title and abstract, by a first pass (the AI assistant). The paper says a second person is needed to
make the "how many surveys does the rule miss" number trustworthy. You are checking those labels.
You will see the first-pass answer, so this is an author check of the labels, not a blind re-labelling,
and the paper will say exactly that.

## What to do (file: 09-check-sheet.xlsx)
1. Open the sheet "How to" once and read the five labels (S, P, M, U, N) and the tie-break rules.
2. Go to the sheet "Core 120". For each row:
   1. Read the title and the abstract. If it is unclear, click the arXiv link.
   2. Read the first-pass label and what it means (the two columns next to it).
   3. In the yellow column "Your Y/N", pick **Y** if the label is right, **N** if it is wrong.
   4. If you picked N, pick the right label (S, P, M, U or N) in "Correct label".
   5. Add a short note if you like (useful for every N).
3. Save the file.

The key question on every row: is the paper's main job to review existing work (S) or to argue a position (P)?
If not, it is N (or M if it reviews and also reports real new experiments).

## How long
- Core 120: about 1 to 1.5 hours (30-40 seconds a row).
- "Extra 280 (optional)": the rest of the 400, another 2.5 to 3 hours. Only if you want to; any part you fill is used.
  The rows that matter most for the "missed surveys" number are the ones labelled N, so a quick pass over those
  in Extra 280 is the most useful extra time.

## When unsure
Put **?** in "Your Y/N" and write why in "Your note". Do not guess. If it is between S and P, either is fine.

## When done
Save the file and tell Claude: **09 check done**
