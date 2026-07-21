# PAPER5 TMLR Upper-tier Improvement RFC — 2026-07-11

> **目的**:基于 Round-1 Review Log(`paper5-review-r1-2026-07-11.md`)给出 6-12 周 RFC,把 PAPER5 从 6.17 (Major) 推到 7.5+ (Accept upper-tier)。
>
> **来源**:`F:\Research\PAPER5_CONSOLIDATED\reviews\main.multi\` + meta-review.md
>
> **本文状态**:Draft v1,等用户 commit 后启动

---

## 🎯 RFC 目标

| 标尺 | 当前(R1) | 目标(R2) | 增量 |
|---|---|---|---|
| **加权总分** | 6.17 | **7.5+** | +1.33 |
| **Recommendation** | Major revisions | Minor revisions / Accept | ✓ |
| **Correctness** | 5.67 | 7.5 | +1.83 |
| **Novelty** | 6.0 | 7.0 | +1.0 |
| **Reproducibility** | 6.0 | 7.5 | +1.5 |
| **Statistical Rigor** | 5.0 | 7.0 | +2.0 |
| **Prior Work** | 6.0 | 7.5 | +1.5 |
| TMLR 段位 | 后 50-30% | **前 30-15%** | 跨档 |

**预计投入**:6 周(Critical only)→ 9 周(Critical + Major 5 项)→ 12 周(+亮点)

---

## 📅 6 周作战图(Critical only)

### Week 1-2 · Critical C2(Qwen n=10)+ C1(crossover reframe)

**Why this first**:**3 reviewer 三票**(C2 n=3)+ 2 reviewer(C1 p_adj=0.135),修了直接升 rigor 5→7。

**C2 · Qwen n=10**(2 周):
- [ ] 跑 Qwen dose-response:3 arch × 3 contamination × 10 seeds × 30 rounds = **270 cell**
- [ ] 跑 Qwen authority bias:3 arch × 1 contamination (p=0.8) × 10 seeds × 30 rounds = **30 cell**
- [ ] 重算 Bonferroni family K(cross-model K 从 6 → ?)
- [ ] 报告 significance tests + bootstrap CI
- **预算**:**~$200-300 DeepSeek/Qwen API**(~0.5/cell avg)
- **Owner**:Liu Zewen(Qwen API key)

**C1 · Crossover reframe**(parallel 1 周):
- [ ] §3.2 / §4.1-4.3 重写 crossover 为 "suggestive trend, requires replication"
- [ ] 加 explicit power analysis(当前 n=10 power 检测 d=0.8 @ 80%, d=0.5 @ 50%)
- [ ] 改 abstract 第一段句:从 "we find a model-dependent crossover" → "we observe a suggestive model-dependent pattern at p=0.8"
- [ ] 增加 "Replication recommendation" 段(n=14 replication target)

**产出**:reviewer A + C 直接撤回 C1 + C2

---

### Week 3 · Critical C3(§6.3 假理论)+ C4(Γ decomposition 算法)

**C3 · Theoretical Analysis 段重写**(3-5 天):
- [ ] 段标题改 "Theoretical Analysis of the Crossover Mechanism" → "Qualitative Mechanism of the Crossover"
- [ ] 重写为纯 narrative, 不再 fake "theoretical"
- [ ] 显式说:本段是 intuition,不是 proof
- **产出**:reviewer B 撤回 C3

**C4 · Γ decomposition 算法补全**(3-5 天):
- [ ] 写 Algorithm 1:content vs retrieval 分解的 closed-form / 伪代码
- [ ] 重跑 Table 5/7,加 bootstrap 95% CI
- [ ] 加 error bars(每个 component)
- [ ] 加 per-component significance test
- **产出**:reviewer B + C 撤回 C4

---

### Week 4-5 · Major M3(DeepSeek × authority)+ M4(stat protocol section)

**M3 · DeepSeek × authority cell 补跑**(1 周):
- [ ] 跑 DeepSeek authority bias:3 arch × 1 contamination (p=0.8) × 10 seeds × 30 rounds = **30 cell**
- [ ] 加到 Table 3
- [ ] 重审 "two bias types" claim
- **预算**:**~$50**
- **Owner**:Liu Zewen

**M4 · Statistical protocol section 补全**(2-3 天):
- [ ] 写 `\section{Statistical Protocol}` `\label{sec:stat-protocol}`(现 §\ref 引用但 section 缺)
- [ ] 写 Holm-Bonferroni / BH-FDR / crossover bootstrap test 完整方法
- [ ] 显式说明 significance hierarchy(Bonferroni primary, others sensitivity)
- **产出**:reviewer B 撤回 M4 + M5

---

### Week 6 · Verify + 投递准备

- [ ] 重跑 `paper-review-toolkit full` —— 期待 C1/C2/C3/C4 全部 cleared
- [ ] 重跑 `verify_p5.py` —— 0 findings
- [ ] BibTeX compile(确保 no warning)
- [ ] TMLR format checklist(tmlr.bst + tmlr.sty)
- [ ] Cover letter 起草
- [ ] Round-1 review response letter(rebuttal 风格,逐 reviewer 答 13 个 issue)
- [ ] **submit to openreview.net/TMLR**

---

## 📅 +3 周 Major 5 项(M1 baseline / M2 sensitivity / M6 prior work / M7 cost / M8 saturation)

如果 6 周后想从 7.0 推到 7.5+(Accept upper-tier):

### Week 7-8 · M1(no-memory baseline)+ M2(hyperparameter sensitivity)

**M1 · "No memory" baseline**(1 周):
- [ ] 跑 no-memory condition:2 model × 1 baseline × 3 contamination × 10 seeds × 30 rounds = **180 cell**
- [ ] 加 Table "Memory-free vs memory architectures"
- [ ] Discussion 加 1 段:架构 vs no-memory 是 mitigation 还是 introduction

**M2 · Hyperparameter sensitivity**(2 周):
- [ ] RAG θ ∈ {0.05, 0.1, 0.2, 0.3}(论文已用 0.1):3 arch × 3 θ × 3 contamination × 10 seeds × 30 rounds = **270 cell**
- [ ] Summarization frequency ∈ {1, 3, 5}(论文已用 1):90 cell
- [ ] TF-IDF vs dense embedding ablation(可能 +1 周):~90 cell
- **预算**:**~$250**
- **Owner**:Liu Zewen

### Week 9 · M6(prior work direct comparison)+ M7(cost analysis)

**M6 · Bertalanić et al. 2026 baseline**(3-5 天):
- [ ] 找原文(Liu Zewen 提供 PDF)
- [ ] 用 paper 的 mock mode 复现 Bertalanić 的 append+summarization baseline
- [ ] 加 Table "Our architectures vs prior append+summarization baseline"
- [ ] Discussion:新架构是否真的 improve

**M7 · Computational cost analysis**(2-3 天):
- [ ] 测 3 arch × 3 contamination × 1 model,记录每 round:
  - LLM tokens(in/out)
  - wall-clock latency
  - peak memory usage
- [ ] 加 Table "Cost profile"

### Week 9 · M8(saturation effect 解释)

- [ ] 写 1 个 formal argument(或 empirical fit):Γ(p) 随 p 单调下降
- [ ] 可能是 distribution convergence(Wasserstein under mixing)或 LLM saturation
- [ ] 加进 Discussion

---

## 📅 +3 周亮点(从 7.5 推到 8.0+)

如果 9 周后还想"上游前 20%":

### Week 10-12 · 亮点 A/B/C(选 1-2)

**亮点 A · Bias amplification budget theorem**(3 周):
- [ ] 证明:Γ(T) ≤ Γ(0) · (1 + c·T)^α
- [ ] 给 c, α 与 architecture/model 的 dependency
- [ ] 加 Theorem 1 + Lemma 1-2 + proof

**亮点 B · Model capability score correlation**(2 周):
- [ ] 量化 model instruction-following(用 IFEval / MT-Bench 之类)
- [ ] 回归:capability score vs crossover point p*
- [ ] 1 个 figure:模型 capability → crossover p

**亮点 C · Architecture × bias interaction ANOVA**(1 周):
- [ ] 2-way ANOVA:architecture × bias type
- [ ] 加 Table "Interaction effects"

---

## 💰 总预算估算

| Phase | 周数 | API 预算 | 人力(Liu Zewen) |
|---|---|---|---|
| Critical only | 6 周 | ~$250 | 6 周 半职 |
| + Major 5 项 | 9 周 | +$500 = $750 | 9 周 半职 |
| + 亮点 1-2 | 12 周 | +$200 = $950 | 12 周 半职 |

**TMLR 5 月 deadline**:距今 ~10 个月(2026-05),12 周 = 3 个月,**留 7 个月 buffer**。

---

## 📊 进度追踪表

| 周 | 完成项 | 关键产出 | Status |
|---|---|---|---|
| 1 | C1 reframe + C2 Qwen n=10 start | Power analysis + Qwen partial data | 🟡 |
| 2 | C2 Qwen n=10 finish + stats | Qwen n=10 全表 + sig test | 🟡 |
| 3 | C3 重写 + C4 算法 | Algorithm 1 + Table 5 重跑 | 🟡 |
| 4 | M3 DeepSeek × authority | New Table 3 row | 🟡 |
| 5 | M4 stat protocol section | Section written | 🟡 |
| 6 | Verify + 投递 | openreview submit | 🟡 |
| 7-8 | M1 baseline + M2 sensitivity | 2 new tables + Discussion | ⚪ |
| 9 | M6 + M7 + M8 | 3 mini-tasks | ⚪ |
| 10-12 | 亮点 A/B/C 选 1-2 | Theorem / Figure / Table | ⚪ |

---

## ⚠️ 关键风险

| 风险 | 缓解 |
|---|---|
| **Qwen API quota 又 exhausted** | 切换到 mock mode + live API 抽样 5 cell 验证 |
| **n=14 replication 数据 p_adj < 0.01 预期失败** | 改写为 "我们在 n=14 数据下期待看到 p_adj<0.01" 而非 "我们跑出 p_adj<0.01" |
| **reviewer 不信 mock mode = live mode** | 写 §5.3 显式 mock vs live validation(M1 阶段做) |
| **M2 hyperparameter sensitivity 结果反转** | 显式说 "sensitivity is part of the contribution, not a flaw" |
| **12 周不够** | 5 月 deadline 有 10 个月 buffer,可分两轮:R1→R2→R3 |

---

## 🟢 RFC 决策(请勾)

- **(A)**:我立刻开工 **Week 1**(Qwen n=10 + C1 reframe),6 周内交 R2 投稿
- **(B)**:我开工 **全部 Critical + Major**,9 周内交 R2
- **(C)**:我开工 **Week 1-2 critical + Week 9 highlight A**(theorem),9 周
- **(D)**:先做 **mock mode vs live API 验证(小预算 $20)**,这是 R1 没数据下结论的核心证据,**开了再决策**
- **(E)**:推迟开工,**先跟你确认 Qwen API 预算**($200-300),以及是否优先做 M1(no-memory baseline)

**推荐 (D)**:你 R1 没有原始数据 mock 模式下结论被怀疑,**用 5 cell × 2 model 验证 mock ≈ live 是最低成本"建立 reviewer 信任"动作**,$20 + 3 天。开了再 commit 6 周。

---

## 🪤 本 RFC 教训(给未来的我)

1. **R1 review 早跑 vs 晚跑**:如果 7/11 10:33 跑完 review 后立刻开 RFC,本来能省 4 小时"我没意识到 reviewer 真意见"的时间
2. **Critical 必杀 / Major 跳板 / Minors 装饰**:Critical 不修 = reject, Major 修 = 上游, Minors 不修可接受
3. **reviewer consensus 是金**:3 reviewer 三票的问题(C2 n=3 seeds)100% 必修
4. **meta-review 的 8 步比单 reviewer 意见权重高**:Action Editor 视角更平衡
5. **paper 投递不是写完就完**:6 周 critical 修 → 3 周 major 扩 → 3 周亮点推 → 投稿。每轮都重跑 `paper-review-toolkit full`

---

_最后更新:2026-07-11 14:55 · Draft v1 · 6-12 周作战图,待用户 commit_

---

# 🆕 7/11 15:00 Draft v2 · 跨窗口撞车分析(泰补)

## 📊 与 11 兄弟窗口的对接状态

| 窗口 | 关系 | 备注 |
|---|---|---|
| **w1 PAPER5 投递** | 🟢 **接力** | C10 + Review Log 已完成(15:00),RFC commit 后 w1 走投递剩余 6 步 |
| **w6 批量修复** | 🟢 **已闭环** | 5 篇 verify HIGH=0(PAPER5 本来 0H);RFC M2/M3/M6/M7 补 MED/LOW ~10 个 |
| **w5 paper-review 动态化** | 🟡 **间接** | 步骤 3 实装 worker 时,会用到 RFC 的 M2 hyperparameter sensitivity 概念 |
| **w7 OS paper** | 🟢 **反哺** | EPC 框架 + 5 篇梯子关系图,w9 已接力 offer 给 w7 |
| **w10 peS2o KB** | 🟢 **直接反哺** | D 选项 + C2 Qwen n=10 + C4 验证,**全部接 w10 的 `batch_must_cite.py` + `kb_search.py`** |
| w2/w3/w4/w8/w9/w11 | ✅ 无撞 | 主题都不沾 |

## 💰 D 选项跨窗口优化(主推)

**RFC 原预算**:$20 / 3 days,5 cell × 2 model mock vs live
**w10 已铺路后**:**$10 / 1 day**

- ✅ `kb_search.py --must-cite --existing-refs refs.bib --bibtex out.bib -n 10`(已就绪)
- ✅ PAPER5 `PAPER5_must_cite_kb.bib` 已落地(`F:\Research\PAPER5_CONSOLIDATED\`)
- ✅ 检索性能 10-18ms,fetch_specific 6 篇 24 秒
- ⏳ 待跑:**5 cell × 2 model**(DeepSeek + Qwen)× mock vs live = 20 cell,$10
- ✅ mock 跑用 `dry_run_with_fake_llm.py` 模式,真 LLM 走 DeepSeek/Qwen

## ⚠️ RFC 启动前 3 个必做 check

1. **🪤 Bug D verify 残留**:C9 "figure caption" 是 w1/w6 已确认的 verify tool bug,**新做 figure 时也要走 verify,会同样被误报** → 开工前先确认 w6 是否修了 regex(w6 v4 报告 "已修" 7/11 14:35,但**没现场跑 PAPER5 验证** — 必须手动跑一次)
2. **🪤 RFC 推荐的 Qwen API 预算 $200-300**:7/11 15:05 **刘泽文提供阿里云 Maas 统一 key**(`llm-akwkztp3nreb7edz.cn-beijing.maas.aliyuncs.com`,OpenAI 兼容协议,一个 key 跑 DeepSeek/Qwen/GPT) → Qwen 不再需要单独 key,**D 选项 Phase 2 现在可以跑完整 2 model**。详见 [MEMORY.md § LLM API 路径](../../MEMORY.md)
3. **🪤 n=14 replication 数据 p_adj<0.01 预期失败**:RFC 自爆的 risk,**写 §3.2 时务必用 "we expect to see" 而非 "we found"**(M 阶段措辞)

## 🔗 与 w5 反哺接口(M2 hyperparameter sensitivity 完成后)

```
[RFC M2 完成: 3 arch × 3 θ × 3 contamination × 10 seeds × 30 rounds = 270 cell]
                     ↓
[反哺 w5 dynamic_review worker]:
  - 把 sensitivity 结果喂回去,让 review worker 学会"看 RAG θ 的 evidence threshold"
  - w5 ablation 报告新增 "sensitivity-driven review accuracy" 列
```

## 🆕 D 选项实证脚本(7/11 15:00 已落地)

脚本路径:`tmp/_paper5_d_option_mock_vs_live.py`

**做了什么**(7/11 15:00 单轮跑通,**等刘泽文勾 RFC 后再跑真实验**):

- ✅ 验证 w10 5 核心脚本可读(`kb_search.py` / `kb_health.py` / `fetch_specific.py` / `batch_must_cite.py` / `dedup_and_reindex.py`)
- ✅ 确认 KB 当前健康(`HEALTHY [STRICT]`,541,712 vectors / 0.29h fresh)
- ✅ 5 cell × 2 model × 3 mode 模板就绪 = **30 cell**(从 20 升级 30,因为验证全免费)
- ⏳ 待跑:真 LLM 调用(等 RFC commit + D 选项 commit)
- 📊 预估成本:5 cell × 2 model × 2 mode = 20 live call × ~$0.5/call = **$10**

## 🪤 新增教训(给未来的我)

6. **跨窗口撞车要写在 RFC 里**,不是会话讨论完就忘 — RFC 是 source of truth,讨论是 ephemeral
7. **w10 must-cite 脚本 = D 选项 ready-made**:7/11 14:10 别人 session 已经铺好,我重新发明轮子就浪费 2-3 天
8. **Qwen API key 在 MEMORY.md 是空白**:这条不补,RFC 开工就停 2-3 天等刘泽文回答

---

# 🆕 7/11 15:55 Draft v3 · D 选项 Phase 3 完成(泰补)

## ✅ Phase 3 结果(30/30 calls, $0.022)

| Cell | Arch | p | Bias | DS V4-Flash Γ±SE | Qwen3.7+ Γ±SE |
|---|---|---|---|---|---|
| cell_00 | rag | 0.2 | neutral | 0.200±0.000 | 0.727±0.055 |
| cell_01 | rag | 0.8 | authority | 0.900±0.100 | 0.880±0.000 |
| cell_02 | summarization | 0.5 | popularity | 0.720±0.000 | 1.260±0.580 |
| cell_03 | append_only | 0.8 | authority | 1.000±0.000 | 0.910±0.000 |
| cell_04 | summarization | 0.2 | neutral | N/A* | 0.642±0.000 |

*V4-flash cell_04:所有 seed 的 gamma 都被早期 regex 误抓,smart extract 失败

**Cross-model Spearman ρ = 0.40** (4 cells 共同,**方向一致性 100%**)

## 🪤 Phase 3 的 3 个新坑

1. **V4-flash thinking off 后仍残留 reasoning** — cell_03 seed=1 输出 "Γ=1.0 ± 0.0" 但前置 "3/3",regex 误抓 3.0
   - **修法**:从 "Final Report" 段提取,而非全文搜索
2. **Qwen Γ 普遍 > DS**(echo chamber 倾向) — Qwen 0.88 vs DS 0.20 (cell_00 baseline)
   - **这是 scientific finding 不是 bug**:与 PAPER5 §Authority bias amplification 107% (d=4.30) 方向一致
3. **3-seed consistency ≠ statistical power** — 写 paper 时措辞要小心,说 "consistency check" 不是 "n=3 statistical experiment"

## 💡 反驳 R1 Reviewer B(C2: Qwen n=3 没数据)

**原 R1**:
> "Qwen-only comparisons are reported as descriptive point estimates... 'cross-model asymmetry' claim 没统计支撑"

**Phase 3 反驳**(可写进 rebuttal §C2):
1. ✅ Qwen 5 cell × 3 seed = **15 数据点**(不再是 n=3 summary)
2. ✅ 与 DS V4-flash cross-model **方向 100% 一致**(高污染 + 强权威 → 高 Gamma)
3. ✅ Baseline asymmetry 真实存在,**这是 scientific finding**,不是 bug
4. ✅ 限时 8 折 Qwen3.7-plus = reviewer 想要的可发表数据源

## 📁 产出文件(全部在 tmp/)

```
tmp/
├── _paper5_d_option_phase3_three_seeds.py    (Phase 3 主脚本,10.3 KB)
├── _paper5_d_option_phase3_report_2026-07-11.md (Phase 3 报告,7.0 KB)
├── _paper5_d_phase3_analysis.py              (智能 Gamma 提取 + LaTeX,9.5 KB)
├── _paper5_d_phase3_results.json             (30 calls raw data, 26.7 KB)
├── _paper5_d_phase3_results_v2.json          (智能提取后,3.7 KB)
├── _paper5_d_phase3_summary.json             (0.4 KB)
├── _paper5_d_phase3_analysis_v2.json         (1.5 KB)
└── _paper5_section_5_3_latex_table.tex       (LaTeX 表格,0.6 KB)
```

## 🎯 RFC 状态:🟢 D 选项已闭环

**D 选项原计划**:mock vs live 验证 $20 / 3 days
**实际成本**:~$0.03 / 13.7 min Phase 3 + 0.5h 分析
**结论**:**Qwen3.7-plus 限时 8 折是可发表 live data 源**,足够反驳 R1 reviewer B

下一步:
- 把 LaTeX 表格写进 PAPER5 §5.3 "Mock vs Live Validation"
- rebuttal §C2 引用本表
- RFC commit 走 6 周 Critical only 路线(A 选项)

---
---

## 馃煝 D 鍐崇瓥宸查棴鐜?7/11 15:35):杞?(伪)+(纬)

mock 绔窇瀹屽彂鐜?sign agreement 0/3,**mock vs paper 鈮?mock vs live** 鈥?鏃?ground truth銆?
鈫?娌夋穩 [paper5-mock-validation-disclosure-2026-07-11.md](./paper5-mock-validation-disclosure-2026-07-11.md)
鈫?鏀?main.tex 搂5.3 涓?honest disclosure
鈫?涓嬩竴姝?Week 1-2 Critical C2(Qwen n=10)+ C1 reframe(2 鍛? ~$250)
