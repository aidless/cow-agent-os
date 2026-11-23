An agent workspace still needs an identity, rules, shared memory, and a flow, plus one application that can be tested without a live model.
cow-agent-os keeps that identity and those rules in Markdown (`AGENT.md`, `RULE.md`, `MEMORY.md`, `WORKFLOW.md`) and anchors them with the Flask app in `fortune-web-v2/`.
Those rules are documents. This repository does not machine-check them.

# cow-agent-os

Result. In separate processes, 2 of 10 test files under `fortune-web-v2/tests/` are clean: `tests/test_phase5_lockout.py` (6 passed, 0 failed), `tests/test_phase6_reset_flow.py` (8 passed, 0 failed). `make check` re-reads 9 files `benchmarks/benchmark_*.json`; every `started_at` date is 2026-07-11. qwen3:4b `overall.weighted_composite` in those files spans 0.0 to 0.619. HEAD tracks 337 files. The Flask healthz version is 1.2.0, the same token as the first heading in `fortune-web-v2/CHANGELOG.md`.

Limits. 8 test files are not clean. Their passed, failed, and error counts are in the table below and are not a repair. Those clean files, run together in one process, record 11 passed and 3 failed (signals: HTTP 429). Separate processes are the run this result calls clean. 7 files have qwen weighted composite 0.0 because every qwen run in that file has `score.len` 0 and no qwen error field. That zero is empty text, not an authentication failure. No qwen run in these JSON files has an error field. The only DeepSeek error string in these files is `HTTPError: HTTP Error 401: Authorization Required`. It appears in 5 files. 5 of those files omit DeepSeek from `overall`. DeepSeek `weighted_composite` is present in 4 files and spans 0.531 to 0.696. Of the 4 files that record both weighted composites, DeepSeek is higher in 3, qwen3:4b is higher in 1, and none are ties. That is not a ranking. `runs_per_prompt` values in the files: 1, 2. Prompt counts: 8. The workspace rules are documents and are not executed. This check does not call a model, does not run `benchmark_llm.py`, and does not walk git history.

## Withdrawn

Withdrawn: the qwen composite at the bottom of the range is an HTTP 401. The 401 string above is a DeepSeek error. qwen rows with that bottom score are empty text.
Withdrawn: the current checkout is mostly vendored third-party code under `tools/` and `knowledge/`. `knowledge/` is workspace notes. `tools/` does not contain the old project trees. Those trees remain in git history; this check does not measure pack size and does not rewrite history.
Withdrawn: one `runs_per_prompt` for every benchmark file. The values are listed above.
Withdrawn: a stable DeepSeek win. The per-file comparison counts are above.
Withdrawn: the two clean test files stay clean when they share a process. The one-process row is in the test table.

## Tests

Each file runs in its own process. The last row runs the two clean files in one process. Signals are substrings of that pytest output, not a full causal taxonomy.

| File | Passed | Failed | Errors | Signals in this run |
|---|---:|---:|---:|---|
| `tests/test_app.py` | 3 | 16 | 0 | application context; missing OllamaQwen3Backend |
| `tests/test_auth_favorites_routes.py` | 5 | 11 | 0 | missing login_attempts; access_token; password policy |
| `tests/test_llm_backends.py` | 0 | 0 | 1 | missing OllamaQwen3Backend |
| `tests/test_phase2_e2e.py` | 3 | 1 | 0 | password policy |
| `tests/test_phase3_user_aware.py` | 4 | 3 | 0 | access_token; status 400 vs 200 |
| `tests/test_phase4_favorite_flow.py` | 2 | 4 | 0 | access_token; status 400 vs 200 |
| `tests/test_phase5_lockout.py` | 6 | 0 | 0 | — |
| `tests/test_phase6_reset_flow.py` | 8 | 0 | 0 | — |
| `tests/test_phase7_subscription.py` | 5 | 3 | 0 | IndexError; status 200 vs 400 |
| `tests/test_user_system.py` | 15 | 4 | 0 | password policy |
| `tests/test_phase5_lockout.py` + `tests/test_phase6_reset_flow.py` in one process | 11 | 3 | 0 | HTTP 429 |

Source facts this check also requires, independent of the counts:

- `llm_backends.py` defines `OllamaQwenBackend` and does not define `OllamaQwen3Backend`.
- `benchmark_llm.py` and `tests/test_llm_backends.py` name `OllamaQwen3Backend`.
- `_validate_question` in `app.py` calls `jsonify`.
- `app.py` sets `DB_PATH` from `readings.db`. The one-process failures above are reported from their pytest signals, not attributed to that path by this check.

## Benchmark JSON files

Values are the strings stored in each file's `overall` object. `—` means that backend has no `overall` entry. `make check` does not re-score the model output.

| File | Date | runs/prompt | Prompts | DeepSeek weighted | qwen3:4b weighted | qwen latency (s) | qwen runs | qwen runs with len 0 | DeepSeek error runs |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `benchmark_20260711_110519.json` | 2026-07-11 | 2 | 8 | — | 0.0 | 7.57 | 16 | 16 | 16 |
| `benchmark_20260711_111805.json` | 2026-07-11 | 2 | 8 | — | 0.0 | 11.15 | 16 | 16 | 16 |
| `benchmark_20260711_112407.json` | 2026-07-11 | 2 | 8 | 0.547 | 0.0 | 10.93 | 16 | 16 | 0 |
| `benchmark_20260711_112923.json` | 2026-07-11 | 2 | 8 | — | 0.0 | 10.92 | 16 | 16 | 16 |
| `benchmark_20260711_113320.json` | 2026-07-11 | 1 | 8 | — | 0.0 | 10.92 | 8 | 8 | 8 |
| `benchmark_20260711_113458.json` | 2026-07-11 | 1 | 8 | — | 0.0 | 11.07 | 8 | 8 | 8 |
| `benchmark_20260711_113711.json` | 2026-07-11 | 2 | 8 | 0.531 | 0.0 | 10.83 | 16 | 16 | 0 |
| `benchmark_20260711_123129.json` | 2026-07-11 | 2 | 8 | 0.545 | 0.619 | 59.12 | 16 | 0 | 0 |
| `benchmark_20260711_125745.json` | 2026-07-11 | 2 | 8 | 0.696 | 0.597 | 64.72 | 16 | 0 | 0 |

## Tracked files

Counted with `git ls-files` at HEAD. Largest top-level path: `knowledge` (113 files). The check fails if a new top-level path has no label in `scripts/check_claims.py`.

| Path | Files | What it is |
|---|---:|---|
| `.editorconfig` | 1 | Editor defaults. |
| `.gitattributes` | 1 | Git attributes. |
| `.github` | 12 | Workflows and templates. |
| `.gitignore` | 1 | Ignore rules. |
| `.gitleaks.toml` | 1 | Secret-scan rules used by the separate gitleaks workflow. |
| `.gitleaksignore` | 1 | Secret-scan ignore list. |
| `.pre-commit-config.yaml` | 1 | Optional pre-commit config. |
| `AGENT.md` | 1 | Workspace identity document. Not machine-checked. |
| `AGENT_HISTORY.md` | 1 | Identity history. |
| `CHANGELOG.md` | 1 | Repository changelog. |
| `CODE_OF_CONDUCT.md` | 1 | Code of conduct. |
| `CONTRIBUTING.md` | 1 | Contributor guide. |
| `FAILURE_MODES.md` | 1 | What the check does not prove. |
| `LICENSE` | 1 | MIT license for this workspace. |
| `MEMORY.md` | 1 | Workspace memory document. Not machine-checked. |
| `Makefile` | 1 | Runs make check. |
| `PREREG.md` | 1 | Questions. Measured numbers sit only in the gated block. |
| `README.md` | 1 | Gated results, rendered by scripts/check_claims.py. |
| `RULE.md` | 1 | Workspace rules document. Not machine-checked. |
| `SECURITY.md` | 1 | Security contact. |
| `SUPPORT.md` | 1 | Support notes. |
| `USER.md` | 1 | User-level notes. |
| `WORKFLOW.md` | 1 | Workspace flow document. Not machine-checked. |
| `benchmarks` | 18 | Committed benchmark artifacts. The check reads the JSON files only. |
| `entries` | 1 | A single file, not a directory. |
| `fortune-web-v2` | 93 | Flask application under test. |
| `installed` | 8 | Install records. |
| `knowledge` | 113 | Workspace notes, not a third-party code tree. Non-markdown tracked paths: `knowledge/concepts/arxiv-watch/.ingested-2026-07-10`. |
| `memory` | 17 | Dated memory notes. |
| `requirements.txt` | 1 | Points at fortune-web-v2/requirements.txt. |
| `scheduler` | 1 | Workspace scheduler data. |
| `scripts` | 1 | Offline check that renders the root README. |
| `skills` | 43 | Workspace skills. |
| `tools` | 7 | Pointer README plus historical license copies. Project trees are not in HEAD. |

## Licenses

Workspace license: `LICENSE` and `fortune-web-v2/LICENSE` both start with `MIT License`. Copies of the removed trees' own `LICENSE` files are under `tools/licenses/`, taken from commit `9a7c090ed90c692dc3f15b837c42f718715906b0` (parent of `98ef4fabbf9a993e08badc9ad6e31493fc579a93`, which dropped the trees). This check hashes those copies and reads their headings. It does not resolve the commit and it does not fetch upstream. Upstream URLs stay in `tools/README.md`; this check only requires those URL strings to remain there.

| Copy | Historical path | Heading read from the copy | Copyright line in the copy | sha256 |
|---|---|---|---|---|
| `tools/licenses/AionUi.LICENSE` | `tools/AionUi/AionUi-main/LICENSE` | Apache License 2.0 | — | `a515d5a76da6c082f0d3d33a597bf82e32ecdac8841ed1783ac081ebd6d62ebf` |
| `tools/licenses/AutoResearchClaw.LICENSE` | `tools/AutoResearchClaw-main/AutoResearchClaw-main/LICENSE` | MIT License | Copyright (c) 2026 Aiming Lab | `4242d33ac3c0a44060197a8d4c5e1c923c613c9aadd873001dcc73389161ac99` |
| `tools/licenses/Awesome-Hacking.LICENSE` | `tools/Awesome-Hacking/Awesome-Hacking-master/LICENSE` | CC0 1.0 Universal | — | `36ffd9dc085d529a7e60e1276d73ae5a030b020313e6c5408593a6ae2af39673` |
| `tools/licenses/ECC.LICENSE` | `tools/ECC/ECC-main/LICENSE` | MIT License | Copyright (c) 2026 Affaan Mustafa | `326146379f01bb137c0a5d3c54770c1aa31076705c8b88a7f6b26a460f6221b2` |
| `tools/licenses/TrendRadar.LICENSE` | `tools/TrendRadar-master/TrendRadar-master/LICENSE` | GNU GPL v3 | Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/> | `3972dc9744f6499f0f9b2dbf76696f2ae7ad8af9b23dde66d6af86c9dfb36986` |

## How to recompute

```bash
pip install -r requirements.txt
make check
```

No API key and no live model host. CI runs the same command on Python 3.12 (`.github/workflows/ci.yml` and `.github/workflows/pr-checks.yml`). The check byte-compiles `fortune-web-v2/app.py` and `fortune-web-v2/auth_routes.py`, scans tracked files for an `sk-` token of 20 or more alphanumeric characters, and compares this README to a fresh render. A shallow clone is enough. Git history is not an input.

## Proposed GitHub About

Agent workspace (泰): identity, rules, shared memory, and the Flask app fortune-web-v2/. HEAD is 337 tracked files and is not a vendored code dump; former tools/ trees are absent (license copies only). Offline check: 2 of 10 test files clean in their own process; 9 benchmark JSON files dated 2026-07-11.

GitHub About is not stored in git. The line above is the text this repository asks for. `make check` regenerates it with the counts.

This file is the output of `scripts/check_claims.py`. Change the script, then run `make check`.
