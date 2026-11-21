#!/usr/bin/env python3
"""Ask your local llama-server a question, answered from this repo in the cloud.

The repo stays on GitHub. Each run downloads its knowledge index
(knowledge/index.json.gz, ~1 MB) straight into memory, picks the sections that
best match the question, and sends them with the question to llama-server's
OpenAI-compatible API on 127.0.0.1. Nothing is saved on the phone.
Standard library only (Termux-friendly).

Install (the only file on the phone):
    curl -fsSL https://raw.githubusercontent.com/nuthouse0440-netizen/h4cker/master/tools/ask.py -o ~/ask.py

Usage:
    python ~/ask.py "what are good free CTF sites?"
    python ~/ask.py            # interactive mode: downloads once, then ask away

Settings (environment variables):
    LLAMA_URL   server address   (default http://127.0.0.1:8080)
    KB_URL      knowledge index  (default: this repo on GitHub)
    ASK_TOP     sections to send (default 6)
    ASK_CHARS   max context characters (default 6000; lower it for small models)
"""
import gzip
import json
import os
import re
import sys
import urllib.error
import urllib.request

KB_URL = os.environ.get("KB_URL", "https://raw.githubusercontent.com/"
                        "nuthouse0440-netizen/h4cker/master/knowledge/index.json.gz")
URL = os.environ.get("LLAMA_URL", "http://127.0.0.1:8080").rstrip("/")
TOP = int(os.environ.get("ASK_TOP", "6"))
MAX_CHARS = int(os.environ.get("ASK_CHARS", "6000"))
STOP = set("a an and are as at be by can do does for from how i in is it me my of on "
           "or the to what when where which who why with you your".split())


def words(text):
    return [w for w in re.findall(r"[a-z0-9][a-z0-9+#.-]*", text.lower()) if w not in STOP]


def load_sections():
    """Download the knowledge index from GitHub into memory."""
    try:
        with urllib.request.urlopen(KB_URL, timeout=120) as resp:
            raw = resp.read()
    except urllib.error.URLError as exc:
        sys.exit("Couldn't download the knowledge index from GitHub (%s).\n"
                 "Check your internet connection." % exc)
    return [tuple(x) for x in json.loads(gzip.decompress(raw).decode("utf-8"))]


def best_sections(question, sections):
    q = set(words(question))
    if not q:
        return []
    scored = []
    for rel, body in sections:
        ws = words(body)
        if not ws:
            continue
        hits = sum(1 for w in ws if w in q)
        found = len(q & set(ws))
        path_hits = len(q & set(words(rel)))
        if found:
            scored.append((found * 3 + path_hits * 2 + hits / (len(ws) ** 0.5), rel, body))
    scored.sort(reverse=True)
    out, used = [], 0
    for _, rel, body in scored[:TOP]:
        chunk = "[%s]\n%s" % (rel, body)
        if used + len(chunk) > MAX_CHARS:
            chunk = chunk[: max(0, MAX_CHARS - used)]
        if chunk:
            out.append(chunk)
            used += len(chunk)
        if used >= MAX_CHARS:
            break
    return out


def ask(question, sections):
    context = best_sections(question, sections)
    system = ("You are a cybersecurity study assistant. Answer from the reference "
              "notes below when they are relevant, and name the file you used in "
              "brackets. If the notes don't cover it, say so and answer briefly from "
              "general knowledge. Offensive techniques are for authorized testing, "
              "labs and CTFs only.\n\nREFERENCE NOTES:\n" +
              ("\n\n".join(context) if context else "(no matching notes)"))
    payload = {
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": question}],
        "temperature": 0.3,
        "stream": False,
    }
    req = urllib.request.Request(URL + "/v1/chat/completions",
                                 data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            data = json.load(resp)
    except urllib.error.URLError as exc:
        return ("Couldn't reach llama-server at %s (%s).\n"
                "Is it running? Check ~/llama-server.log, or set LLAMA_URL to the "
                "right port." % (URL, exc))
    return data["choices"][0]["message"]["content"].strip()


def main():
    sections = load_sections()
    if len(sys.argv) > 1:
        print(ask(" ".join(sys.argv[1:]), sections))
        return
    print("Ask about the h4cker repo (Ctrl+C or empty line to quit).")
    while True:
        try:
            q = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not q:
            break
        print("\n" + ask(q, sections))


if __name__ == "__main__":
    main()
