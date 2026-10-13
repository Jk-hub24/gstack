#!/usr/bin/env python3
"""voice-check: flag machine-written tells in marketing copy.

Usage:
  python3 voice-check.py draft.md
  python3 voice-check.py --channel linkedin draft.md
  pbpaste | python3 voice-check.py --channel reddit -
  python3 voice-check.py --allow-name "Acme" draft.md   # explicit, approved name
  python3 voice-check.py --allow "here's what" ad.md    # approved quote, this piece only

Exit code 0 = clean (warnings allowed), 1 = at least one FAIL.
Stdlib only, so it runs anywhere python3 does.
"""

import argparse
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_NAMES = os.path.normpath(
    os.path.join(HERE, "..", "..", "proof-policy", "blocked-names.txt")
)

SOCIAL = {"reddit", "linkedin", "email", "dm", "x"}

BANNED_WORDS = [
    "delve", "delves", "delving", "landscape", "tapestry", "realm", "leverage",
    "leveraging", "leveraged", "robust", "seamless", "seamlessly", "unlock",
    "unlocks", "unlocking", "unleash", "elevate", "elevates", "empower",
    "empowers", "empowering", "navigate", "navigating", "foster", "fostering",
    "holistic", "pivotal", "game-changer", "game-changing", "cutting-edge",
    "best-in-class", "world-class", "testament", "crucial", "vital", "streamline",
    "streamlined", "supercharge", "supercharged",
    "revolutionize", "revolutionizing", "transformative", "paradigm", "synergy",
    "synergies", "nuanced", "intricate", "multifaceted", "myriad", "plethora",
    "embark", "underscore", "underscores", "showcase", "showcases", "resonate",
    "resonates", "solid", "actionable", "unpack", "mission-critical",
    "value-add", "needle-moving", "thought leader", "thought leadership",
]

BANNED_PHRASES = [
    "moreover", "furthermore", "additionally", "that said", "with that in mind",
    "in addition", "ultimately", "importantly", "notably", "crucially",
    "interestingly", "essentially", "in essence", "at its core",
    "when it comes to", "in today's", "in the world of", "it's worth noting",
    "it is worth noting", "it's important to note", "it is important to note",
    "the reality is", "the truth is", "at the end of the day", "the bottom line",
    "all in all", "in conclusion", "to sum up", "let's dive in", "dive into",
    "deep dive", "let's break it down", "here's why", "here's how",
    "here's what", "here's the thing", "double down", "move the needle",
    "low-hanging fruit", "north star", "level up", "secret sauce",
    "hope this helps", "happy to chat", "feel free to reach out",
    "i hope this finds you well", "i noticed that", "great question",
    "love this", "so true", "let's be honest", "picture this", "imagine a world",
    "here's what nobody tells you", "the lesson here", "moral of the story",
    "game changer", "in the ever-evolving", "fast-paced", "navigate the",
    "on the other hand", "first and foremost", "last but not least",
    "it goes without saying", "needless to say", "rest assured",
]

REVERSAL_PATTERNS = [
    (r"\b(it'?s|this is|that'?s|it is)\s+not\s+(just\s+|only\s+|about\s+)?[^.?!\n]{1,60}?(?:[,;.]|\s[—–-]+)\s*(it'?s|this is|it is|but)\b",
     "setup-then-reversal (It's not X, it's Y)"),
    (r"\bisn'?t\s+about\s+[^.?!\n]{1,60}[.,;]\s*(it'?s|this is)\s+about\b",
     "setup-then-reversal (isn't about X. It's about Y)"),
    (r"\bnot\s+(just|only|merely)\s+[^.?!\n]{1,50}?,?\s+but\s+(also\s+)?",
     "not just X but Y"),
    (r"\b\w+\s+isn'?t\s+the\s+problem\.\s+\w+",
     "X isn't the problem. Y is."),
    (r"\bless\s+about\s+[^.?!\n]{1,40}\s+and\s+more\s+about\b",
     "less about X and more about Y"),
]

OTHER_PATTERNS = [
    (r"(^|[.!?]\s+)(the\s+)?(result|kicker|catch|truth|answer|secret|twist|best part|problem|takeaway)\s*[?:]\s",
     "colon/question reveal (The result? / The kicker:)", "FAIL"),
    (r"\bwhy does (this|that|it) matter\?", "rhetorical question answered", "FAIL"),
    (r"\bwhether you'?re\b", "\"Whether you're X or Y\"", "FAIL"),
    (r"\bfrom\s+\w+(\s+\w+)?\s+to\s+\w+(\s+\w+)?,\s", "\"from X to Y\" range", "WARN"),
    (r"\b\w+,\s+\w+(\s\w+)?,\s+and\s+(\w+\s+){0,2}\w+", "possible rule-of-three list", "WARN"),
    (r"^\s*(imagine|picture)\b", "opens with Imagine/Picture", "FAIL"),
]

# Em/en dashes anywhere, or a spaced hyphen between words. A "- " at the start
# of a line is a markdown bullet, not a dash.
DASH_RE = re.compile(r"[—–]|(?<=\S)[ \t]+-{1,2}[ \t]+(?=\S)")
SEMI_RE = re.compile(r";")
HASHTAG_RE = re.compile(r"(?<!\w)#\w+")
BOLD_LEAD_RE = re.compile(r"^\s*([-*•]\s*)?\*\*[^*\n]{1,40}:?\*\*:?\s")
HEADER_RE = re.compile(r"^\s{0,3}#{1,6}\s")
EMOJI_BULLET_RE = re.compile(r"^\s*[\U0001F300-\U0001FAFF☀-➿✅❌➡]\s")
GENERIC_END_Q = re.compile(
    r"(what do you think|thoughts|agree|what's your take|what are your thoughts|anyone else)\??\s*$",
    re.I,
)
NUMBER_RE = re.compile(r"\b\d[\d,.]*\s?(%|x|k|m|M|K|percent)?\b")


class Finding:
    def __init__(self, sev, rule, line, snippet):
        self.sev, self.rule, self.line, self.snippet = sev, rule, line, snippet

    def __str__(self):
        snip = self.snippet.strip().replace("\n", " ")
        if len(snip) > 90:
            snip = snip[:87] + "..."
        return f"{self.sev:<4}  L{self.line:<4} {self.rule}\n        > {snip}"


def line_of(text, idx):
    return text.count("\n", 0, idx) + 1


def strip_code(text):
    # Ignore fenced code blocks and inline code; they aren't prose.
    text = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def load_names(path):
    if not path or not os.path.exists(path):
        return []
    names = []
    with open(path, encoding="utf-8") as f:
        for raw in f:
            raw = raw.strip()
            if raw and not raw.startswith("#"):
                names.append(raw)
    return names


def sentences(text):
    flat = re.sub(r"\s+", " ", text)
    parts = re.split(r"(?<=[.!?])\s+", flat)
    return [p for p in parts if len(p.split()) >= 2]


def check(text, channel, names, allowed):
    out = []
    prose = strip_code(text)
    low = prose.lower()

    for m in DASH_RE.finditer(prose):
        out.append(Finding("FAIL", "dash used as punctuation (use . , or parentheses)",
                           line_of(prose, m.start()), prose[max(0, m.start() - 30):m.end() + 30]))

    if channel in SOCIAL:
        for m in SEMI_RE.finditer(prose):
            out.append(Finding("FAIL", "semicolon in social copy", line_of(prose, m.start()),
                               prose[max(0, m.start() - 30):m.end() + 30]))

    allow_low = {a.lower() for a in allowed}
    for w in BANNED_WORDS:
        if w in allow_low:
            continue
        for m in re.finditer(r"(?<![\w-])" + re.escape(w) + r"(?![\w-])", low):
            out.append(Finding("FAIL", f"banned word: {w}", line_of(prose, m.start()),
                               prose[max(0, m.start() - 30):m.end() + 30]))

    for p in BANNED_PHRASES:
        if p in allow_low:
            continue
        for m in re.finditer(r"(?<!\w)" + re.escape(p) + r"(?!\w)", low):
            out.append(Finding("FAIL", f"banned phrase: {p}", line_of(prose, m.start()),
                               prose[max(0, m.start() - 30):m.end() + 30]))

    for pat, rule in REVERSAL_PATTERNS:
        for m in re.finditer(pat, prose, re.I):
            out.append(Finding("FAIL", rule, line_of(prose, m.start()), m.group(0)))

    for pat, rule, sev in OTHER_PATTERNS:
        for m in re.finditer(pat, prose, re.I | re.M):
            out.append(Finding(sev, rule, line_of(prose, m.start()), m.group(0)))

    lines = prose.split("\n")
    for i, ln in enumerate(lines, 1):
        if BOLD_LEAD_RE.search(ln):
            out.append(Finding("FAIL" if channel in SOCIAL else "WARN",
                               "bold lead-in bullet (**Thing:** ...)", i, ln))
        if EMOJI_BULLET_RE.search(ln):
            out.append(Finding("FAIL", "emoji bullet", i, ln))
        if channel in SOCIAL and HEADER_RE.search(ln):
            out.append(Finding("FAIL", "header in social copy", i, ln))

    tags = HASHTAG_RE.findall(prose)
    if channel == "reddit" and tags:
        out.append(Finding("FAIL", "hashtags on Reddit", 1, " ".join(tags)))
    elif len(tags) > 3:
        out.append(Finding("FAIL", f"{len(tags)} hashtags (max 3)", 1, " ".join(tags)))

    tail = prose.strip().split("\n")[-1] if prose.strip() else ""
    if GENERIC_END_Q.search(tail):
        out.append(Finding("FAIL", "generic engagement question at the end",
                           len(prose.strip().split("\n")), tail))

    # Rhythm: sentence-length variance.
    sents = sentences(prose)
    if len(sents) >= 6:
        lens = [len(s.split()) for s in sents]
        mean = statistics.mean(lens)
        cv = statistics.pstdev(lens) / mean if mean else 0
        if cv < 0.40:
            out.append(Finding("WARN", f"sentence lengths too even (variation {cv:.2f}, want > 0.40)",
                               1, "mix long wandering sentences with very short ones"))

    # Paragraph shape.
    paras = [p for p in re.split(r"\n\s*\n", prose.strip()) if p.strip()]
    if len(paras) >= 6:
        one_liners = sum(1 for p in paras if len(sentences(p)) <= 1 and len(p.split()) < 18)
        if one_liners / len(paras) > 0.6:
            out.append(Finding("FAIL" if channel == "linkedin" else "WARN",
                               "stacked one-line paragraphs (broetry)", 1,
                               f"{one_liners} of {len(paras)} paragraphs are one short line"))
        sizes = [len(p.split()) for p in paras]
        if statistics.mean(sizes) and statistics.pstdev(sizes) / statistics.mean(sizes) < 0.25:
            out.append(Finding("WARN", "paragraphs all the same size", 1,
                               "vary them: one sentence next to six is normal"))

    # Names: clients, competitors, partners. Never without explicit approval.
    for name in names:
        if name.lower() in allow_low:
            continue
        for m in re.finditer(r"(?<![\w.])" + re.escape(name) + r"(?![\w])", prose, re.I):
            out.append(Finding("FAIL", f"named brand '{name}' (proof-policy: anonymize or get explicit OK)",
                               line_of(prose, m.start()), prose[max(0, m.start() - 30):m.end() + 30]))

    # Numbers: never fail, always remind.
    nums = sorted({m.group(0).strip() for m in NUMBER_RE.finditer(prose) if any(c.isdigit() for c in m.group(0))})
    if nums:
        shown = ", ".join(nums[:12]) + (" ..." if len(nums) > 12 else "")
        out.append(Finding("INFO", "numbers present, each must trace to the proof bank or a named internal source",
                           1, shown))

    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", default=["-"])
    ap.add_argument("--channel", default="generic",
                    choices=["generic", "reddit", "linkedin", "article", "email", "dm", "landing", "x"])
    ap.add_argument("--names", default=DEFAULT_NAMES, help="blocked brand names file")
    ap.add_argument("--allow-name", "--allow", action="append", default=[], dest="allow_name",
                    help="a brand name, word or phrase explicitly approved for this piece (repeatable)")
    args = ap.parse_args()

    names = load_names(args.names)
    failed = False
    for path in args.files:
        text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
        findings = check(text, args.channel, names, args.allow_name)
        order = {"FAIL": 0, "WARN": 1, "INFO": 2}
        findings.sort(key=lambda f: (order[f.sev], f.line))
        label = "stdin" if path == "-" else path
        fails = sum(f.sev == "FAIL" for f in findings)
        warns = sum(f.sev == "WARN" for f in findings)
        print(f"== {label} [{args.channel}]  {fails} fail, {warns} warn")
        for f in findings:
            print(f)
        if fails:
            failed = True
    print("RESULT:", "FAIL, rewrite and re-run" if failed else "PASS")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
