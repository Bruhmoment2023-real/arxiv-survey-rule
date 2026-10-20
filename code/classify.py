"""Transparent title-and-abstract rules for review (survey) articles and position papers.

RULES VERSION 1.0 - frozen on 2026-10-13 BEFORE any post-policy count was computed
(see 03-design.md). Do not edit the patterns; add a new version instead.

classify(title, abstract) -> dict with
  strict  (bool)  primary measure: paper self-identifies as a survey/review or a position paper
  broad   (bool)  strict OR weaker cues (sensitivity measure)
  kind    'survey' | 'position' | 'both' | ''   (for strict)
  rules   list of rule names that fired
Everything is case-insensitive and applied to the LATEST-version title/abstract.
"""
import re

F = re.I

# ---- phrases where "survey"/"review" does NOT mean a literature survey -------------------
NOT_LIT_SURVEY = re.compile(
    r"survey (data|respondents?|responses?|participants?|experiments?|questions?|questionnaires?|"
    r"instruments?|results|study|studies|sampling|weights?|design|methodology|research|items?|"
    r"mode|non-?response|estimat\w+|answers?)|"
    r"(user|online|large-scale|national|household|social|public|opinion|customer|employee|"
    r"developer|practitioner|expert|student|community|cross-sectional|longitudinal|panel|"
    r"sky|galaxy|redshift|imaging|spectroscopic|geological|seismic|aerial|site|field|health|"
    r"labou?r|population|election|census|telephone|web|mail|pilot|empirical) surveys?|"
    r"survey of (\d[\d,]* )?(users|developers|practitioners|students|researchers|participants|"
    r"respondents|experts|engineers|adults|people|professionals|teachers|workers|clinicians)|"
    r"surveys? (of|with|among) \d|surveyed|survey propagation|survey sampling", F)
NOT_LIT_REVIEW = re.compile(
    r"(code|peer|peer-|pull request|design|security|product|customer|user|movie|online|app|"
    r"restaurant|hotel|book|legal|judicial|document|contract|performance|safety|ethics|ethical|"
    r"human|expert|manual|rapid|annual|code-|fake|amazon|yelp|imdb|paper|manuscript|medical record|"
    r"chart|utilization|post-incident|after-action) reviews?|reviews? (comments?|process|"
    r"processes|generation|helpfulness|rating|ratings|sentiment|datasets?|texts?|spam|scores?|"
    r"board|boards|committee|time|workload|assignment)|reviewer|under review|reviewing", F)

# ---- STRICT survey rules ------------------------------------------------------------------
T_SURVEY = re.compile(r"\b(surveys?|surveying)\b", F)
T_REVIEW = re.compile(r"\b(reviews?|reviewing)\b", F)
T_STRONG = re.compile(
    r"\b(systematic|literature|scoping|narrative|critical|comprehensive|state[- ]of[- ]the[- ]art|"
    r"brief|short|mini|concise|comparative|technical|integrative|umbrella|structured|"
    r"methodological|historical|tertiary|rapid|a|an|in)[- ](literature[- ])?(reviews?|surveys?)\b|"
    r"\b(review|survey)\s+(of|on|and|for|from|with|about|in)\b|[:\-]\s*(a\s+|an\s+)?[\w\- ]*\b(review|survey)\s*$|"
    r"^\s*(a\s+)?(review|survey)\b|\bsok\b\s*:|systemati[sz]ation of knowledge|"
    r"\bsystematic (literature )?mapping\b|\bmapping study\b", F)
A_SELF = re.compile(
    r"\b(this|our|the present|present) (survey|review|sok|systematic review|literature review|"
    r"overview article|review article|review paper|survey paper|tutorial)\b|"
    r"\bin this (comprehensive |systematic |short |brief )?(survey|review)\b|"
    r"\bwe (comprehensively |systematically |critically |briefly |thoroughly |first )?(survey|review)\b(?! (the )?(related work|our|prior work in section))|"
    r"\bthis (paper|article|work|study|manuscript|chapter|report|monograph) "
    r"(surveys|reviews|presents? an? (comprehensive |systematic |extensive |thorough |detailed |critical |brief |up-to-date |structured )*(survey|review|literature review|overview) of|"
    r"provides? an? (comprehensive |systematic |extensive |thorough |detailed |critical |brief |up-to-date |structured )*(survey|review|literature review|overview) of|"
    r"offers? an? (comprehensive |systematic |extensive |thorough |detailed |critical |brief |up-to-date |structured )*(survey|review|literature review|overview) of|"
    r"is an? (comprehensive |systematic |extensive |thorough |detailed |critical |brief |up-to-date |structured )*(survey|review) (of|on))|"
    r"\b(comprehensive|systematic|extensive|thorough|up-to-date|structured|holistic) (literature )?(survey|review)\b|"
    r"\bsystematic(ally)? (literature )?(review|mapping)\b|\bsystemati[sz]ation of knowledge\b|"
    r"\b(survey|review) (paper|article)\b|\bfirst (comprehensive |systematic )?(survey|review)\b", F)

# ---- STRICT position rules ----------------------------------------------------------------
T_POSITION = re.compile(r"^\s*position\s*(paper)?\s*:|\bposition (paper|statement)\b|"
                        r"\b(a|an) (position|vision|perspective|opinion|viewpoint) (paper|piece|article)\b|"
                        r"^\s*(perspective|viewpoint|opinion|commentary|manifesto)\s*:|\bmanifesto\b", F)
A_POSITION = re.compile(r"\b(position|vision|perspective|opinion|viewpoint) (paper|piece|article)\b|"
                        r"\bthis (position|perspective|viewpoint|commentary|essay|manifesto|opinion)\b|"
                        r"\bin this (position|perspective|viewpoint|commentary|essay)\b|"
                        r"\bthis paper (takes|argues for) the position\b|\bwe take the position\b", F)

# ---- BROAD (weak) cues ----------------------------------------------------------------------
T_WEAK = re.compile(
    r"\b(an|the) overview\b|\boverview of\b|:\s*(an? )?overview\b|\broadmap\b|\btaxonomy\b|"
    r"\b(a|an) (perspective|primer|tutorial|retrospective|introduction|guide)\b|\bperspectives?\b|"
    r"\bchallenges and (opportunities|future|open|directions|solutions|prospects)\b|"
    r"\bopportunities and challenges\b|\bopen (problems|challenges|questions)\b|"
    r"\bfuture (directions|research|challenges|prospects)\b|\brecent (advances|progress|trends|developments)\b|"
    r"\bstate[- ]of[- ]the[- ]art (and|in)\b|\blandscape\b|\bwhere (are we|do we stand)\b|"
    r"\b(should|must|need to|needs to|we need)\b|\brethinking\b|\ba call (to|for)\b|\bthe case (for|against)\b|"
    r"\blessons learned\b|\bviewpoint\b|\bvision\s*:|\bprimer\b|\btutorial\b", F)
A_WEAK = re.compile(
    r"\bwe argue\b|\b(this|the) (paper|article|work|essay) argues\b|\bwe (advocate|contend|posit that|call for|make the case)\b|"
    r"\bliterature review\b|\bwe (provide|present|give|offer) an? (comprehensive |systematic |broad |brief |high-level |detailed |extensive |unified )*(overview|taxonomy|roadmap|tutorial|primer)\b|"
    r"\bthis (paper|article|work|chapter) (provides|presents|gives|offers) an? (comprehensive |systematic |broad |brief |high-level |detailed |extensive |unified )*(overview|taxonomy|roadmap|tutorial|primer)\b|"
    r"\bthis (tutorial|overview|primer|roadmap|perspective)\b|\bwe (summari[sz]e|synthesi[sz]e|categori[sz]e|organi[sz]e) (the )?(existing|recent|current|prior|related) (work|works|literature|research|studies|methods|approaches)\b|"
    r"\b(existing|recent|current) (literature|studies|works|research) (is|are) (reviewed|surveyed|summari[sz]ed)\b", F)


def classify(title, abstract):
    t, a = title or "", abstract or ""
    rules = []
    # strict survey, title
    t_wo_survey = NOT_LIT_SURVEY.sub(" ", t)
    t_wo_review = NOT_LIT_REVIEW.sub(" ", t)
    if T_SURVEY.search(t_wo_survey):
        rules.append("T_survey")
    if T_REVIEW.search(t_wo_review) and T_STRONG.search(t_wo_review):
        rules.append("T_review")
    if re.search(r"\bsok\b\s*:|systemati[sz]ation of knowledge|\bmapping study\b|systematic (literature )?mapping", t, F):
        rules.append("T_sok")
    # strict survey, abstract (after removing questionnaire / peer-review senses)
    a_clean = NOT_LIT_REVIEW.sub(" ", NOT_LIT_SURVEY.sub(" ", a))
    if A_SELF.search(a_clean):
        rules.append("A_self")
    survey = bool(rules)
    # strict position
    pos = []
    if T_POSITION.search(t):
        pos.append("T_position")
    if A_POSITION.search(a):
        pos.append("A_position")
    rules += pos
    strict = survey or bool(pos)
    weak = []
    if T_WEAK.search(t):
        weak.append("T_weak")
    if A_WEAK.search(a_clean):
        weak.append("A_weak")
    kind = "both" if (survey and pos) else "survey" if survey else "position" if pos else ""
    return {"strict": strict, "broad": strict or bool(weak), "kind": kind, "rules": rules + weak}


def title_only(title):
    """Title-only strict rule, used for comparison series outside the study group G
    (abstract terms were not harvested there)."""
    r = classify(title, "")
    return any(x in ("T_survey", "T_review") for x in r["rules"])


if __name__ == "__main__":
    tests = [
        ("A Survey of Large Language Models", "", True),
        ("Deep learning for X: a review", "", True),
        ("Position: AI safety needs social science", "", True),
        ("Automated code review with LLMs", "We propose a model for code review generation.", False),
        ("Results from a user survey of 300 developers", "We surveyed 300 developers.", False),
        ("Fast transformers", "We propose a new architecture. Experiments show gains.", False),
        ("Graph neural networks in chemistry", "This paper provides a comprehensive review of GNNs.", True),
    ]
    for t, a, want in tests:
        got = classify(t, a)
        print("OK " if got["strict"] == want else "BAD", want, got, "|", t)
