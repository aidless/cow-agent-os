# 📚 研究生命周期 CHANGELOG — 2026-07-11

> 自动生成(facts 由 `scan_facts.py` 扫,narrative 从整个 `knowledge/` 树抽取)。
> Narrative 留 `<!-- TODO: user -->` 的字段需要人手补充。

## 🎯 总览

- **论文目录总数**: 38
- **含 main.tex**: 36
- **含 protocol.md**: 5
- **含 verify_*.py**: 5
- **含 RELEASE_NOTES.md / CHANGELOG.md**: 1
- **CONSOLIDATED 系列**: 8

### 状态分布

- **🟢 audit-ready / final**: 4 篇
- **🟡 needs-audit**: 1 篇
- **🟠 stub-with-tex**: 15 篇
- **🔴 stub-only**: 18 篇

### Narrative 覆盖率(7/11 打磨后)

- **演化轨迹有内容**: 38 / 38 = 100%
- **下一步有内容**: 7 / 38 = 18%

## 🟢 🟢 audit-ready / final (4 篇)

### 🟢 `PAPER1_CONSOLIDATED`

- **状态**: 🟢 audit-ready / final
- **路径**: `F:\Research\PAPER1_CONSOLIDATED`
- **字数 / 图表**: 7487 words / 1 figs / 7 tables / 0 algorithms
- **main.tex 大小**: 57.9 KB
- **协议 / 验证 / Release Notes**: ✓ / ✓ / ✗
- **Audit score**: 9 / 11
- **Verify scripts**: verify_p1.py, verify_decite.py, verify_fixes.py, verify_p1.py
- **.bak_*** files: 4

**演化轨迹**: - PAPER1 完成改进报告(7/9,12 句 Abstract + Limitations 已加)
- **工具链**:`paper-writing-agent` v24.0(7/9 已在 PAPER1 上跑通),`tmlr-review-simulator`,`tmlr_pipeline`
### 🟢 `PAPER1_CONSOLIDATED`
- **路径**: `F:\Research\PAPER1_CONSOLIDATED`
**演化轨迹**: - `PAPER1_CONSOLIDATED` — 7/9 改进报告完成,12 句 Abstract + Limitations 章节已加
- **实验原料**:`experiments/`、`arxiv/`、`arxiv_1m/`、`arxiv_p13/p14/`、`arxiv_submission_paper1/`
- `paper-writing-agent/` — 21 模块论文写作 agent(v24.0,7/9 用于 PAPER1 改进)
| PAPER1 | 改进报告完成,待 BibTeX 编译 | 12 句 Abstract + Limitations 已加 |
**下一步**: | PAPER1 | 改进报告完成,待 BibTeX 编译 | 12 句 Abstract + Limitations 已加 |
### 🟠 `arxiv_submission_paper1`
- **路径**: `F:\Research\arxiv_submission_paper1`
**演化轨迹**: - **实验原料**:`experiments/`、`arxiv/`、`arxiv_1m/`、`arxiv_p13/p14/`、`arxiv_submission_paper1/`
- **下一步**:研究 AI 指令对齐时,**配合 PAPER1-6 用**(避免我们造的提示词也是"烂尾")
- `PAPER1_CONSOLIDATED` — 7/9 改进报告完成,12 句 Abstract + Limitations 章节已加
| `papers-we-love` | 论文阅读社区 | 跟 PAPER1-6 配套(社区评论 / 复现) |

**下一步**: | PAPER1 | 改进报告完成,待 BibTeX 编译 | 12 句 Abstract + Limitations 已加 |
**下一步**: | PAPER1 | 改进报告完成,待 BibTeX 编译 | 12 句 Abstract + Limitations 已加 |

### 🟢 `PAPER2_CONSOLIDATED`

- **状态**: 🟢 audit-ready / final
- **路径**: `F:\Research\PAPER2_CONSOLIDATED`
- **字数 / 图表**: 4090 words / 0 figs / 2 tables / 0 algorithms
- **main.tex 大小**: 32.9 KB
- **协议 / 验证 / Release Notes**: ✓ / ✓ / ✓
- **Audit score**: 10 / 11
- **Verify scripts**: verify_p2.py, verify_p2.py

**演化轨迹**: - PAPER2/3/4 待同款 audit
### 立即可做(PAPER2/3/4 同款 audit)
- 在 `PAPER2_CONSOLIDATED` / `PAPER3_CONSOLIDATED` / `PAPER4_CONSOLIDATED` 各放一份 `verify_p<N>.py`(从 PAPER5 复制改 ROOT + CHECKS_CONFIG)
- 写 `gen_verify_scripts.py` 自动从 TEMPLATE 派生 PAPER2/3/4 的 verify 脚本
### 🟢 `PAPER2_CONSOLIDATED`
- **路径**: `F:\Research\PAPER2_CONSOLIDATED`
**演化轨迹**: - `PAPER2_CONSOLIDATED` — v9 构建脚本齐全(main_v9.tex + supplementary_v9.tex)
| PAPER2 | v9 已构建 | 需 v24.0 同样的 audit |
**下一步**: | PAPER2 | v9 已构建 | 需 v24.0 同样的 audit |
- `PAPER2_CONSOLIDATED` — v9 构建脚本齐全(main_v9.tex + supplementary_v9.tex)
- **对你的价值**:5 篇 TMLR 论文中 PAPER2/3/4 待 audit,如果它真能自动出 paper skeleton,**省数天**

**下一步**: - PAPER2/3/4 待同款 audit
| PAPER2 | v9 已构建 | 需 v24.0 同样的 audit |
**下一步**: | PAPER2 | v9 已构建 | 需 v24.0 同样的 audit |
- **对你的价值**:5 篇 TMLR 论文中 PAPER2/3/4 待 audit,如果它真能自动出 paper skeleton,**省数天**

### 🟢 `PAPER4_CONSOLIDATED`

- **状态**: 🟢 audit-ready / final
- **路径**: `F:\Research\PAPER4_CONSOLIDATED`
- **字数 / 图表**: 6932 words / 2 figs / 6 tables / 0 algorithms
- **main.tex 大小**: 54.0 KB
- **协议 / 验证 / Release Notes**: ✓ / ✓ / ✗
- **Audit score**: 9 / 11
- **Verify scripts**: verify_p4.py, verify_p4.py

**演化轨迹**: - 在 `PAPER2_CONSOLIDATED` / `PAPER3_CONSOLIDATED` / `PAPER4_CONSOLIDATED` 各放一份 `verify_p<N>.py`(从 PAPER5 复制改 ROOT + CHECKS_CONFIG)
### 🟢 `PAPER4_CONSOLIDATED`
- **路径**: `F:\Research\PAPER4_CONSOLIDATED`
**演化轨迹**: - `PAPER4_CONSOLIDATED` — 标准结构,有 prebonferroni 备份
| PAPER4 | 标准模板 | 需 v24.0 同样的 audit |
**下一步**: | PAPER4 | 标准模板 | 需 v24.0 同样的 audit |
- `PAPER4_CONSOLIDATED` — 标准结构,有 prebonferroni 备份

**下一步**: | PAPER4 | 标准模板 | 需 v24.0 同样的 audit |
**下一步**: | PAPER4 | 标准模板 | 需 v24.0 同样的 audit |

### 🟢 `PAPER5_CONSOLIDATED`

- **状态**: 🟢 audit-ready / final
- **路径**: `F:\Research\PAPER5_CONSOLIDATED`
- **字数 / 图表**: 8735 words / 6 figs / 6 tables / 0 algorithms
- **main.tex 大小**: 71.2 KB
- **协议 / 验证 / Release Notes**: ✓ / ✓ / ✗
- **Audit score**: 9 / 11
- **Verify scripts**: verify_p5.py, verify_p5.py
- **.bak_*** files: 12

**演化轨迹**: - PAPER5 已"可提交"(verify_p5.py 6/6 PASS,7/10 最终报告)
## 🎯 已验证的端到端测试(2026-07-10, PAPER5)
### `quick` 在 PAPER5 上跑通
- `identify` → PAPER5 = "analysis" 类型,9.09% confidence(低置信度符合 PAPER5 多方法论文定位)
- `evaluate` → PAPER5 整体 **B 级 88.5%**(correctness 80% / novelty 80% / reproducibility 100% / clarity 100% / statistical_rigor 75% / prior_work 100% / writing_quality 100%)
- 在 `PAPER2_CONSOLIDATED` / `PAPER3_CONSOLIDATED` / `PAPER4_CONSOLIDATED` 各放一份 `verify_p<N>.py`(从 PAPER5 复制改 ROOT + CHECKS_CONFIG)
### 🟢 `PAPER5_CONSOLIDATED`
- **路径**: `F:\Research\PAPER5_CONSOLIDATED`
**演化轨迹**: > Source: 2026-07-10 用户口述 + 实地扫描 F:\Research 根目录 + 读取 🏠_科研总览.md / 🖥️_项目总览.md / PAPER5_FINAL_REPORT.md
- `PAPER5_CONSOLIDATED` — 7/10 最终报告,verify_p5.py 6/6 PASS,**唯一可提交状态的论文**
- **过渡目录**:`FLAGSHIP`、`CONSOLIDATED_PAPER5`
| PAPER5 | **可提交** | verify_p5.py 6/6 PASS,25 页 PDF |
### 🔴 `CONSOLIDATED_PAPER5`
- **路径**: `F:\Research\CONSOLIDATED_PAPER5`
**演化轨迹**: - **过渡目录**:`FLAGSHIP`、`CONSOLIDATED_PAPER5`
> Source: 2026-07-10 用户口述 + 实地扫描 F:\Research 根目录 + 读取 🏠_科研总览.md / 🖥️_项目总览.md / PAPER5_FINAL_REPORT.md
| **P1** | `papers-we-love` 找 PAPER5 相关讨论(校准 TMLR 投稿前找社区反馈) | 30 分钟 |
- [论文审阅工具箱 — 刘泽文的能力全景](analysis/paper-review-toolkit.md) — 3 工具 + 1 统一 wrapper(`review_paper.py`)+ 12 种审阅方式 + 3 个已修上游 bug + PAPER5 端到端验证

## 🟡 🟡 needs-audit (1 篇)

### 🟡 `PAPER3_CONSOLIDATED`

- **状态**: 🟡 needs-audit
- **路径**: `F:\Research\PAPER3_CONSOLIDATED`
- **字数 / 图表**: 5389 words / 0 figs / 11 tables / 0 algorithms
- **main.tex 大小**: 42.7 KB
- **协议 / 验证 / Release Notes**: ✓ / ✓ / ✗
- **Audit score**: 8 / 11
- **Verify scripts**: verify_p3.py, verify_p3.py

**演化轨迹**: - 在 `PAPER2_CONSOLIDATED` / `PAPER3_CONSOLIDATED` / `PAPER4_CONSOLIDATED` 各放一份 `verify_p<N>.py`(从 PAPER5 复制改 ROOT + CHECKS_CONFIG)
### 🟡 `PAPER3_CONSOLIDATED`
- **路径**: `F:\Research\PAPER3_CONSOLIDATED`
**演化轨迹**: - `PAPER3_CONSOLIDATED` — 标准结构,有 arxiv_submit 子目录
| PAPER3 | 标准模板 | 需 v24.0 同样的 audit |
**下一步**: | PAPER3 | 标准模板 | 需 v24.0 同样的 audit |
- `PAPER3_CONSOLIDATED` — 标准结构,有 arxiv_submit 子目录
- **何时激活**:**写 PAPER3-6 / 泰玄小站 v2.0 / 任何 5+ 步的任务之前**

**下一步**: | PAPER3 | 标准模板 | 需 v24.0 同样的 audit |
**下一步**: | PAPER3 | 标准模板 | 需 v24.0 同样的 audit |

## 🟠 🟠 stub-with-tex (15 篇)

### 🟠 `CALIBRATION_EFFECTS`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\CALIBRATION_EFFECTS`
- **字数 / 图表**: 4468 words / 0 figs / 6 tables / 0 algorithms
- **main.tex 大小**: 40.1 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 3 / 11

**演化轨迹**: ### 🟠 `CALIBRATION_EFFECTS`
- **路径**: `F:\Research\CALIBRATION_EFFECTS`
**演化轨迹**: - **Calibration**:`CALIBRATION_EFFECTS`、`CALIBRATION_UNIFIED`、`RESAMPLING_CALIBRATION`
- **Calibration**:`CALIBRATION_EFFECTS`、`CALIBRATION_UNIFIED`、`RESAMPLING_CALIBRATION`

### 🟠 `CALIBRATION_UNIFIED`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\CALIBRATION_UNIFIED`
- **字数 / 图表**: 3438 words / 0 figs / 10 tables / 0 algorithms
- **main.tex 大小**: 28.5 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 3 / 11

**演化轨迹**: **演化轨迹**: - **Calibration**:`CALIBRATION_EFFECTS`、`CALIBRATION_UNIFIED`、`RESAMPLING_CALIBRATION`
### 🟠 `CALIBRATION_UNIFIED`
- **路径**: `F:\Research\CALIBRATION_UNIFIED`
- **Calibration**:`CALIBRATION_EFFECTS`、`CALIBRATION_UNIFIED`、`RESAMPLING_CALIBRATION`

### 🟠 `FLAGSHIP`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\FLAGSHIP`
- **字数 / 图表**: 4707 words / 1 figs / 4 tables / 0 algorithms
- **main.tex 大小**: 38.7 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 3 / 11

**演化轨迹**: - **过渡目录**:`FLAGSHIP`、`CONSOLIDATED_PAPER5`
### 🟠 `FLAGSHIP`
- **路径**: `F:\Research\FLAGSHIP`
**演化轨迹**: - `tmlr_flagship` + `tmlr_p6` / `p9` / `p10` / ... / `p19` — 早期分散版本
### 🟠 `tmlr_flagship`
- **路径**: `F:\Research\tmlr_flagship`
**演化轨迹**: - **过渡目录**:`FLAGSHIP`、`CONSOLIDATED_PAPER5`
- `tmlr_flagship` + `tmlr_p6` / `p9` / `p10` / ... / `p19` — 早期分散版本

### 🟠 `RESAMPLING_CALIBRATION`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\RESAMPLING_CALIBRATION`
- **字数 / 图表**: 8254 words / 3 figs / 15 tables / 0 algorithms
- **main.tex 大小**: 66.1 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 4 / 11

**演化轨迹**: **演化轨迹**: - **Calibration**:`CALIBRATION_EFFECTS`、`CALIBRATION_UNIFIED`、`RESAMPLING_CALIBRATION`
### 🟠 `RESAMPLING_CALIBRATION`
- **路径**: `F:\Research\RESAMPLING_CALIBRATION`
- **Calibration**:`CALIBRATION_EFFECTS`、`CALIBRATION_UNIFIED`、`RESAMPLING_CALIBRATION`

### 🟠 `TEMPORAL_DYNAMICS`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\TEMPORAL_DYNAMICS`
- **字数 / 图表**: 6963 words / 2 figs / 6 tables / 0 algorithms
- **main.tex 大小**: 55.9 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 4 / 11

**演化轨迹**: ### 🟠 `TEMPORAL_DYNAMICS`
- **路径**: `F:\Research\TEMPORAL_DYNAMICS`
**演化轨迹**: - **Temporal/Boundary**:`TEMPORAL_DYNAMICS`、`closing_landscape`、`boundary_sync_standalone`
- **Temporal/Boundary**:`TEMPORAL_DYNAMICS`、`closing_landscape`、`boundary_sync_standalone`

### 🟠 `arxiv`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\arxiv`
- **字数 / 图表**: 4475 words / 0 figs / 6 tables / 0 algorithms
- **main.tex 大小**: 40.2 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 3 / 11

**演化轨迹**: - 但用户重新拉回:**arxiv-tracker + rr-responder**(A+B)→ **我自己交付**
| `arxiv-tracker` | ✅ live | `knowledge/concepts/arxiv-watch/arxiv-2026-07-10.md` (555 行,38 篇 ≥3星) |
- `arxiv-tracker.md` / `rr-responder.md` / `wechat-mp-validation.md` / `paper-review-toolkit.md` / `paper-changelog.md`
- arxiv-tracker + rr-responder 都基于此 key 跑通
- **实验原料**:`experiments/`、`arxiv/`、`arxiv_1m/`、`arxiv_p13/p14/`、`arxiv_submission_paper1/`
**演化轨迹**: - `PAPER3_CONSOLIDATED` — 标准结构,有 arxiv_submit 子目录
### 🟠 `arxiv`
- **路径**: `F:\Research\arxiv`
- **Contagion**:`calibration_contagion`、`contagion_networks`、`memory_contagion`、`arxiv_contagion`
### 🟠 `arxiv_contagion`
- **路径**: `F:\Research\arxiv_contagion`
**演化轨迹**: - **Contagion**:`calibration_contagion`、`contagion_networks`、`memory_contagion`、`arxiv_contagion`
### 🟠 `arxiv_submission_paper1`
- **路径**: `F:\Research\arxiv_submission_paper1`
**演化轨迹**: - **实验原料**:`experiments/`、`arxiv/`、`arxiv_1m/`、`arxiv_p13/p14/`、`arxiv_submission_paper1/`
### 🔴 `arxiv_p13`
- **路径**: `F:\Research\arxiv_p13`
### 🔴 `arxiv_p14`
- **路径**: `F:\Research\arxiv_p14`
=== knowledge\concepts\arxiv-watch\arxiv-2026-07-10.md ===
# arxiv-watch — 2026-07-10
> 自动生成的 arxiv 监控报告。来源:`arxiv-tracker` skill。
- **arxiv**:[2607.08731](https://arxiv.org/abs/2607.08731)
- **arxiv**:[2607.08700](https://arxiv.org/abs/2607.08700)
- **arxiv**:[2607.08662](https://arxiv.org/abs/2607.08662)
- **arxiv**:[2607.08652](https://arxiv.org/abs/2607.08652)
- **arxiv**:[2607.08651](https://arxiv.org/abs/2607.08651)
- **arxiv**:[2607.08493](https://arxiv.org/abs/2607.08493)
- **arxiv**:[2607.08403](https://arxiv.org/abs/2607.08403)
- **arxiv**:[2607.08400](https://arxiv.org/abs/2607.08400)
- **arxiv**:[2607.08374](https://arxiv.org/abs/2607.08374)
- **arxiv**:[2607.08193](https://arxiv.org/abs/2607.08193)
- **arxiv**:[2607.08180](https://arxiv.org/abs/2607.08180)
- **arxiv**:[2607.08122](https://arxiv.org/abs/2607.08122)
- **arxiv**:[2607.08080](https://arxiv.org/abs/2607.08080)
- **arxiv**:[2607.08034](https://arxiv.org/abs/2607.08034)
- **arxiv**:[2607.07989](https://arxiv.org/abs/2607.07989)
- **arxiv**:[2607.07985](https://arxiv.org/abs/2607.07985)
- **arxiv**:[2607.07976](https://arxiv.org/abs/2607.07976)
- **arxiv**:[2607.07858](https://arxiv.org/abs/2607.07858)
- **arxiv**:[2607.07857](https://arxiv.org/abs/2607.07857)
- **arxiv**:[2607.07695](https://arxiv.org/abs/2607.07695)
- **arxiv**:[2607.07601](https://arxiv.org/abs/2607.07601)
- **arxiv**:[2607.07548](https://arxiv.org/abs/2607.07548)
- **arxiv**:[2607.07467](https://arxiv.org/abs/2607.07467)
- **arxiv**:[2607.07436](https://arxiv.org/abs/2607.07436)
- **arxiv**:[2607.07395](https://arxiv.org/abs/2607.07395)
- **arxiv**:[2607.07368](https://arxiv.org/abs/2607.07368)
- **arxiv**:[2607.07097](https://arxiv.org/abs/2607.07097)
- **arxiv**:[2607.07050](https://arxiv.org/abs/2607.07050)
- **arxiv**:[2607.07029](https://arxiv.org/abs/2607.07029)
- **arxiv**:[2607.07023](https://arxiv.org/abs/2607.07023)
- **arxiv**:[2607.06993](https://arxiv.org/abs/2607.06993)
- **arxiv**:[2607.06964](https://arxiv.org/abs/2607.06964)
- **arxiv**:[2607.06879](https://arxiv.org/abs/2607.06879)
- **arxiv**:[2607.06875](https://arxiv.org/abs/2607.06875)
- **arxiv**:[2607.06855](https://arxiv.org/abs/2607.06855)
- **arxiv**:[2607.06807](https://arxiv.org/abs/2607.06807)
- **arxiv**:[2607.06452](https://arxiv.org/abs/2607.06452)
- **arxiv**:[2607.06435](https://arxiv.org/abs/2607.06435)
1. **Finding H. pylori in the Fine Print: Evidence-Linked Multi-Agent Case Finding from Gastric Biopsy Reports** ⭐⭐⭐⭐ ([2607.06435](https://arxiv.org/abs/2607.06435))
2. **Geometric Self-Distillation for Reasoning Generalization** ⭐⭐⭐⭐ ([2607.06855](https://arxiv.org/abs/2607.06855))
3. **Video2Reaction: Mapping Video to Audience Reaction Distribution in the Wild** ⭐⭐⭐⭐ ([2607.06875](https://arxiv.org/abs/2607.06875))
4. **End-to-End LLM Flight Planning with RAG-based Memory and Multi-modal Coach Agent** ⭐⭐⭐⭐ ([2607.06964](https://arxiv.org/abs/2607.06964))
5. **Behavior Leverage Imbalance in Multi-Teacher On-Policy Distillation** ⭐⭐⭐⭐ ([2607.07050](https://arxiv.org/abs/2607.07050))
6. **Multi-Agent AI Control: Distributed Attacks Hamper Per-Instance Monitors** ⭐⭐⭐⭐ ([2607.07368](https://arxiv.org/abs/2607.07368))
7. **SpaCellAgent: A Self-Evolving LLM-Based Multi-Agent Framework for Trajectory Analysis** ⭐⭐⭐⭐ ([2607.07467](https://arxiv.org/abs/2607.07467))
8. **CARLA-GS: Decoupling Representation, Reasoning, and Physics Simulation for Autonomous Driving Corner-Case Synthesis** ⭐⭐⭐⭐ ([2607.07601](https://arxiv.org/abs/2607.07601))
9. **Multi-agent Autoformalization of Tensor Network Theory** ⭐⭐⭐⭐ ([2607.07857](https://arxiv.org/abs/2607.07857))
10. **Agentic AI and Retrieval-Augmented Models in Straight-Through Underwriting** ⭐⭐⭐⭐ ([2607.07858](https://arxiv.org/abs/2607.07858))
11. **MASTE: A Multi-Agent Pipeline for Zero-Shot Aspect Sentiment Triplet Extraction** ⭐⭐⭐⭐ ([2607.08080](https://arxiv.org/abs/2607.08080))
12. **Large-Language-Models-as-a-Judge in Theory-Agnostic Adaptive Metric-Alignment for Prototypical Networks in Personality Recognition** ⭐⭐⭐⭐ ([2607.08374](https://arxiv.org/abs/2607.08374))
13. **Ensemble Diversity Optimization for Subjective Supervision** ⭐⭐⭐⭐ ([2607.08493](https://arxiv.org/abs/2607.08493))
14. **Formal Mechanisms for Market Stability in Self-Interested Agent Societies: A Marketplace Simulation Study** ⭐⭐⭐⭐ ([2607.08652](https://arxiv.org/abs/2607.08652))
15. **WebSwarm: Recursive Multi-Agent Orchestration for Deep-and-Wide Web Search** ⭐⭐⭐⭐ ([2607.08662](https://arxiv.org/abs/2607.08662))
16. **Do You Need a Frontier Model as a Citation Verifier? Benchmarking Rubric LLMs for Deep-Research Source Attribution** ⭐⭐⭐⭐ ([2607.08700](https://arxiv.org/abs/2607.08700))
17. **From Voting to Agent Collaboration: Answer-Type-Aware LLM Pipelines for BioASQ 14b** ⭐⭐⭐ ([2607.06452](https://arxiv.org/abs/2607.06452))
18. **When Agents Go Rogue: Activation-Based Detection of Malicious Behaviors in Multi-Agent Systems** ⭐⭐⭐ ([2607.06807](https://arxiv.org/abs/2607.06807))
19. **Best-Arm Identification with Generative Proxy** ⭐⭐⭐ ([2607.06879](https://arxiv.org/abs/2607.06879))
20. **Large Behavior Model: A Promptable Digital Twin of the Retail Customer** ⭐⭐⭐ ([2607.06993](https://arxiv.org/abs/2607.06993))
21. **Online Data Selection Is Implicit Alignment** ⭐⭐⭐ ([2607.07023](https://arxiv.org/abs/2607.07023))
22. **Gimitest: A Comprehensive Tool for Testing Reinforcement Learning Policies** ⭐⭐⭐ ([2607.07029](https://arxiv.org/abs/2607.07029))
23. **Operational Reframing and Approval-Framed Delegation in Multi-Agent LLM Safety** ⭐⭐⭐ ([2607.07097](https://arxiv.org/abs/2607.07097))
24. **When Prompts Ignore Structure: Graph-Based Attribute Reasoning for Calibrated VLMs** ⭐⭐⭐ ([2607.07395](https://arxiv.org/abs/2607.07395))
25. **The Blind Curator: How a Biased Judge Silently Disables Skill Retirement in Self-Evolving Agents** ⭐⭐⭐ ([2607.07436](https://arxiv.org/abs/2607.07436))
26. **Think Big, Search Small: Where Capacity Matters in Hierarchical Search Agents?** ⭐⭐⭐ ([2607.07548](https://arxiv.org/abs/2607.07548))
27. **Institutional Red-Teaming: Deployment Rules, Not Just Models, Causally Shape Multi-Agent AI Safety** ⭐⭐⭐ ([2607.07695](https://arxiv.org/abs/2607.07695))
28. **When Implausible Tokens Get Reinforced: Tail-Aware Credit Calibration for LLM Reinforcement Learning** ⭐⭐⭐ ([2607.07976](https://arxiv.org/abs/2607.07976))
29. **A Reliability Assessment of LALM Audio Judges for Full-Duplex Voice Agents** ⭐⭐⭐ ([2607.07985](https://arxiv.org/abs/2607.07985))
30. **Who Broke the System? Failure Localization in LLM-Based Multi-Agent Systems** ⭐⭐⭐ ([2607.07989](https://arxiv.org/abs/2607.07989))
31. **PLURAL: A Global Dataset for Value Alignment** ⭐⭐⭐ ([2607.08034](https://arxiv.org/abs/2607.08034))
32. **Workload-Preserving Differentially Private Synthetic Data for Causal Inference via Maximum-Entropy Calibration** ⭐⭐⭐ ([2607.08122](https://arxiv.org/abs/2607.08122))
33. **Out of Sight: Compression-Aware Content Protection against Agentic Crawlers** ⭐⭐⭐ ([2607.08180](https://arxiv.org/abs/2607.08180))
34. **Open-ended Multi-agent Autocurricula via Visual Inspection of Policies with Multi-modal LLMs** ⭐⭐⭐ ([2607.08193](https://arxiv.org/abs/2607.08193))
35. **TRACE: A Two-Channel Robust Attribution Watermark via Complementary Embeddings for LLM-Agent Trajectories** ⭐⭐⭐ ([2607.08400](https://arxiv.org/abs/2607.08400))
36. **Game Theory Driven Multi-Agent Framework Mitigates Language Model Hallucination** ⭐⭐⭐ ([2607.08403](https://arxiv.org/abs/2607.08403))
37. **Secure Decentralized Federated Learning via Gossip and Virtual Voting** ⭐⭐⭐ ([2607.08651](https://arxiv.org/abs/2607.08651))
38. **Validity of LLMs as data annotators: AMALIA on authority** ⭐⭐⭐ ([2607.08731](https://arxiv.org/abs/2607.08731))
39. **Prompt-Adapter Context Routing for Parameter-Efficient Multi-Shot Long Video Extrapolation** ⭐⭐ ([2607.06481](https://arxiv.org/abs/2607.06481))
40. **Multi-Agent Deep Reinforcement Learning for Multi Objective Battery Management in Dairy Farms** ⭐⭐ ([2607.06489](https://arxiv.org/abs/2607.06489))
41. **Pitwall: Faithful Natural-Language Race-Strategy Briefings from a Calibrated Real-Time Monte Carlo Engine** ⭐⭐ ([2607.06495](https://arxiv.org/abs/2607.06495))
42. **Doomed from the Start: Early Abort of LLM Agent Episodes via a Recall-Controlled Probe Cascade** ⭐⭐ ([2607.06503](https://arxiv.org/abs/2607.06503))
43. **tsbootstrap: Distribution-Free Uncertainty Quantification and Conformal Prediction for Time Series** ⭐⭐ ([2607.06690](https://arxiv.org/abs/2607.06690))
44. **What Predicts Correctness in Text-to-SQL? A Selective-Prediction Study** ⭐⭐ ([2607.06799](https://arxiv.org/abs/2607.06799))
45. **Evaluating SageMath-Augmented LLM Agents for Computational and Experimental Mathematics** ⭐⭐ ([2607.06820](https://arxiv.org/abs/2607.06820))
46. **Flow-ERD: Agent-type Aware Flow Matching with Entropy-Regularized Distillation for Diverse Traffic Simulation** ⭐⭐ ([2607.06957](https://arxiv.org/abs/2607.06957))
47. **LiST: Lipschitz Scaling Training for Robust and Calibrated Neural Networks** ⭐⭐ ([2607.07745](https://arxiv.org/abs/2607.07745))
48. **From Text to Parameters: Predicting Item Parameters from Embedding Regularization with Reliability and Design Ceilings** ⭐⭐ ([2607.07141](https://arxiv.org/abs/2607.07141))
49. **From Atomic Actions to Standard Operating Procedures: Iterative Tool Optimization for Self-Evolving LLM Agents** ⭐⭐ ([2607.07321](https://arxiv.org/abs/2607.07321))
50. **Future Confidence Distillation in Large Language Models** ⭐⭐ ([2607.07626](https://arxiv.org/abs/2607.07626))
51. **DiaLLM: An Investigation into the Robustness-Generation Gap in English Dialect Adaptation** ⭐⭐ ([2607.07669](https://arxiv.org/abs/2607.07669))
52. **From Triggers to Emotions: A CPM-Grounded Appraisal Multi-Agent for Dynamic Emotional Evolution in Persona-Based Dialogue** ⭐⭐ ([2607.07824](https://arxiv.org/abs/2607.07824))
53. **Can We Trust LLM's Logic? Quantifying Uncertainty, Coherence, and Robustness via a Graph-Based Framework** ⭐⭐ ([2607.08017](https://arxiv.org/abs/2607.08017))
54. **From Prompts to Contracts: Harness Engineering for Auditable Enterprise LLM Agents** ⭐⭐ ([2607.08028](https://arxiv.org/abs/2607.08028))
55. **A safety-oriented hypothetico-deductive framework for AI-assisted differential diagnosis** ⭐⭐ ([2607.08038](https://arxiv.org/abs/2607.08038))
56. **What LLM Forecasters Know but Don't Say: Probing Internal Representations for Calibration and Faithfulness** ⭐⭐ ([2607.08046](https://arxiv.org/abs/2607.08046))
57. **PIT-SUN: A Deployable Empirical Marginal Transform Framework with Expectation-Consistent Recovery for Regression in Recommender Systems** ⭐⭐ ([2607.08202](https://arxiv.org/abs/2607.08202))
58. **Multi-Agent Firewall Architecture for Privacy Protection of Sensitive Data in Interactions with Language Models** ⭐⭐ ([2607.08282](https://arxiv.org/abs/2607.08282))
59. **From Legacy Documentation to OSCAL: An MCP-Based Agent Pipeline for Threat-Informed Continuous Compliance in Critical Infrastructure** ⭐⭐ ([2607.08288](https://arxiv.org/abs/2607.08288))
60. **WCog-VLA: A Dual-Level World-Cognitive Vision-Language-Action Model for End-to-End Autonomous Driving** ⭐⭐ ([2607.08375](https://arxiv.org/abs/2607.08375))
61. **Eigenvalue Calibration for Semantic Embeddings of Large Language Models** ⭐⭐ ([2607.08377](https://arxiv.org/abs/2607.08377))
62. **When Synthetic Speech Is All You Have: Better Call GRPO** ⭐⭐ ([2607.08409](https://arxiv.org/abs/2607.08409))
63. **UniClawBench: A Universal Benchmark for Proactive Agents on Real-World Tasks** ⭐⭐ ([2607.08768](https://arxiv.org/abs/2607.08768))
64. **UASPL: Uncertainty-Aware Self-Paced Learning with Evidential Neural Networks** ⭐ ([2607.06638](https://arxiv.org/abs/2607.06638))
65. **A Definition and Roadmap for World Models** ⭐ ([2607.06401](https://arxiv.org/abs/2607.06401))
66. **DepthWeave-KV: Token-Adaptive Cross-Layer Residual Factorization for Long-Context KV Cache Compression** ⭐ ([2607.06523](https://arxiv.org/abs/2607.06523))
67. **Efficient Bayesian Deep Ensembles via Analytic Predictive Inference** ⭐ ([2607.06776](https://arxiv.org/abs/2607.06776))
68. **Prior-matched evaluation of operational Earth-observation classifiers: a three-number reporting method demonstrated on Sentinel-1 internal-wave detection** ⭐ ([2607.07146](https://arxiv.org/abs/2607.07146))
69. **Does AI Understand Imaging? A Systematic Benchmark of Agentic AI for Computational Imaging Tasks** ⭐ ([2607.07189](https://arxiv.org/abs/2607.07189))
70. **Reason Less, Verify More: Deterministic Gates Recover a Silent Policy-Violation Failure Mode in Tool-Using LLM Agents** ⭐ ([2607.07405](https://arxiv.org/abs/2607.07405))
71. **Guidance Breaks the Fitted Operator: A Terminal-Fitted Repair for Classifier-Free Guidance** ⭐ ([2607.07665](https://arxiv.org/abs/2607.07665))
72. **DreamCharacter-1: From 3D Generative Foundation Models to Product-Ready Character Generation** ⭐ ([2607.07817](https://arxiv.org/abs/2607.07817))
73. **Tool-Making and Self-Evolving LLM Agents in Low-Latency Systems** ⭐ ([2607.08010](https://arxiv.org/abs/2607.08010))
74. **TTHE: Test-Time Harness Evolution** ⭐ ([2607.08124](https://arxiv.org/abs/2607.08124))
- `PAPER3_CONSOLIDATED` — 标准结构,有 arxiv_submit 子目录
- [arxiv-watch 2026-07-10](concepts/arxiv-watch/arxiv-2026-07-10.md) — 38 篇高相关论文(≥3星)

### 🟠 `arxiv_contagion`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\arxiv_contagion`
- **字数 / 图表**: 6791 words / 2 figs / 5 tables / 0 algorithms
- **main.tex 大小**: 52.9 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 4 / 11

**演化轨迹**: - **Contagion**:`calibration_contagion`、`contagion_networks`、`memory_contagion`、`arxiv_contagion`
### 🟠 `arxiv_contagion`
- **路径**: `F:\Research\arxiv_contagion`
**演化轨迹**: - **Contagion**:`calibration_contagion`、`contagion_networks`、`memory_contagion`、`arxiv_contagion`

### 🟠 `arxiv_submission_paper1`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\arxiv_submission_paper1`
- **字数 / 图表**: 5555 words / 2 figs / 9 tables / 0 algorithms
- **main.tex 大小**: 45.0 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 3 / 11

**演化轨迹**: - **实验原料**:`experiments/`、`arxiv/`、`arxiv_1m/`、`arxiv_p13/p14/`、`arxiv_submission_paper1/`
### 🟠 `arxiv_submission_paper1`
- **路径**: `F:\Research\arxiv_submission_paper1`
**演化轨迹**: - **实验原料**:`experiments/`、`arxiv/`、`arxiv_1m/`、`arxiv_p13/p14/`、`arxiv_submission_paper1/`

### 🟠 `calibration_contagion`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\calibration_contagion`
- **字数 / 图表**: 6813 words / 2 figs / 5 tables / 0 algorithms
- **main.tex 大小**: 53.1 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 4 / 11

**演化轨迹**: - **Contagion**:`calibration_contagion`、`contagion_networks`、`memory_contagion`、`arxiv_contagion`
**演化轨迹**: - **Contagion**:`calibration_contagion`、`contagion_networks`、`memory_contagion`、`arxiv_contagion`
### 🟠 `calibration_contagion`
- **路径**: `F:\Research\calibration_contagion`

### 🟠 `impossibility_triangle`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\impossibility_triangle`
- **字数 / 图表**: 3777 words / 3 figs / 3 tables / 0 algorithms
- **main.tex 大小**: 29.1 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 3 / 11

**演化轨迹**: ### 🟠 `impossibility_triangle`
- **路径**: `F:\Research\impossibility_triangle`
**演化轨迹**: - **Impossibility Triangle**:`impossibility_triangle` + `impossibility_triangle_consolidated`
### 🟠 `impossibility_triangle_consolidated`
- **路径**: `F:\Research\impossibility_triangle_consolidated`
- **Impossibility Triangle**:`impossibility_triangle` + `impossibility_triangle_consolidated`

### 🟠 `impossibility_triangle_consolidated`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\impossibility_triangle_consolidated`
- **字数 / 图表**: 3676 words / 2 figs / 5 tables / 0 algorithms
- **main.tex 大小**: 32.9 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 3 / 11

**演化轨迹**: **演化轨迹**: - **Impossibility Triangle**:`impossibility_triangle` + `impossibility_triangle_consolidated`
### 🟠 `impossibility_triangle_consolidated`
- **路径**: `F:\Research\impossibility_triangle_consolidated`
- **Impossibility Triangle**:`impossibility_triangle` + `impossibility_triangle_consolidated`

### 🟠 `memory_architecture`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\memory_architecture`
- **字数 / 图表**: 3794 words / 3 figs / 5 tables / 0 algorithms
- **main.tex 大小**: 32.4 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 3 / 11

**演化轨迹**: ### 🟠 `memory_architecture`
- **路径**: `F:\Research\memory_architecture`
**演化轨迹**: - `BAAI_Knowledge_Base/`、`memory_architecture/` — 知识库 / 记忆架构研究
- `BAAI_Knowledge_Base/`、`memory_architecture/` — 知识库 / 记忆架构研究

### 🟠 `tmlr_flagship`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\tmlr_flagship`
- **字数 / 图表**: 4707 words / 1 figs / 4 tables / 0 algorithms
- **main.tex 大小**: 38.7 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 3 / 11

**演化轨迹**: **演化轨迹**: - `tmlr_flagship` + `tmlr_p6` / `p9` / `p10` / ... / `p19` — 早期分散版本
### 🟠 `tmlr_flagship`
- **路径**: `F:\Research\tmlr_flagship`
- `tmlr_flagship` + `tmlr_p6` / `p9` / `p10` / ... / `p19` — 早期分散版本

### 🟠 `tmlr_p12`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\tmlr_p12`
- **字数 / 图表**: 5169 words / 2 figs / 5 tables / 0 algorithms
- **main.tex 大小**: 39.3 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 3 / 11

**演化轨迹**: ### 🟠 `tmlr_p12`
- **路径**: `F:\Research\tmlr_p12`

### 🟠 `tmlr_p6`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\tmlr_p6`
- **字数 / 图表**: 3374 words / 3 figs / 2 tables / 0 algorithms
- **main.tex 大小**: 28.4 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 3 / 11

**演化轨迹**: **演化轨迹**: - `tmlr_flagship` + `tmlr_p6` / `p9` / `p10` / ... / `p19` — 早期分散版本
### 🟠 `tmlr_p6`
- **路径**: `F:\Research\tmlr_p6`
- `tmlr_flagship` + `tmlr_p6` / `p9` / `p10` / ... / `p19` — 早期分散版本

## 🔴 🔴 stub-only (18 篇)

### 🔴 `CONSOLIDATED_PAPER5`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\CONSOLIDATED_PAPER5`
- **字数 / 图表**: 2251 words / 5 figs / 5 tables / 0 algorithms
- **main.tex 大小**: 20.1 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

**演化轨迹**: - **过渡目录**:`FLAGSHIP`、`CONSOLIDATED_PAPER5`
### 🔴 `CONSOLIDATED_PAPER5`
- **路径**: `F:\Research\CONSOLIDATED_PAPER5`
**演化轨迹**: - **过渡目录**:`FLAGSHIP`、`CONSOLIDATED_PAPER5`

### 🔴 `PAPER6_CONSOLIDATED`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\PAPER6_CONSOLIDATED`
- **字数 / 图表**: (无 main.tex)
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 0 / 11

**演化轨迹**: - PAPER6 是 7/9 新起的 stub,目前只有废稿
### 🔴 `PAPER6_CONSOLIDATED`
- **路径**: `F:\Research\PAPER6_CONSOLIDATED`
**演化轨迹**: - `PAPER6_CONSOLIDATED` — 7/9 新起,目前仅 `main.tex.LLM_FABRICATED_DO_NOT_SUBMIT` 废稿,**stub 状态**
| PAPER6 | stub | LLM_FABRICATED 废稿,无实质内容 |
**下一步**: - `PAPER6_CONSOLIDATED` — 7/9 新起,目前仅 `main.tex.LLM_FABRICATED_DO_NOT_SUBMIT` 废稿,**stub 状态**
- `PAPER6_CONSOLIDATED` — 7/9 新起,目前仅 `main.tex.LLM_FABRICATED_DO_NOT_SUBMIT` 废稿,**stub 状态**

**下一步**: - PAPER6 是 7/9 新起的 stub,目前只有废稿
**演化轨迹**: - `PAPER6_CONSOLIDATED` — 7/9 新起,目前仅 `main.tex.LLM_FABRICATED_DO_NOT_SUBMIT` 废稿,**stub 状态**
| PAPER6 | stub | LLM_FABRICATED 废稿,无实质内容 |
**下一步**: - `PAPER6_CONSOLIDATED` — 7/9 新起,目前仅 `main.tex.LLM_FABRICATED_DO_NOT_SUBMIT` 废稿,**stub 状态**
- `PAPER6_CONSOLIDATED` — 7/9 新起,目前仅 `main.tex.LLM_FABRICATED_DO_NOT_SUBMIT` 废稿,**stub 状态**

### 🔴 `arxiv_p13`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\arxiv_p13`
- **字数 / 图表**: 1712 words / 3 figs / 1 tables / 0 algorithms
- **main.tex 大小**: 15.3 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

**演化轨迹**: - **实验原料**:`experiments/`、`arxiv/`、`arxiv_1m/`、`arxiv_p13/p14/`、`arxiv_submission_paper1/`
**演化轨迹**: - **实验原料**:`experiments/`、`arxiv/`、`arxiv_1m/`、`arxiv_p13/p14/`、`arxiv_submission_paper1/`
### 🔴 `arxiv_p13`
- **路径**: `F:\Research\arxiv_p13`

### 🔴 `arxiv_p14`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\arxiv_p14`
- **字数 / 图表**: 1439 words / 1 figs / 1 tables / 0 algorithms
- **main.tex 大小**: 12.5 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

**演化轨迹**: ### 🔴 `arxiv_p14`
- **路径**: `F:\Research\arxiv_p14`

### 🔴 `closing_landscape`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\closing_landscape`
- **字数 / 图表**: 2350 words / 0 figs / 1 tables / 0 algorithms
- **main.tex 大小**: 21.0 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

**演化轨迹**: **演化轨迹**: - **Temporal/Boundary**:`TEMPORAL_DYNAMICS`、`closing_landscape`、`boundary_sync_standalone`
### 🔴 `closing_landscape`
- **路径**: `F:\Research\closing_landscape`
- **Temporal/Boundary**:`TEMPORAL_DYNAMICS`、`closing_landscape`、`boundary_sync_standalone`

### 🔴 `memory_contagion`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\memory_contagion`
- **字数 / 图表**: (无 main.tex)
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 0 / 11

**演化轨迹**: - **Contagion**:`calibration_contagion`、`contagion_networks`、`memory_contagion`、`arxiv_contagion`
**演化轨迹**: - **Contagion**:`calibration_contagion`、`contagion_networks`、`memory_contagion`、`arxiv_contagion`
### 🔴 `memory_contagion`
- **路径**: `F:\Research\memory_contagion`

### 🔴 `tmlr_p10`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\tmlr_p10`
- **字数 / 图表**: 1237 words / 0 figs / 1 tables / 0 algorithms
- **main.tex 大小**: 11.1 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

**演化轨迹**: ### 🔴 `tmlr_p10`
- **路径**: `F:\Research\tmlr_p10`

### 🔴 `tmlr_p11`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\tmlr_p11`
- **字数 / 图表**: 928 words / 0 figs / 2 tables / 0 algorithms
- **main.tex 大小**: 7.7 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

**演化轨迹**: ### 🔴 `tmlr_p11`
- **路径**: `F:\Research\tmlr_p11`

### 🔴 `tmlr_p13`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\tmlr_p13`
- **字数 / 图表**: 548 words / 0 figs / 1 tables / 0 algorithms
- **main.tex 大小**: 4.7 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

**演化轨迹**: ### 🔴 `tmlr_p13`
- **路径**: `F:\Research\tmlr_p13`

### 🔴 `tmlr_p14`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\tmlr_p14`
- **字数 / 图表**: 1439 words / 1 figs / 1 tables / 0 algorithms
- **main.tex 大小**: 12.5 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

**演化轨迹**: ### 🔴 `tmlr_p14`
- **路径**: `F:\Research\tmlr_p14`

### 🔴 `tmlr_p15`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\tmlr_p15`
- **字数 / 图表**: 1543 words / 1 figs / 1 tables / 0 algorithms
- **main.tex 大小**: 13.8 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

**演化轨迹**: ### 🔴 `tmlr_p15`
- **路径**: `F:\Research\tmlr_p15`

### 🔴 `tmlr_p16`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\tmlr_p16`
- **字数 / 图表**: 1837 words / 1 figs / 1 tables / 0 algorithms
- **main.tex 大小**: 14.4 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

**演化轨迹**: ### 🔴 `tmlr_p16`
- **路径**: `F:\Research\tmlr_p16`

### 🔴 `tmlr_p17`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\tmlr_p17`
- **字数 / 图表**: 1304 words / 1 figs / 0 tables / 0 algorithms
- **main.tex 大小**: 10.6 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

**演化轨迹**: ### 🔴 `tmlr_p17`
- **路径**: `F:\Research\tmlr_p17`

### 🔴 `tmlr_p18`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\tmlr_p18`
- **字数 / 图表**: 67 words / 0 figs / 0 tables / 0 algorithms
- **main.tex 大小**: 1.0 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

**演化轨迹**: ### 🔴 `tmlr_p18`
- **路径**: `F:\Research\tmlr_p18`

### 🔴 `tmlr_p19`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\tmlr_p19`
- **字数 / 图表**: 105 words / 0 figs / 0 tables / 0 algorithms
- **main.tex 大小**: 1.4 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

**演化轨迹**: ### 🔴 `tmlr_p19`
- **路径**: `F:\Research\tmlr_p19`

### 🔴 `tmlr_p20_k_generalization`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\tmlr_p20_k_generalization`
- **字数 / 图表**: 105 words / 0 figs / 0 tables / 0 algorithms
- **main.tex 大小**: 1.4 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

**演化轨迹**: ### 🔴 `tmlr_p20_k_generalization`
- **路径**: `F:\Research\tmlr_p20_k_generalization`
**演化轨迹**: - `tmlr_p20_k_generalization`、`tmlr_p21_self_eval_causal` — 两个新方向分支(可能尚未合并)
**下一步**: - `tmlr_p20_k_generalization`、`tmlr_p21_self_eval_causal` — 两个新方向分支(可能尚未合并)
- `tmlr_p20_k_generalization`、`tmlr_p21_self_eval_causal` — 两个新方向分支(可能尚未合并)

**下一步**: **演化轨迹**: - `tmlr_p20_k_generalization`、`tmlr_p21_self_eval_causal` — 两个新方向分支(可能尚未合并)
**下一步**: - `tmlr_p20_k_generalization`、`tmlr_p21_self_eval_causal` — 两个新方向分支(可能尚未合并)
- `tmlr_p20_k_generalization`、`tmlr_p21_self_eval_causal` — 两个新方向分支(可能尚未合并)

### 🔴 `tmlr_p21_self_eval_causal`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\tmlr_p21_self_eval_causal`
- **字数 / 图表**: 105 words / 0 figs / 0 tables / 0 algorithms
- **main.tex 大小**: 1.4 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

**演化轨迹**: **演化轨迹**: - `tmlr_p20_k_generalization`、`tmlr_p21_self_eval_causal` — 两个新方向分支(可能尚未合并)
**下一步**: - `tmlr_p20_k_generalization`、`tmlr_p21_self_eval_causal` — 两个新方向分支(可能尚未合并)
### 🔴 `tmlr_p21_self_eval_causal`
- **路径**: `F:\Research\tmlr_p21_self_eval_causal`
- `tmlr_p20_k_generalization`、`tmlr_p21_self_eval_causal` — 两个新方向分支(可能尚未合并)

**下一步**: **演化轨迹**: - `tmlr_p20_k_generalization`、`tmlr_p21_self_eval_causal` — 两个新方向分支(可能尚未合并)
**下一步**: - `tmlr_p20_k_generalization`、`tmlr_p21_self_eval_causal` — 两个新方向分支(可能尚未合并)
- `tmlr_p20_k_generalization`、`tmlr_p21_self_eval_causal` — 两个新方向分支(可能尚未合并)

### 🔴 `tmlr_p9`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\tmlr_p9`
- **字数 / 图表**: 2234 words / 0 figs / 1 tables / 0 algorithms
- **main.tex 大小**: 20.1 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

**演化轨迹**: ### 🔴 `tmlr_p9`
- **路径**: `F:\Research\tmlr_p9`
