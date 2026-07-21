# Genesis Master — 元级 AI 编排系统

> Source: 2026-07-11 F:\Research\genesis-master\ 实地扫描 + README + submission/README + CHANGELOG(部分乱码段已跳过)

## 🎯 一句话定位

**Genesis Master** 是刘泽文 **第 6 篇论文的提交材料** ——
"一个能自己创造 AI Agent、调度它们协作、让它们反思进化的元级 AI 编排系统"。
**4 层反馈循环 + 动态 Agent 生成 + 学术可复现 + 可插拔 LLM**。

**重要更正**:在 7/11 上午盘点时我以为这是 paper-writing-agent 的早期版本,**完全错了**。
这是 **TMLR 投稿的独立论文项目**(11 页 paper.pdf),不在 PAPER6_CONSOLIDATED 那个新 stub 里。

## 📊 关键数字

| 指标 | 数值 | 备注 |
|---|---|---|
| 单元测试 | **195 passed**(0 fail / 0 error) | v1 提交时 161,post-submission +34 |
| 论文篇幅 | **11 页 TMLR** | paper.pdf 414 KB |
| AgentSpec templates | 18(5 generic + 13 paper-review) | |
| review tools | 28 | |
| 反射日志 | 43 条(R-001–R-043) | |
| Ablation 配置 | 5(L1–L4 渐进)+ v9.3 组合 4 配置 | |
| Zip 大小 | 1,116,661 B | |
| License | MIT | |

## 🏛️ 三大核心能力

| 能力 | 含义 | 实现路径 |
|---|---|---|
| **创世 (Creation)** | 动态生成专用 Agent | `genesis/master/factory.py` + `genesis/templates/` |
| **调度 (Orchestration)** | 多 Agent 协作(顺序/并行/DAG) | `genesis/master/orchestrator.py` + `genesis/agent/protocol.py` |
| **反思 (Reflection)** | 任务后反思 + 长期记忆 | `genesis/master/memory.py` |

## 🔄 四层反馈循环(论文核心贡献)

| 层 | 范围 | 触发 | 机制 |
|---|---|---|---|
| **L1** Agent Internal | 单次任务 | self-eval 失败 | 反思 + 改 prompt |
| **L2** Task Retry | 单次 run | 子任务失败 | mutate spec + 重试 |
| **L3** Cross-run | 跨 run | 每次 run 开始 | 检索 top-k 记忆 + 注入 context |
| **L4** Self-evolution | 跨多次 run | 失败次数 ≥ 阈值 | LLM 生成新模板 + 影子模式验证 |

## 📦 版本历史(实际开发进度)

### v1.0(2026-07-09,已投稿)✅

- 4 层反馈循环 L1-L4 全套
- 工具权限 + 重试 + 日志
- 可插拔记忆后端(TFIDF + Chroma)
- L4 影子模式
- Gradio dashboard
- 消融实验脚本(L1-L4 5 配置)
- 161 个单元测试
- 18 AgentSpec templates + 28 review tools
- 11 页 TMLR 投稿 paper.pdf

### v8.0 – v9.3(2026-07-08 – 2026-07-09, post-submission)🆕

**不包含在 paper.pdf 里,作为扩展材料保留**:

- v8.0: AdaptiveTeamSizer(2–10 reviewers, 5 因子复杂度评分)
- v9.0: NegotiationEngine(A2A 协商,4 档决定 + 多轮挑战/让步)
- v9.1: 协商集成到固定团队(`PaperReviewWorkflow`)
- v9.2: 协商集成到动态团队(`DynamicPaperReviewWorkflow`)
- v9.3: 组合 ablation(adaptive_sizing × use_negotiation, 4 配置 × 60 runs)
- **+34** 个单元测试(161 → 195)
- 3 个新文档(`docs/NEGOTIATION_V92.md` / `docs/ABLATION_V93.md` / `docs/REFLECTION_LOG.md` R-042/R-043)

### v9.4+ Future Work

- 真实 LLM 端到端测试(需要有效 API key)
- v2.0 paper(整合 v8-v9 + 真实 LLM 数据)
- A2A 通信更复杂模式(辩论、市场、共识)
- Web UI 任务树可视化
- LLM-as-judge 偏差校准 ← **与刘泽文 PAPER1-3 校准主线直接相关**
- 跨域模板迁移
- 在线学习(持续进化)
- 多用户/多租户

## 🆚 与主流框架对比(README 表格)

| 特性 | LangGraph | AutoGen | CrewAI | **Genesis Master** |
|------|-----------|---------|--------|---------------------|
| 动态创建 Agent | ❌ | ❌ | ❌ | ✅ |
| Agent YAML 序列化 | ❌ | ❌ | ❌ | ✅ |
| L1 自我评估 + 反思 | ❌ | ❌ | ❌ | ✅ |
| L2 任务级重试 + spec 变异 | ❌ | ❌ | ❌ | ✅ |
| L3 长期记忆 + 跨 run 学习 | 需自配 | 需自配 | 部分 | ✅ 内置 + 反思 |
| L4 模板自我进化 | ❌ | ❌ | ❌ | ✅ 含影子模式 |
| 工具权限控制 | ❌ | ❌ | ❌ | ✅ 三级风险 + 角色限制 |
| Web Dashboard | ❌ | ❌ | ❌ | ✅(Gradio)|

## 📁 项目结构(核心)

```
genesis-master/
├── genesis/
│   ├── llm/                # LLM 抽象层(openai_compat + router)
│   ├── agent/              # Agent 基类 + 协议 + worker
│   ├── tools/              # 工具(含权限、重试、日志)
│   ├── master/             # 创世主
│   │   ├── planner.py
│   │   ├── factory.py      # 创世
│   │   ├── orchestrator.py # DAG + L2 重试
│   │   ├── memory.py       # 可插拔记忆 + 反思
│   │   ├── evolver.py      # L4 模板进化
│   │   ├── shadow.py       # L4 影子模式
│   │   └── master.py       # 顶层门面
│   └── templates/          # Agent YAML 模板(5 generic)
├── tests/                  # 195 单元测试
├── examples/               # 4 demo
├── experiments/            # ablation 脚本
├── docs/                   # 文档
├── README.md
├── CHANGELOG.md
├── SUBMISSION_SUMMARY.md
├── submission/             # 投稿材料
│   ├── paper/paper.pdf     # 11 页主论文
│   ├── code/               # 全源码
│   ├── reproduce/reproduce.sh
│   └── genesis-master-submission.zip  # 1.1 MB
└── reproduce.sh
```

## 🎯 与刘泽文研究主线的对接

| 维度 | 接续点 |
|---|---|
| **校准** | LLM-as-judge 偏差校准(Future Work)直接对接 [PAPER1-3 Calibration 主线](../research/index.md) |
| **多 Agent 协作** | 4 层反馈循环 = [Multi-Agent 协作框架](../concepts/multi-agent-collaboration.md) 的工程实现 |
| **A2A** | NegotiationEngine v9.0 直接对应 [A2A Protocol](../concepts/a2a.md) 概念页 |
| **Trust** | 工具三级风险 + 角色限制 ↔ [Trust 体系](../concepts/trust.md) T0-T4 等级 |
| **反思** | L4 影子模式 = Evolution 但带"谨慎验证",避免 LLM-as-judge 偏差放大 |

## 🪤 7/11 盘点时的纠错

- ❌ 旧印象:`genesis-master` 是 paper-writing-agent 的早期版本
- ✅ 真相:**独立 TMLR 投稿项目**(已投稿 v1.0),7/9 提交,7/10 做了 v1.0.1 post-submission patch 清理 v8/v9 supplementary material 标注
- 🪤 教训:**任何"已投稿 + 已发布"的项目都要查 submission 目录,不要只看 README 头部 status**

## 🛠️ 启动方式

```bash
cd F:\Research\genesis-master
pip install -r requirements.txt
# 可选: pip install chromadb gradio

# 端到端 demo
python examples/demo_research_report.py

# 迭代 demo(L1-L4 协作)
python examples/iteration_demo.py

# 消融实验(论文用)
python experiments/ablation_study.py --tasks 6 --runs 3

# Dashboard
pip install gradio
python examples/dashboard.py  # http://localhost:7860

# 测试
python -m pytest tests/ -v  # 195 passed
```

## 🔗 跨文档链接

- [PAPER1-6 总览](../research/index.md) — 6 篇 CONSOLIDATED 论文(含 **本项目是第 6 篇独立投稿**)
- [论文审阅工具箱](../analysis/paper-review-toolkit.md) — `paper-writing-agent` 是其上游
- [Tools 2026-07-10](../entities/tools-2026-07-10.md) — 与 40 项目速览对照
- [Multi-Agent 协作框架](../concepts/multi-agent-collaboration.md)
- [A2A Protocol](../concepts/a2a.md)
- [Trust 体系](../concepts/trust.md)
- [刘泽文 — 研究系统全图](./liu-zewen-research.md)

---

_最后更新:2026-07-11 13:40 · 泰 补_