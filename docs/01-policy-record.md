# 01 - Policy record

Everything below was read on arXiv's own pages on 13 Oct 2026. The saved HTML of each page is in
`data/sources/` so the quotations can be re-checked. Quotations are exact (copied from the saved page text).
"Not stated" means the page does not say it; nothing is inferred.

## A. The rule itself

**Source:** "Attention Authors: Updated Practice for Review Articles and Position Papers in arXiv CS Category",
arXiv blog, by Kat Boboris, time-stamped 31 Oct 2025 09:41 US Eastern (13:41 UTC).
https://blog.arxiv.org/2025/10/31/attention-authors-updated-practice-for-review-articles-and-position-papers-in-arxiv-cs-category/
(saved: `data/sources/blog-2025-10-31.html`; full text opened.)

| Question | What the page says (exact words) |
|---|---|
| What changed | "arXiv's computer science (CS) category has updated its moderation practice with respect to review (or survey) articles and position papers. Before being considered for submission to arXiv's CS category, review articles and position papers must now be accepted at a journal or a conference and complete successful peer review." |
| Evidence required | "When submitting review articles or position papers, authors must include documentation of successful peer review to receive full consideration." and "When you submit to arXiv, please include the peer reviewed journal reference and DOI metadata. If you do not provide this, your review article or position paper will likely be rejected." |
| Consequence | "Review/survey articles or position papers submitted to arXiv without this documentation will be likely to be rejected and not appear on arXiv." |
| Workshops | "the review conducted at conference workshops generally does not meet the same standard of rigor of traditional peer review and is not enough to have your review article or position paper accepted to arXiv." |
| Stated reason | "This change is being implemented due to the unmanageable influx of review articles and position papers to arXiv CS." |
| LLM reason | "Generative AI / large language models have added to this flood by making papers - especially papers not introducing new research results - fast and easy to write." |
| Scale claimed | "we now receive hundreds of review articles every month. The advent of large language models have made this type of content relatively easy to churn out on demand, and the majority of the review articles we receive are little more than annotated bibliographies, with no substantial discussion of open research issues." |
| Is it a policy change? | "Technically, no! ... review articles and position papers are not (and have never been) listed as part of the accepted content types. Review articles and position papers have, in the past, only been accepted at moderator discretion" |
| Goals | "Help arXiv readers more easily find valuable review articles and position papers written by subject matter experts" and "Free up moderators to focus on the content types officially accepted by arXiv, reduce submission hold times" |
| After a rejection | "you can submit an appeal request to resubmit if your article has since completed a successful peer review process. Do not resubmit your position paper or review article without an accepted appeal." |
| What is exempt | "I have a scientific paper studying the impact of science and technology in society. Can I submit this to arXiv without peer review? Yes, arXiv has always released these types of scientific papers, for example in cs.CY or physics.soc-ph. These are scientific research papers and are not subject to this moderation practice change." |
| Other sections | "If other categories see a similar rise in LLM-written review articles and position papers, they may choose to change their moderation practices in a similar manner to better serve arXiv authors and readers. We will make these updates public if and when they do occur." |

### Points the announcement leaves open (important for the paper)
- **Start of enforcement: not stated as a date.** The post says the CS category "has updated" its practice
  and gives no grace period, so the only defensible reading is "in force by 31 Oct 2025". Whether moderators
  applied it earlier is not stated. The study therefore treats October 2025 as the last pre month and tests
  a wash-out of October-November 2025.
- **Coverage:** "arXiv's computer science (CS) category", meaning the whole CS section (all cs.* categories).
  The post does not say how cross-lists are handled (a survey with a non-CS primary category and a CS
  cross-list). That gap is exactly the displacement route RQ2(b) tests.
- **Definition of a review or position paper: none is given.** The only description is negative ("papers not
  introducing new research results", "little more than annotated bibliographies"). Classification is left
  to moderators. So the paper must define its own rubric (see `03-design.md`) and say so.
- **Form of the evidence:** journal reference and DOI in the metadata. So `journal-ref` and `doi` are the
  fields to check for compliance (RQ4).
- **No numbers** are given beyond "hundreds of review articles every month".

## B. arXiv's standing rules that the announcement relies on
- Content types page, https://info.arxiv.org/help/policies/content-types.html (saved; full text opened).
  The accepted list is: "Articles", "Theses", "Conference proceedings", "Books or book chapters",
  "Lecture notes", "Translations", "Comments and Reply to Comments". Review articles and position papers
  are in neither the accepted nor the not-accepted list. The not-accepted list includes "News items or
  opinion pieces", "Proposals for future research" and "Undergraduate or high school research".
- Moderation page, https://info.arxiv.org/help/moderation/index.html (saved; opened):
  - "the arXiv moderation process is not a peer-review process."
  - "Reclassification by our moderators ensures that submissions are posted to the most relevant category.
    Cross-lists may be added to other related categories, or they may be removed by moderators when the
    classification is deemed inappropriate."  (So final categories reflect moderators as well as authors.)
  - "Submissions that do not contain original or substantive research ... may be declined."
  - Generative-AI policy: authors must "report in their work any significant use of sophisticated tools ...
    we now include in particular text-to-text generative AI".

## C. Later clarifications or extensions of the review rule (to 13 Oct 2026)
- I listed every post on blog.arxiv.org from March 2025 to 8 Oct 2026 (index pages 1-4, saved) and read
  the titles. **No later post clarifies, extends or withdraws the review/position rule, and no post
  announces another section adopting it.** (Verified by title scan and by reading the policy posts below;
  a post whose title hides such content would be missed.)
- arXiv's news page (https://info.arxiv.org/new/index.html, saved) has no entry on it either.
- Not checked: arXiv's social-media accounts, mailing lists, and moderator statements in the press.

## D. Other arXiv changes that could confound a before/after comparison

| Date | Change | Source (all opened in full) | Why it matters |
|---|---|---|---|
| 2024 (month not stated) | Limit of 3 active submissions per submitter. "Since 2024, arXiv has had a limit of 3 active submissions at any time" | Rate-limit post of 1 Oct 2026 (below) | Background constraint through most of the window. |
| 10 Sep 2025 | "Submission 1.5" replaces AutoTeX; TeX Live 2025 | https://blog.arxiv.org/2025/09/10/attention-authors-submission-1-5-and-other-updates/ | Technical; could cause a small dip in submissions around Sep 2025. |
| 31 Oct 2025 | **CS review/position rule** | section A | The intervention. |
| 21 Nov 2025 (announced); 11 Feb 2026 (in force) | Full English version required for non-English papers. "Beginning February 11, 2026*, arXiv will require that all submissions have a full English-language version" | https://blog.arxiv.org/2025/11/21/upcoming-policy-change-to-non-english-language-paper-submissions/ | Small; all sections. |
| 10 Dec 2025 | Mathematics: institutional e-mail no longer enough for automatic endorsement. Reason: "stemming the flood of low-quality, non-scientific submissions to the arXiv Math section." | https://blog.arxiv.org/2025/12/10/updated-endorsement-policy-for-arxiv-mathematics/ | Hits the mathematics comparison series one month after the rule. |
| 21 Jan 2026 | **All sections:** "arXiv will no longer accept institutional email addresses ... as the sole qualifier of endorsement for new authors." New submitters need an institutional e-mail **and** prior authorship in the endorsement domain, or a personal endorser. | https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/ | The main confounder: three months after the rule, it reduces papers from first-time submitters in every section, CS included. A fall in CS surveys after Jan 2026 could come from this. Controls outside CS are hit too, which helps. |
| 1 Oct 2026 | Rate limit: "arXiv now limits submitters to up to two submissions per calendar month, with a limit of three total active submissions at any given time." | https://blog.arxiv.org/2026/10/01/updated-rate-limit-policy/ | Starts the day after the study window ends (30 Sep 2026). A reason not to extend the window without modelling it. |
| - | Category reorganisation in 2025-26 | none found on the blog or news page | The old aliases matter instead: cs.SY is stored as eess.SY and cs.NA as math.NA in the API metadata. |

Useful context from the 1 Oct 2026 post (exact): "In September of 2024, arXiv received 20,569 submissions.
This September, arXiv received 40,363 submissions"; "Increases over the past two years in cs.AI (over 6X
increase)"; "Our moderators are observing an increase in thin papers of narrow scope, as well as 'salami'
papers ... There is also a marked increase in dense, AI-written papers."
- These are **submission** counts (including rejected papers), not announced papers. They cannot be compared
  directly with this study's counts of papers that appeared.

## E. Data-access rules followed
- API Terms of Use, https://info.arxiv.org/help/api/tou.html (saved; opened in full):
  - "When using the legacy APIs (including OAI-PMH, RSS, and the arXiv API), make no more than one request
    every three seconds, and limit requests to a single connection at a time."
  - "You are free to use descriptive metadata about arXiv e-prints under the terms of the Creative Commons
    Universal (CC0 1.0) Public Domain Declaration."
  - Allowed: "Retrieve, store, transform, and share descriptive metadata about arXiv e-prints."
  - Not allowed: "Attempt to circumvent rate limits."; representing the project as endorsed by arXiv.
- OAI-PMH page, https://info.arxiv.org/help/oa/index.html (saved; opened): base URL
  `https://oaipmh.arxiv.org/oai`; `arXivRaw` format "Includes history for previous versions of the paper";
  "The OAI-PMH interface does not support selective harvesting based on submission date."
- Bulk data page, https://info.arxiv.org/help/bulk_data.html (saved; not needed for metadata).
- What the harvester does: one request at a time, 3.2 s pause, User-Agent with a contact e-mail, metadata
  only, every response cached so nothing is fetched twice. See `code/README.md`.
- One lapse to record: while the harvester was running I fetched two `arxiv.org/list/cs/...` pages to
  cross-check counts. The API began returning HTTP 429 at that moment and the harvester backed off. No
  other parallel requests to arXiv hosts were made after that.

## F. Not verified
- When moderators actually began refusing surveys (no arXiv page gives a date other than the announcement).
- How many submissions were refused under the rule (arXiv has published no figure that I found; the 2025
  annual report PDF is saved in `data/sources/` but has not been read).
- Press coverage and reactions (not opened; web search was kept for other uses).
- Whether any non-CS section quietly adopted the same practice.
