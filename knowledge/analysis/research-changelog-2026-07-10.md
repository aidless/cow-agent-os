# 📚 研究生命周期 CHANGELOG — 2026-07-10

> 自动生成(facts 由 `scan_facts.py` 扫,narrative 从 `entities/liu-zewen-research.md` + `MEMORY.md` 抽取)。
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

**演化轨迹**: - `PAPER1_CONSOLIDATED` — 7/9 改进报告完成,12 句 Abstract + Limitations 章节已加
- **实验原料**:`experiments/`、`arxiv/`、`arxiv_1m/`、`arxiv_p13/p14/`、`arxiv_submission_paper1/`
- `paper-writing-agent/` — 21 模块论文写作 agent(v24.0,7/9 用于 PAPER1 改进)
| PAPER1 | 改进报告完成,待 BibTeX 编译 | 12 句 Abstract + Limitations 已加 |
- PAPER1 完成改进报告(7/9,12 句 Abstract + Limitations 已加)
- **工具链**:`paper-writing-agent` v24.0(7/9 已在 PAPER1 上跑通),`tmlr-review-simulator`,`tmlr_pipeline`

**下一步**: | PAPER1 | 改进报告完成,待 BibTeX 编译 | 12 句 Abstract + Limitations 已加 |

### 🟢 `PAPER2_CONSOLIDATED`

- **状态**: 🟢 audit-ready / final
- **路径**: `F:\Research\PAPER2_CONSOLIDATED`
- **字数 / 图表**: 4090 words / 0 figs / 2 tables / 0 algorithms
- **main.tex 大小**: 32.9 KB
- **协议 / 验证 / Release Notes**: ✓ / ✓ / ✓
- **Audit score**: 10 / 11
- **Verify scripts**: verify_p2.py, verify_p2.py

**演化轨迹**: - `PAPER2_CONSOLIDATED` — v9 构建脚本齐全(main_v9.tex + supplementary_v9.tex)
| PAPER2 | v9 已构建 | 需 v24.0 同样的 audit |
- PAPER2/3/4 待同款 audit

**下一步**: | PAPER2 | v9 已构建 | 需 v24.0 同样的 audit |
- PAPER2/3/4 待同款 audit

### 🟢 `PAPER4_CONSOLIDATED`

- **状态**: 🟢 audit-ready / final
- **路径**: `F:\Research\PAPER4_CONSOLIDATED`
- **字数 / 图表**: 6932 words / 2 figs / 6 tables / 0 algorithms
- **main.tex 大小**: 54.0 KB
- **协议 / 验证 / Release Notes**: ✓ / ✓ / ✗
- **Audit score**: 9 / 11
- **Verify scripts**: verify_p4.py, verify_p4.py

**演化轨迹**: - `PAPER4_CONSOLIDATED` — 标准结构,有 prebonferroni 备份
| PAPER4 | 标准模板 | 需 v24.0 同样的 audit |

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

**演化轨迹**: > Source: 2026-07-10 用户口述 + 实地扫描 F:\Research 根目录 + 读取 🏠_科研总览.md / 🖥️_项目总览.md / PAPER5_FINAL_REPORT.md
- `PAPER5_CONSOLIDATED` — 7/10 最终报告,verify_p5.py 6/6 PASS,**唯一可提交状态的论文**
- **过渡目录**:`FLAGSHIP`、`CONSOLIDATED_PAPER5`
| PAPER5 | **可提交** | verify_p5.py 6/6 PASS,25 页 PDF |
- PAPER5 已"可提交"(verify_p5.py 6/6 PASS,7/10 最终报告)

## 🟡 🟡 needs-audit (1 篇)

### 🟡 `PAPER3_CONSOLIDATED`

- **状态**: 🟡 needs-audit
- **路径**: `F:\Research\PAPER3_CONSOLIDATED`
- **字数 / 图表**: 5389 words / 0 figs / 11 tables / 0 algorithms
- **main.tex 大小**: 42.7 KB
- **协议 / 验证 / Release Notes**: ✓ / ✓ / ✗
- **Audit score**: 8 / 11
- **Verify scripts**: verify_p3.py, verify_p3.py

**演化轨迹**: - `PAPER3_CONSOLIDATED` — 标准结构,有 arxiv_submit 子目录
| PAPER3 | 标准模板 | 需 v24.0 同样的 audit |

**下一步**: | PAPER3 | 标准模板 | 需 v24.0 同样的 audit |

## 🟠 🟠 stub-with-tex (15 篇)

### 🟠 `CALIBRATION_EFFECTS`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\CALIBRATION_EFFECTS`
- **字数 / 图表**: 4468 words / 0 figs / 6 tables / 0 algorithms
- **main.tex 大小**: 40.1 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 3 / 11

**演化轨迹**: - **Calibration**:`CALIBRATION_EFFECTS`、`CALIBRATION_UNIFIED`、`RESAMPLING_CALIBRATION`

### 🟠 `CALIBRATION_UNIFIED`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\CALIBRATION_UNIFIED`
- **字数 / 图表**: 3438 words / 0 figs / 10 tables / 0 algorithms
- **main.tex 大小**: 28.5 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 3 / 11

**演化轨迹**: - **Calibration**:`CALIBRATION_EFFECTS`、`CALIBRATION_UNIFIED`、`RESAMPLING_CALIBRATION`

### 🟠 `FLAGSHIP`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\FLAGSHIP`
- **字数 / 图表**: 4707 words / 1 figs / 4 tables / 0 algorithms
- **main.tex 大小**: 38.7 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 3 / 11

**演化轨迹**: - `tmlr_flagship` + `tmlr_p6` / `p9` / `p10` / ... / `p19` — 早期分散版本
- **过渡目录**:`FLAGSHIP`、`CONSOLIDATED_PAPER5`

### 🟠 `RESAMPLING_CALIBRATION`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\RESAMPLING_CALIBRATION`
- **字数 / 图表**: 8254 words / 3 figs / 15 tables / 0 algorithms
- **main.tex 大小**: 66.1 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 4 / 11

**演化轨迹**: - **Calibration**:`CALIBRATION_EFFECTS`、`CALIBRATION_UNIFIED`、`RESAMPLING_CALIBRATION`

### 🟠 `TEMPORAL_DYNAMICS`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\TEMPORAL_DYNAMICS`
- **字数 / 图表**: 6963 words / 2 figs / 6 tables / 0 algorithms
- **main.tex 大小**: 55.9 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 4 / 11

**演化轨迹**: - **Temporal/Boundary**:`TEMPORAL_DYNAMICS`、`closing_landscape`、`boundary_sync_standalone`

### 🟠 `arxiv`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\arxiv`
- **字数 / 图表**: 4475 words / 0 figs / 6 tables / 0 algorithms
- **main.tex 大小**: 40.2 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 3 / 11

**演化轨迹**: - `PAPER3_CONSOLIDATED` — 标准结构,有 arxiv_submit 子目录
- **Contagion**:`calibration_contagion`、`contagion_networks`、`memory_contagion`、`arxiv_contagion`
- **实验原料**:`experiments/`、`arxiv/`、`arxiv_1m/`、`arxiv_p13/p14/`、`arxiv_submission_paper1/`
- 但用户重新拉回:**arxiv-tracker + rr-responder**(A+B)→ **我自己交付**
| `arxiv-tracker` | ✅ live | `knowledge/concepts/arxiv-watch/arxiv-2026-07-10.md` (555 行,38 篇 ≥3星) |
- arxiv-tracker + rr-responder 都基于此 key 跑通

### 🟠 `arxiv_contagion`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\arxiv_contagion`
- **字数 / 图表**: 6791 words / 2 figs / 5 tables / 0 algorithms
- **main.tex 大小**: 52.9 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 4 / 11

**演化轨迹**: - **Contagion**:`calibration_contagion`、`contagion_networks`、`memory_contagion`、`arxiv_contagion`

### 🟠 `arxiv_submission_paper1`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\arxiv_submission_paper1`
- **字数 / 图表**: 5555 words / 2 figs / 9 tables / 0 algorithms
- **main.tex 大小**: 45.0 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 3 / 11

**演化轨迹**: - **实验原料**:`experiments/`、`arxiv/`、`arxiv_1m/`、`arxiv_p13/p14/`、`arxiv_submission_paper1/`

### 🟠 `calibration_contagion`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\calibration_contagion`
- **字数 / 图表**: 6813 words / 2 figs / 5 tables / 0 algorithms
- **main.tex 大小**: 53.1 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 4 / 11

**演化轨迹**: - **Contagion**:`calibration_contagion`、`contagion_networks`、`memory_contagion`、`arxiv_contagion`

### 🟠 `impossibility_triangle`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\impossibility_triangle`
- **字数 / 图表**: 3777 words / 3 figs / 3 tables / 0 algorithms
- **main.tex 大小**: 29.1 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 3 / 11

**演化轨迹**: - **Impossibility Triangle**:`impossibility_triangle` + `impossibility_triangle_consolidated`

### 🟠 `impossibility_triangle_consolidated`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\impossibility_triangle_consolidated`
- **字数 / 图表**: 3676 words / 2 figs / 5 tables / 0 algorithms
- **main.tex 大小**: 32.9 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 3 / 11

**演化轨迹**: - **Impossibility Triangle**:`impossibility_triangle` + `impossibility_triangle_consolidated`

### 🟠 `memory_architecture`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\memory_architecture`
- **字数 / 图表**: 3794 words / 3 figs / 5 tables / 0 algorithms
- **main.tex 大小**: 32.4 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 3 / 11

**演化轨迹**: - `BAAI_Knowledge_Base/`、`memory_architecture/` — 知识库 / 记忆架构研究

### 🟠 `tmlr_flagship`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\tmlr_flagship`
- **字数 / 图表**: 4707 words / 1 figs / 4 tables / 0 algorithms
- **main.tex 大小**: 38.7 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 3 / 11

**演化轨迹**: - `tmlr_flagship` + `tmlr_p6` / `p9` / `p10` / ... / `p19` — 早期分散版本

### 🟠 `tmlr_p12`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\tmlr_p12`
- **字数 / 图表**: 5169 words / 2 figs / 5 tables / 0 algorithms
- **main.tex 大小**: 39.3 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 3 / 11

### 🟠 `tmlr_p6`

- **状态**: 🟠 stub-with-tex
- **路径**: `F:\Research\tmlr_p6`
- **字数 / 图表**: 3374 words / 3 figs / 2 tables / 0 algorithms
- **main.tex 大小**: 28.4 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 3 / 11

**演化轨迹**: - `tmlr_flagship` + `tmlr_p6` / `p9` / `p10` / ... / `p19` — 早期分散版本

## 🔴 🔴 stub-only (18 篇)

### 🔴 `CONSOLIDATED_PAPER5`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\CONSOLIDATED_PAPER5`
- **字数 / 图表**: 2251 words / 5 figs / 5 tables / 0 algorithms
- **main.tex 大小**: 20.1 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

**演化轨迹**: - **过渡目录**:`FLAGSHIP`、`CONSOLIDATED_PAPER5`

### 🔴 `PAPER6_CONSOLIDATED`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\PAPER6_CONSOLIDATED`
- **字数 / 图表**: (无 main.tex)
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 0 / 11

**演化轨迹**: - `PAPER6_CONSOLIDATED` — 7/9 新起,目前仅 `main.tex.LLM_FABRICATED_DO_NOT_SUBMIT` 废稿,**stub 状态**
| PAPER6 | stub | LLM_FABRICATED 废稿,无实质内容 |
- PAPER6 是 7/9 新起的 stub,目前只有废稿

**下一步**: - `PAPER6_CONSOLIDATED` — 7/9 新起,目前仅 `main.tex.LLM_FABRICATED_DO_NOT_SUBMIT` 废稿,**stub 状态**
| PAPER6 | stub | LLM_FABRICATED 废稿,无实质内容 |
- PAPER6 是 7/9 新起的 stub,目前只有废稿

### 🔴 `arxiv_p13`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\arxiv_p13`
- **字数 / 图表**: 1712 words / 3 figs / 1 tables / 0 algorithms
- **main.tex 大小**: 15.3 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

**演化轨迹**: - **实验原料**:`experiments/`、`arxiv/`、`arxiv_1m/`、`arxiv_p13/p14/`、`arxiv_submission_paper1/`

### 🔴 `arxiv_p14`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\arxiv_p14`
- **字数 / 图表**: 1439 words / 1 figs / 1 tables / 0 algorithms
- **main.tex 大小**: 12.5 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

### 🔴 `closing_landscape`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\closing_landscape`
- **字数 / 图表**: 2350 words / 0 figs / 1 tables / 0 algorithms
- **main.tex 大小**: 21.0 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

**演化轨迹**: - **Temporal/Boundary**:`TEMPORAL_DYNAMICS`、`closing_landscape`、`boundary_sync_standalone`

### 🔴 `memory_contagion`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\memory_contagion`
- **字数 / 图表**: (无 main.tex)
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 0 / 11

**演化轨迹**: - **Contagion**:`calibration_contagion`、`contagion_networks`、`memory_contagion`、`arxiv_contagion`

### 🔴 `tmlr_p10`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\tmlr_p10`
- **字数 / 图表**: 1237 words / 0 figs / 1 tables / 0 algorithms
- **main.tex 大小**: 11.1 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

### 🔴 `tmlr_p11`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\tmlr_p11`
- **字数 / 图表**: 928 words / 0 figs / 2 tables / 0 algorithms
- **main.tex 大小**: 7.7 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

### 🔴 `tmlr_p13`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\tmlr_p13`
- **字数 / 图表**: 548 words / 0 figs / 1 tables / 0 algorithms
- **main.tex 大小**: 4.7 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

### 🔴 `tmlr_p14`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\tmlr_p14`
- **字数 / 图表**: 1439 words / 1 figs / 1 tables / 0 algorithms
- **main.tex 大小**: 12.5 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

### 🔴 `tmlr_p15`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\tmlr_p15`
- **字数 / 图表**: 1543 words / 1 figs / 1 tables / 0 algorithms
- **main.tex 大小**: 13.8 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

### 🔴 `tmlr_p16`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\tmlr_p16`
- **字数 / 图表**: 1837 words / 1 figs / 1 tables / 0 algorithms
- **main.tex 大小**: 14.4 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

### 🔴 `tmlr_p17`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\tmlr_p17`
- **字数 / 图表**: 1304 words / 1 figs / 0 tables / 0 algorithms
- **main.tex 大小**: 10.6 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

### 🔴 `tmlr_p18`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\tmlr_p18`
- **字数 / 图表**: 67 words / 0 figs / 0 tables / 0 algorithms
- **main.tex 大小**: 1.0 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

### 🔴 `tmlr_p19`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\tmlr_p19`
- **字数 / 图表**: 105 words / 0 figs / 0 tables / 0 algorithms
- **main.tex 大小**: 1.4 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

### 🔴 `tmlr_p20_k_generalization`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\tmlr_p20_k_generalization`
- **字数 / 图表**: 105 words / 0 figs / 0 tables / 0 algorithms
- **main.tex 大小**: 1.4 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

**演化轨迹**: - `tmlr_p20_k_generalization`、`tmlr_p21_self_eval_causal` — 两个新方向分支(可能尚未合并)

**下一步**: - `tmlr_p20_k_generalization`、`tmlr_p21_self_eval_causal` — 两个新方向分支(可能尚未合并)

### 🔴 `tmlr_p21_self_eval_causal`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\tmlr_p21_self_eval_causal`
- **字数 / 图表**: 105 words / 0 figs / 0 tables / 0 algorithms
- **main.tex 大小**: 1.4 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11

**演化轨迹**: - `tmlr_p20_k_generalization`、`tmlr_p21_self_eval_causal` — 两个新方向分支(可能尚未合并)

**下一步**: - `tmlr_p20_k_generalization`、`tmlr_p21_self_eval_causal` — 两个新方向分支(可能尚未合并)

### 🔴 `tmlr_p9`

- **状态**: 🔴 stub-only
- **路径**: `F:\Research\tmlr_p9`
- **字数 / 图表**: 2234 words / 0 figs / 1 tables / 0 algorithms
- **main.tex 大小**: 20.1 KB
- **协议 / 验证 / Release Notes**: ✗ / ✗ / ✗
- **Audit score**: 1 / 11
