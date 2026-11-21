#!/usr/bin/env python3
"""Rebuild knowledge/index.json.gz: every Markdown section in the repo.

tools/ask.py downloads this one file from GitHub, so the phone never needs a
copy of the repo. Run after changing docs (a GitHub Action also runs it).
"""
import gzip, json, os, re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sections = []
for root, dirs, files in os.walk(REPO):
    dirs[:] = sorted(d for d in dirs if not d.startswith(".") and d != "knowledge")
    for name in sorted(files):
        if not name.lower().endswith(".md"):
            continue
        path = os.path.join(root, name)
        with open(path, encoding="utf-8", errors="ignore") as fh:
            text = fh.read()
        rel = os.path.relpath(path, REPO)
        for part in re.split(r"\n(?=#{1,4} )", text):
            part = part.strip()
            if len(part) > 40:
                sections.append([rel, part[:3000]])
out = os.path.join(REPO, "knowledge", "index.json.gz")
with gzip.GzipFile(out, "wb", mtime=0) as fh:
    fh.write(json.dumps(sections, ensure_ascii=False).encode("utf-8"))
print("%d sections -> %s (%d KB)" % (len(sections), out, os.path.getsize(out) // 1024))
