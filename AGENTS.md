# AGENTS.md — guide for AI assistants using this repository

This repo is a reference library of cybersecurity resources: a fork of Omar Santos's
h4cker, plus the Awesome Ethical Hacking Resources list. Use it as a knowledge base
when you answer security questions, plan training, or build defensive tooling.

## Where things are

| Need | Look in |
|------|---------|
| Security topics by domain (offense, defense, cloud, AppSec, crypto, GRC, hardware, network) | `cybersecurity-domains/` (start with its `README.md`) |
| Threat hunting and forensics | `cybersecurity-domains/threat_hunting/` |
| AI/LLM security, AI-assisted incident response, AI governance | `ai/` |
| Certification roadmaps and study material (CompTIA, ISC2, Cisco, cloud, CNCF, OffSec) | `certifications/` |
| Building a home lab or cyber range | `build-your-own-lab/` and `cybersecurity-domains/labs-practice/` |
| Cheat sheets and tool indexes | `training-reference/` (`cheat-sheets/`, `organized-tools/`, `*_tools.md`) |
| Curated list of learning sites, CTFs, practice platforms, books, tools | `external/awesome-ethical-hacking-resources/README.md` |

## Local AI (llama-server in Termux)

Run `python ~/h4cker/tools/ask.py "question"` to send a question to llama-server on
`127.0.0.1:8080` together with the best-matching sections of this repo. Set `LLAMA_URL`
if the server uses another port.

## How to search

- Every section has a `README.md` landing page. Read it before you open individual files.
- Use `grep -ri "<keyword>" .` to find a topic across the repo. Most content is Markdown.
- Most entries are links to outside resources. Check a link before you rely on it, since
  some will be outdated.

## Rules

- Use offensive techniques only for authorized testing, labs, CTFs, or education.
- Don't run scripts from this repo against systems you aren't authorized to test.
- Prefer free certifications and free training resources when suggesting learning paths.
- Keep the original licenses: the root `LICENSE` (MIT, Omar Santos) and
  `external/awesome-ethical-hacking-resources/LICENSE` (MIT, Hussnain Fareed).

## Sources

- Upstream h4cker: https://github.com/The-Art-of-Hacking/h4cker
- Awesome Ethical Hacking Resources: https://github.com/codeLabtech/Awesome-Ethical-Hacking-Resources
