"""Add a 'For Seniors' link to the topnav of every page, idempotently.

Reads every *.html in the site root, inserts the link right after the
'Play' nav item if it is not already present, and reports what changed.
Safe to re-run.
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
LINK = '<a href="/memory-test-for-seniors.html">For Seniors</a>'
ANCHOR = re.compile(r'(<a href="/">Play</a>)(\s*)(?!<)')

changed, skipped = [], []

for path in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
    name = os.path.basename(path)
    with open(path, encoding="utf-8") as f:
        html = f.read()

    if "memory-test-for-seniors.html" in html and 'For Seniors</a>' in html:
        skipped.append(name)
        continue
    if ANCHOR.search(html) is None:
        skipped.append(name + " (no nav anchor)")
        continue

    new = ANCHOR.sub(lambda m: m.group(1) + "\n      " + LINK, html, count=1)
    if new == html:
        skipped.append(name + " (no change)")
        continue

    with open(path, "w", encoding="utf-8") as f:
        f.write(new)
    changed.append(name)

print("changed :", ", ".join(changed) if changed else "(none)")
print("skipped :", ", ".join(skipped) if skipped else "(none)")
