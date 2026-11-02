# cow-agent-os 预注册（PREREG）

> 本文档是研究规格（registered-report 风格），不是结果报告。它声明本仓库**计划检验的假设、评测方案、成功标准与明确边界**，全部基于 `README.md`、`AGENT.md`、`benchmarks/`、`fortune-web-v2/benchmark_llm.py` 中已落盘的真实内容。本文档不虚构任何未执行的实验。

## 1. 研究问题

一个长期运行的 agent 工作区治理与运行规范（身份/边界 `AGENT.md`、行为规则 `RULE.md`、共享记忆 `MEMORY.md`、多 agent 流程 `WORKFLOW.md`，锚点应用 `fortune-web-v2/`）能否做到：

- **RQ1**：工作区应用（`fortune-web-v2/`，Flask 命理咨询站）的测试是否诚实报告通过/失败，而不隐藏缺陷？
- **RQ2**：LLM 后端对比基准（DeepSeek vs qwen3:4b）是否给出**单日实测**而非跨配置结论？
- **RQ3**：工作区规则文件（AGENT/RULE/MEMORY/WORKFLOW）是否做了机器验证？

## 2. 预注册假设

| ID | 假设 | 检验方式 | 成功标准 |
|---|---|---|---|
| H1 | 工作区应用测试结果**诚实**：绿的文件通过、红的文件如实报告根因 | `pytest` 跑 `fortune-web-v2/tests/` + 读 `.github/workflows/ci.yml` 注释 | 10 个测试文件中 2 绿（test_phase5_lockout 6 passed / test_phase6_reset_flow 8 passed），8 红如实列出根因 |
| H2 | LLM 基准是**单日实测**而非稳定结论 | 读 `benchmarks/` 9 组 dated JSON + `fortune-web-v2/benchmark_llm.py` | 每组含 `started_at` 时间戳与 `runs_per_prompt`，`qwen3:4b` 综合分 0.0–0.619 不等，标注「不是跨配置结论」 |
| H3 | 基准写入逻辑与报告文件**一致** | 核对 `benchmark_llm.py` 的 `datetime.now().strftime('%Y%m%d_%H%M%S')` 命名 | 9 组对比文件与写入逻辑一致 |
| H4 | 工作区规则**未做机器验证**（诚实边界） | 检查 AGENT/RULE/MEMORY/WORKFLOW 是否为可证明形式语义 | 明确声明为文档性规范而非形式语义 |

## 3. 评测方案

- **应用测试**：`fortune-web-v2/tests/test_phase5_lockout.py`（6 passed）、`test_phase6_reset_flow.py`（8 passed）各自独立进程（避免共享 `readings.db` 干扰）；其余 8 个红文件在 `.github/workflows/ci.yml` 注释逐条给出根因（`app.py` 的 `_validate_question()` 在 application context 外调 `jsonify()`、`llm_backends.py` 的 `OllamaQwenBackend`/`OllamaQwen3Backend` 改名未传播、共享 SQLite 状态互相干扰等）。
- **LLM 基准**：`benchmark_llm.py`（DeepSeek vs qwen3:4b，9 组 2026-07-11 实测，`runs_per_prompt=2`），指标含 `avg_composite`、`compliance_score`、`length_score`。
- **复现**：`cd fortune-web-v2 && python benchmark_llm.py --runs 2`（需真实 LLM 端点 + key）。

## 4. 已声明边界（证明什么 / 不证明什么）

**证明什么（已实测）**：
- `fortune-web-v2/tests/test_phase5_lockout.py` 与 `test_phase6_reset_flow.py` 各自独立进程下全绿（6 + 8 passed）。
- `benchmarks/` 的 9 组对比文件与 `benchmark_llm.py` 的写入逻辑一致（`datetime.now().strftime('%Y%m%d_%H%M%S')` 命名）。

**不证明什么（诚实边界）**：
- 应用整体测试通过——8/10 文件当前红，是**仓库内真实缺陷**，非环境问题（CI 注释逐条给了根因）。
- 基准的「DeepSeek 胜」不是**稳定结论**——2026-07-11 单日、单模型、有限 prompt 集。
- 工作区规则（AGENT/RULE/MEMORY/WORKFLOW）**未做机器验证**，是文档性规范而非可证明的形式语义。

## 5. 成功标准（预先声明）

H1 与 H2 的**联合**成功 = 应用测试诚实报告（2 绿 + 8 红如实列根因）+ 基准标注为单日实测而非稳定结论。本文档声明的成功**不**包括「工作区规则被形式化验证」——那明确排除在成功之外（H4）。

## 6. 预注册时间戳与状态

- 本文档为**回顾性预注册**：反映仓库既有已落盘内容（`README.md`、`AGENT.md`、`benchmarks/`、`fortune-web-v2/benchmark_llm.py`），不做前瞻性承诺。
- 目的：把「假设 + 评测方案 + 成功标准 + 边界」写清楚，供评审判断本仓库到底证明/不证明什么。
