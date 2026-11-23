# cow-agent-os preregistration

This file states the questions. It is retrospective: it describes what the repository already contains. It does not promise a future experiment.

Measured numbers that this repository stands behind are regenerated into the block below by `scripts/check_claims.py`. Edit that script, then run `make check`.

## Questions

- Can the Flask app report passing and failing tests without hiding the failures?
- Are the committed LLM benchmark JSON files one saved day, rather than a cross-configuration ranking?
- Are the workspace rules (`AGENT.md`, `RULE.md`, `MEMORY.md`, `WORKFLOW.md`) machine-checked?

## What would count as an answer

The first two questions are answered only by the gated block. The third question is answered by the absence of a checker for those documents. `make check` does not parse them.

<!-- GATED-FACTS:START -->
Result. In separate processes, 2 of 10 test files under `fortune-web-v2/tests/` are clean: `tests/test_phase5_lockout.py` (6 passed, 0 failed), `tests/test_phase6_reset_flow.py` (8 passed, 0 failed). `make check` re-reads 9 files `benchmarks/benchmark_*.json`; every `started_at` date is 2026-07-11. qwen3:4b `overall.weighted_composite` in those files spans 0.0 to 0.619. HEAD tracks 337 files. The Flask healthz version is 1.2.0, the same token as the first heading in `fortune-web-v2/CHANGELOG.md`.

Limits. 8 test files are not clean. Their passed, failed, and error counts are in the table below and are not a repair. Those clean files, run together in one process, record 11 passed and 3 failed (signals: HTTP 429). Separate processes are the run this result calls clean. 7 files have qwen weighted composite 0.0 because every qwen run in that file has `score.len` 0 and no qwen error field. That zero is empty text, not an authentication failure. No qwen run in these JSON files has an error field. The only DeepSeek error string in these files is `HTTPError: HTTP Error 401: Authorization Required`. It appears in 5 files. 5 of those files omit DeepSeek from `overall`. DeepSeek `weighted_composite` is present in 4 files and spans 0.531 to 0.696. Of the 4 files that record both weighted composites, DeepSeek is higher in 3, qwen3:4b is higher in 1, and none are ties. That is not a ranking. `runs_per_prompt` values in the files: 1, 2. Prompt counts: 8. The workspace rules are documents and are not executed. This check does not call a model, does not run `benchmark_llm.py`, and does not walk git history.
<!-- GATED-FACTS:END -->

## Out of scope

A live model call, a repair of failing tests, and a formal semantics for the workspace rules.
