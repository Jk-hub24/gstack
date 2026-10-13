#!/usr/bin/env python3
"""Copy shared/house-rules.md into every agent between the house-rules markers.

Run after editing shared/house-rules.md:  python3 scripts/sync-house-rules.py
Use --check in CI or before committing: exits 1 if any agent is out of date.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES = open(os.path.join(ROOT, "shared", "house-rules.md"), encoding="utf-8").read().strip()
BLOCK = re.compile(r"<!-- house-rules:start -->.*?<!-- house-rules:end -->", re.S)
NEW = f"<!-- house-rules:start -->\n{RULES}\n<!-- house-rules:end -->"

check = "--check" in sys.argv
stale = []
agents_dir = os.path.join(ROOT, "agents")
for name in sorted(os.listdir(agents_dir)):
    if not name.endswith(".md"):
        continue
    path = os.path.join(agents_dir, name)
    text = open(path, encoding="utf-8").read()
    if not BLOCK.search(text):
        print(f"missing markers: agents/{name}")
        stale.append(name)
        continue
    updated = BLOCK.sub(lambda _: NEW, text)
    if updated != text:
        stale.append(name)
        if not check:
            open(path, "w", encoding="utf-8").write(updated)
            print(f"updated agents/{name}")

if check and stale:
    print("out of date:", ", ".join(stale))
    sys.exit(1)
print("house rules in sync" if not stale or not check else "")
