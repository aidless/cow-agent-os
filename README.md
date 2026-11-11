# cow-agent-os

> **English TL;DR**: An agent-workspace "OS" layer (identity, rules, shared memory, multi-agent flow) anchored by one real Flask application. Only 2 of 10 test files are green; the other 8 stay red with their root causes documented in CI. Nine committed 2026-07-11 benchmark JSONs can be re-read offline, but they are single-day observations, not cross-configuration conclusions.

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

## 这个项目解决什么问题 / 为什么重要

Agent 系统的日常运行需要一个「OS 层」：身份与边界（`AGENT.md`）、行为规则（`RULE.md`）、
共享记忆（`MEMORY.md`）、多 agent 流程（`WORKFLOW.md`）。cow-agent-os 把这四件事落成
**一组可执行的规则文件** + 一个**真实可运行的应用**（`fortune-web-v2/`，Flask 命理咨询站，
含用户系统、订阅、收藏、限流与合规）。它不是又一个 agent 框架，而是**一个长期运行的
agent 工作区的治理与运行规范**——「谁是泰、泰能做什么、记忆如何沉淀、出错怎么办」。

## 我用了什么方法

- **规则即代码**：`AGENT.md`（身份/边界 V4）/ `RULE.md`（行为规则）/ `MEMORY.md`（记忆层）/
  `WORKFLOW.md`（多 agent 流程）以版本化 Markdown 维护，`AGENT_HISTORY.md` 保留 v1.0 迁移史。
- **真实应用做锚点**：`fortune-web-v2/` 是唯一 CI 测试的自家代码（Flask + SQLite + 多后端 LLM），
  用真实 HTTP 流测试用户系统、订阅、锁屏、重置、收藏。
- **基准对比**：`benchmark_llm.py` 跑 DeepSeek vs qwen3:4b 对比（`benchmarks/`，9 组 2026-07-11 实测）。

## 结果如何

- **测试基线（诚实）**：10 个测试文件中 **2 个绿**（`test_phase5_lockout.py` 6 passed /
  `test_phase6_reset_flow.py` 8 passed），**8 个红**（原因已在 CI 注释逐条列出：`app.py` 的
  `_validate_question()` 在 application context 外调 `jsonify()`、`llm_backends.py` 的
  `OllamaQwenBackend`/`OllamaQwen3Backend` 改名未传播、共享 SQLite 状态互相干扰等）。
  CI 只跑绿的两个（各自独立进程，避免共享 `readings.db` 干扰），其余**如实报告不隐藏**。
- **基准结果**：`benchmarks/` 9 组报告显示 qwen3:4b 综合分从 0.0（401 认证失败）到 0.619 不等，
  DeepSeek 在部分维度胜出——但这是 2026-07-11 的单日实测，**不是跨配置结论**。

## 边界声明（证明什么 / 不证明什么）

**Fail-closed 声明**：测试与基准**默认 fail-closed**——8 个当前红的测试文件**不被隐藏、不被当环境问题**，而是在 `.github/workflows/ci.yml` 注释逐条列出真实根因（如 `app.py` 的 `_validate_question()` 在 application context 外调 `jsonify()`、`llm_backends.py` 后端改名未传播、共享 SQLite 状态互相干扰）。CI 只跑绿的两个（各自独立进程避免共享 `readings.db` 干扰），其余**如实报告**。基准的「DeepSeek 胜」不写成稳定结论——明确标注为 2026-07-11 单日实测。缺陷不被掩盖、单日结论不被拔高，是本文档的 fail-closed 立场。

**证明（可复算）**：① `fortune-web-v2/tests/test_phase5_lockout.py` 与
`test_phase6_reset_flow.py` 各自独立进程下全绿；② `benchmarks/` 的 9 组对比文件与
`benchmark_llm.py` 的写入逻辑一致（`datetime.now().strftime('%Y%m%d_%H%M%S')` 命名）。
**不证明**：① 应用整体测试通过——8/10 文件当前红，是**仓库内真实缺陷**，非环境问题
（CI 注释逐条给了根因）；② 基准的「DeepSeek 胜」不是**稳定结论**——2026-07-11 单日、
单模型、有限 prompt 集；③ 工作区规则（AGENT/RULE/MEMORY/WORKFLOW）**未做机器验证**，
是文档性规范而非可证明的形式语义。

## 复算（Reproduction）

```bash
cd cow-agent-os
# 1) 跑绿的两个测试（各自独立进程，避免共享 readings.db 干扰）
cd fortune-web-v2
python -m pytest tests/test_phase5_lockout.py -q      # 6 passed
python -m pytest tests/test_phase6_reset_flow.py -q   # 8 passed

# 2) 看 CI 如何如实报告 8 个红文件（含根因）
sed -n '1,50p' .github/workflows/ci.yml               # 注释即证据

# 3) 重算基准：读一份 json 的汇总（不重跑，避免耗 token）
python3 -c "import json; d=json.load(open('benchmarks/benchmark_20260711_123129.json')); print(json.dumps(d, ensure_ascii=False)[:400])"

# 4) 重新生成基准对（需真实 LLM 端点 + key）
cd fortune-web-v2 && python benchmark_llm.py --runs 2
```

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

## U1 results table (recomputed 2026-11-11)

The nine committed benchmark reports were parsed offline and their `overall`
summaries recomputed. `—` means the report has no summary for that backend in
that run (it is not a zero). Column `runs/p` is `runs_per_prompt`.

| Benchmark file | runs/p | prompts | DeepSeek weighted composite | qwen3:4b weighted composite | qwen3:4b avg latency (s) | Source (path:line) |
|---|---|---|---|---|---|---|
| `benchmark_20260711_110519.json` | 2 | 8 | — | 0.0 | 7.57 | `benchmarks/benchmark_20260711_110519.json:511` |
| `benchmark_20260711_111805.json` | 2 | 8 | — | 0.0 | 11.15 | `benchmarks/benchmark_20260711_111805.json:511` |
| `benchmark_20260711_112407.json` | 2 | 8 | 0.547 | 0.0 | 10.93 | `benchmarks/benchmark_20260711_112407.json:711` |
| `benchmark_20260711_112923.json` | 2 | 8 | — | 0.0 | 10.92 | `benchmarks/benchmark_20260711_112923.json:511` |
| `benchmark_20260711_113320.json` | 1 | 8 | — | 0.0 | 10.92 | `benchmarks/benchmark_20260711_113320.json:351` |
| `benchmark_20260711_113458.json` | 1 | 8 | — | 0.0 | 11.07 | `benchmarks/benchmark_20260711_113458.json:351` |
| `benchmark_20260711_113711.json` | 2 | 8 | 0.531 | 0.0 | 10.83 | `benchmarks/benchmark_20260711_113711.json:711` |
| `benchmark_20260711_123129.json` | 2 | 8 | 0.545 | 0.619 | 59.12 | `benchmarks/benchmark_20260711_123129.json:711` |
| `benchmark_20260711_125745.json` | 2 | 8 | 0.696 | 0.597 | 64.72 | `benchmarks/benchmark_20260711_125745.json:711` |

Recompute command actually executed for this pass:

```bash
python3 -c "import json,glob,os; fs=sorted(glob.glob('benchmarks/benchmark_*.json')); \
print(len(fs),'benchmark files'); [print(os.path.basename(p), json.load(open(p))['overall']) for p in fs]"
# 9 benchmark files  (full per-file values are in the table above)
```

Known-failure inventory (unchanged by this pass — the test suite itself is not
modified here):

| Item | Count | Source |
|---|---|---|
| Test files under `fortune-web-v2/tests/` | 10 | live `glob test_*.py` |
| Green test files | 2 | `test_phase5_lockout.py`, `test_phase6_reset_flow.py` (see Reproduction above) |
| Red test files | 8 | root causes listed in `.github/workflows/ci.yml` comments |
| Test files named in CI comments (includes the 2 green ones) | 10 | `.github/workflows/ci.yml` |

The benchmark numbers are a single-day (2026-07-11) measurement, not a stable
ranking: several runs have no DeepSeek summary at all, and qwen3:4b composites
range from 0.0 to 0.619.

<!-- figure: pending real measurement -->
