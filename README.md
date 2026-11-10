# cow-agent-os

[![CI](https://github.com/aidless/cow-agent-os/actions/workflows/ci.yml/badge.svg)](https://github.com/aidless/cow-agent-os/actions/workflows/ci.yml)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

An agent operating-system workspace ("泰"): multi-agent flows, a shared memory layer,
and the rules that govern how agents work here. **Most of the file count is vendored**
— read [AGENT.md](AGENT.md), [RULE.md](RULE.md), and [MEMORY.md](MEMORY.md) first to
find which parts are the workspace and which are third-party material that came with it.

> **Vendored content.** This repository contains a large amount of third-party
> material under `tools/` and `knowledge/`. Those trees are third-party and are not
> the project's own intent; only `fortune-web-v2/`, `entries/`, `scheduler/`,
> `skills/`, `installed/`, and the root `*.md` files are the workspace itself.

## Quickstart

The workspace's own runnable application is `fortune-web-v2/` (Flask). Everything
under `tools/` and `knowledge/` is vendored third-party material (see the boundary
note above and [tools/README.md](tools/README.md)) — nothing there is started or tested.

```bash
# 1. install the runnable app's dependencies
pip install -r requirements.txt          # points at fortune-web-v2/requirements.txt

# 2. start the app (dev server, port 5000)
python3 fortune-web-v2/app.py
#   * Running on http://127.0.0.1:5000
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:5000/    # → 200 (verified 2026-11-10)

# 3. run the CI-green test subset
python3 -m pytest fortune-web-v2/tests/test_phase5_lockout.py -q   # → 6 passed
python3 -m pytest fortune-web-v2/tests/test_phase6_reset_flow.py -q # → 8 passed
```

## Results

Real runs on 2026-11-10 (CPython 3.12, Flask 3.0.0):

- `python3 fortune-web-v2/app.py` serves the workspace app; `GET /` returns HTTP 200.
- CI test subset: `test_phase5_lockout.py` 6 passed, `test_phase6_reset_flow.py` 8
  passed (each file in a separate process — see Limits).

## Limits

- **The full fortune-web-v2 pytest suite is not green.** 55 failed / 38 passed on
  2026-11-10, all pre-existing repository defects, documented file-by-file in
  [.github/workflows/ci.yml](.github/workflows/ci.yml) (e.g. `app.py:619`
  `_validate_question()` calls `flask.jsonify()` outside an application context;
  `test_llm_backends.py` imports `OllamaQwen3Backend` while `llm_backends.py:188`
  defines `OllamaQwenBackend`). CI runs only the two green files so the gap stays
  visible instead of being hidden behind `--ignore`.
- The two green test files must run in separate processes: sharing one process hits
  a shared-SQLite defect between them.
- `app.py` is a Flask development server; production deploys use the Dockerfile /
  docker-compose.yml in `fortune-web-v2/` (see its own README).
- Vendored trees (`tools/`, `knowledge/`) are documented upstream pointers, not
  working copies — fetch originals from their own sources.

## Entry points

| Path | Contents |
|---|---|
| [AGENT.md](AGENT.md) | who the workspace agent ("泰") is and how it operates |
| [RULE.md](RULE.md) | the rules agents must follow |
| [MEMORY.md](MEMORY.md) | the shared memory layer |
| [WORKFLOW.md](WORKFLOW.md) | the multi-agent flow definition |
| [USER.md](USER.md) | user-level configuration |
| [AGENT_HISTORY.md](AGENT_HISTORY.md) | agent activity history |
| `fortune-web-v2/` | the workspace's own application (Flask) — the only part CI tests |
| `memory/` | dated memory notes (`YYYY-MM-DD.md`) |
| `entries/`, `scheduler/`, `skills/`, `installed/` | workspace data and skills |
| `tools/`, `knowledge/` | vendored third-party trees — left untouched by CI |

Benchmark runs (nine dated pairs, 2026-07-11) are kept in
`benchmarks/`; the date-stamped filenames are separate runs.
`fortune-web-v2/benchmark_llm.py` writes a new pair to the current
directory when it runs.

## License

MIT for the workspace. Vendored material under `tools/` and `knowledge/` keeps its own
license.
