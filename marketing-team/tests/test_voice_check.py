#!/usr/bin/env python3
"""Regression tests for voice-check.py. Run: python3 marketing-team/tests/test_voice_check.py"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
spec = importlib.util.spec_from_file_location(
    "vc", os.path.join(ROOT, "skills", "authentic-voice", "scripts", "voice-check.py"))
vc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vc)
NAMES = vc.load_names(vc.DEFAULT_NAMES)


def rules(text, channel="generic", allowed=()):
    return [f.rule for f in vc.check(text, channel, NAMES, list(allowed)) if f.sev == "FAIL"]


def has(text, fragment, **kw):
    return any(fragment in r for r in rules(text, **kw))


CASES = [
    # (description, passes?)
    ("em dash", lambda: has("We tried it — it broke.", "dash")),
    ("spaced hyphen dash", lambda: has("We tried it - it broke.", "dash")),
    ("markdown bullet is not a dash", lambda: not has("notes\n- first item\n- second", "dash")),
    ("hyphenated word is not a dash", lambda: not has("a well-known 2-3 month window", "dash")),
    ("reversal with comma", lambda: has("It's not about ranking, it's about being cited.", "reversal")),
    ("reversal with dash", lambda: has("It's not about ranking — it's about being cited.", "reversal")),
    ("isn't about / it's about", lambda: has("This isn't about volume. It's about trust.", "reversal")),
    ("not just X but Y", lambda: has("We do not just write posts but run accounts.", "not just")),
    ("colon reveal", lambda: has("Then we checked. The result? Triple.", "reveal")),
    ("banned word", lambda: has("A robust approach.", "robust")),
    ("banned connector", lambda: has("Moreover, it works.", "moreover")),
    ("allow flag clears a phrase", lambda: not has("Here's what worked for us.", "here's what", allowed=["here's what"])),
    ("client name blocked", lambda: has("We ran this for Checkmarx last year.", "Checkmarx")),
    ("approved name allowed", lambda: not has("We ran this for Checkmarx.", "Checkmarx", allowed=["Checkmarx"])),
    ("name inside another word ignored", lambda: not has("the cameos were fine", "Cameo")),
    ("generic closing question", lambda: has("Some point.\n\nWhat do you think?", "engagement question")),
    ("hashtags banned on reddit", lambda: has("good thread #devops", "hashtags", channel="reddit")),
    ("4 hashtags too many", lambda: has("post #a #b #c #d", "hashtags", channel="linkedin")),
    ("semicolon in social", lambda: has("it broke; we fixed it", "semicolon", channel="reddit")),
    ("clean practitioner text passes", lambda: rules(
        "went through 39 prompts for one appsec account last week. four threads did most of the work "
        "and two were from 2024. nobody on their team knew they existed.\n\n"
        "still figuring out if that holds outside security.", channel="reddit") == []),
]

failed = 0
for name, fn in CASES:
    ok = fn()
    print(("ok   " if ok else "FAIL ") + name)
    failed += not ok
print(f"\n{len(CASES) - failed}/{len(CASES)} passed")
sys.exit(1 if failed else 0)
