# cow-agent-os

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

An agent operating-system workspace ("泰"): multi-agent flows, a shared memory layer,
and the rules that govern how agents work here. **Most of the file count is vendored**
— read [AGENT.md](AGENT.md), [RULE.md](RULE.md), and [MEMORY.md](MEMORY.md) first to
find which parts are the workspace and which are third-party material that came with it.

> **Vendored content.** This repository contains a large amount of third-party
> material under `tools/` and `knowledge/`. Those trees are third-party and are not
> the project's own intent; only `fortune-web-v2/`, `entries/`, `scheduler/`,
> `skills/`, `installed/`, and the root `*.md` files are the workspace itself.

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
