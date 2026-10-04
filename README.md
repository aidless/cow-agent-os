# cow-agent-os

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

An agent operating-system workspace ("泰"): multi-agent flows, a shared memory layer,
and the rules that govern how agents work here. **Most of the file count is vendored**
— read [AGENT.md](AGENT.md), [RULE.md](RULE.md), and [MEMORY.md](MEMORY.md) first to
find which parts are the workspace and which are third-party material that came with it.

> **Vendored content.** This repository contains a large amount of third-party
> material. Only the files described in `AGENT.md` are the workspace itself; treat
> everything under vendored paths as third-party and do not read those files as project
> intent. `checksums.py` verifies the vendored trees.

## Entry points

| Path | Contents |
|---|---|
| [AGENT.md](AGENT.md) | what this workspace is and how to work in it |
| [RULE.md](RULE.md) | the rules agents must follow |
| [MEMORY.md](MEMORY.md) | the shared memory layer |
| [WORKFLOW.md](WORKFLOW.md) | the multi-agent flow definition |
| [USER.md](USER.md) | user-level configuration |
| [AGENT_HISTORY.md](AGENT_HISTORY.md) | agent activity history |
| `checksums.py` | integrity check for the vendored trees |

Benchmarks live in `benchmark_*.json` at the repository root; the date-stamped filenames
are separate runs.

## License

MIT for the workspace. Vendored material keeps its own license — see the upstream
projects listed in `AGENT.md`.
