# PAPER5 Round-1 Review Log — 2026-07-11

> **目的**:把 3 个 reviewer 真实报告 + meta-review 凝练成"修正 source of truth",后续 6-12 周的 paper 改进 / rebuttal 都引用本文件。
>
> **来源**:`F:\Research\PAPER5_CONSOLIDATED\reviews\main.multi\*.review.md`(7/11 10:33-10:34 跑通)+ `meta-review.md`(7/11 10:35)
>
> **审计模式**:paper-review-toolkit `full` + `meta`(LLM × 4, ~$0.15)

---

## 📊 评分快照

| 维度 | 权重 | Reviewer A(Novelty) | Reviewer B(Theory) | Reviewer C(Experiment) | **平均** | meta 采纳 |
|---|---|---|---|---|---|---|
| Correctness | 25% | 6 | 6 | 5 | **5.67** | 5.67 |
| Novelty | 20% | 5 | 7 | 7 | **6.33** | 6 |
| Reproducibility | 15% | 7 | 5 | 7 | **6.33** | 6 |
| Clarity | 15% | 7 | 6 | 7 | **6.67** | 6.67 |
| Statistical Rigor | 10% | 5 | 6 | 4 | **5.00** | 5 |
| Prior Work | 10% | 5 | 7 | 8 | **6.67** | 6 |
| Writing Quality | 5% | 7 | 7 | 8 | **7.33** | 7.33 |
| **加权总分** | | **5.95** | **6.20** | **6.35** | **6.17** | **6.17** |
| Recommendation | | Major | Major | Major | **Major revisions** | Major |

**当前定位**:TMLR 中段(accept 率后 50-30%)。修 4 Critical 可升 7.0+,修全 Major 可升 7.5+。

---

## 🔥 4 个 Critical 问题(reviewer 必杀)

### C1. Headline crossover claim 在 paper 自己的 Bonferroni 下不显著(2/3 reviewer)

**提**:Reviewer A(§Weakness 1)+ Reviewer C(§Weakness 1)

**核心数据**:
- DeepSeek Summarization vs Append-Only at p=0.8:**p_adj=0.135**(family-level Bonferroni, k=9, α'=0.00556)→ **n.s.**
- DeepSeek RAG advantage at p=0.2:**d=0.40, n.s.**
- 论文承认 non-significant 但**仍当 finding 讲**(§3.2 / §4.1-4.3)

**reviewer 建议**:
- (a) Reframe 为 "suggestive trend, requires replication"
- (b) 跑 n=14 复现(论文§6.2 自己提的)
- (c) 加 power analysis 显式说明当前 power 不足

**投入**:**~2 周**(+ 跑 n=14 数据,$100)

---

### C2. Qwen 实验 n=3 seeds, 无 significance test(**3/3 reviewer 三票**)

**提**:Reviewer A(§Weakness 2)+ Reviewer B(§Weakness 5)+ Reviewer C(§Weakness 2)

**核心数据**:
- Qwen 主表(Table 2/3):n=3 seeds,**no sig tests reported**
- paper 自己说:"Qwen-only comparisons are reported as descriptive point estimates"
- 这意味着 **"cross-model asymmetry" 整个 claim 没统计支撑**
- authority bias 107% amplification:**d=4.30, p_adj<0.001**,但 n=3 → 置信区间极宽

**reviewer 建议**:
- 跑 Qwen n=10(匹配 DeepSeek)
- 或明确说 Qwen 是 preliminary,不该做 practical recommendations

**投入**:**~2 周**(+ $200 API budget,40 cell × 10 seeds × DeepSeek/Qwen)

---

### C3. §6.3 "Theoretical Analysis" 没公式、没证明(1/3 reviewer, 但 B 是 sticky)

**提**:Reviewer B(§Weakness 1)

**核心问题**:
- 段落标题叫 "Theoretical Analysis of the Crossover Mechanism"
- 内容**全是定性叙述**,0 equations, 0 proofs, 0 derivations
- 仅给两个直觉("relevance filtering" + "redundancy compression")

**reviewer 建议**:
- (a) 删除 "Theoretical" 标签,改名 "Qualitative Mechanism"
- (b) 加 Theorem 1 + 数学形式化:Γ(p, architecture, model) 的 bound

**投入**:**~1 周**(选 a 改标签 + 段落重写)

---

### C4. Γ decomposition(content / retrieval)算法未定义(2/3 reviewer)

**提**:Reviewer B(§Weakness 2)+ Reviewer C(§Weakness 5)

**核心问题**:
- Table 7/5 报 content/retrieval 两 component
- paper **没说怎么分**:无 formula, 无 algorithm, 无 citation
- 进一步:无 error bars, 无 significance test, 无 SD

**reviewer 建议**:
- 提供**伪代码 + closed-form**(如适用)
- 加 bootstrap CI for 每个 component

**投入**:**~3-5 天**(伪代码 + 重跑 bootstrap)

---

## 🟡 6 个 Major 问题(影响上游,**强烈建议修**)

| # | 问题 | Reviewer | 投入 |
|---|---|---|---|
| **M1** | **缺最强 baseline: no-memory condition**(agents 无 memory) | A + C | 1 周(2×3×3×10 cell,~180 cell) |
| **M2** | **缺 hyperparameter sensitivity**(RAG θ / SUM freq / TF-IDF vs dense) | A + B + C(三票) | 2 周(3 ablation table,~270 cell) |
| **M3** | **缺 DeepSeek × authority bias cell**(论文承认漏) | A + C | 3 天($50,~30 cell) |
| **M4** | **缺 statistical protocol section**(`\ref{sec:stat-protocol}` 引用但 section 缺) | B | 半天(写 ~30 行 + bootstrap method) |
| **M5** | **significance hierarchy 混乱**(3 family k + within-table k) | B + C | 半天(commit 一套 + 显式说明) |
| **M6** | **缺 direct comparison with Bertalanić et al. 2026 prior work** | A | 3-5 天(找 paper + reproduce baseline) |
| **M7** | **缺 computational cost analysis**(tokens / latency / memory) | B | 2-3 天(测 3 arch × 3 contamination) |
| **M8** | **缺 "saturation effect" 解释**(Γ 随 p 单调下降) | B + C | 3-5 天(理论 + experiment) |
| **M9** | **缺 Gamma decomposition 误差棒** | C | 3-5 天(随 C4 一起) |

---

## 🟢 3 个 Minor / 措辞问题(可选)

- "first systematic comparison" → "first controlled comparison of three architectures for bias resistance under explicit contamination"(M)
- alternative explanations 信息丢失/方差缩减实验没真跑(M)
- RAG θ / SUM freq / 检索数 / embedding 方法缺 ablation(M → M2 已覆盖)

---

## ✅ reviewer 共识优势(修了就别改)

| 优势 | 来源 | 保留建议 |
|---|---|---|
| 透明统计报告(multi-k Bonferroni + CI + d) | A + C | 保留 |
| Falsification criteria 显式 | B | 保留 + 强化 |
| Practical guidelines(Table 4/8) | A + B | 保留,可能扩 |
| Γ decomposition analysis idea | C | **保留,但补算法** |
| Honest limitations section | A + B + C | 保留 + 更新 |
| 多 model × 多 bias × 多 contamination 设计 | C | 保留 + 扩 |

---

## 🎯 Meta-review "Required for resubmission"(8 步)

按 meta-review `F:\Research\PAPER5_CONSOLIDATED\reviews\main.multi\meta-review.md` "Required revisions for resubmission":

1. **Reframe crossover** 为 suggestive trend(satisfies C1)
2. **Qwen n=10**(satisfies C2)
3. **Add "no memory" baseline**(satisfies M1)
4. **Define Γ decomposition + add error bars**(satisfies C4 + M9)
5. **Run DeepSeek × authority OR downgrade "two bias types" claim**(satisfies M3)
6. **Add hyperparameter sensitivity at minimum for RAG θ**(satisfies M2 partial)
7. **Remove "Theoretical Analysis" label OR provide math**(satisfies C3)
8. **Include missing statistical protocol section**(satisfies M4 + M5)

**8 步全做 = Major revisions → Minor revisions**(estimated TMLR round-2 accept probability ~70%)

---

## 📊 Reviewer expertise / confidence

| Reviewer | Background | Confidence |
|---|---|---|
| A · Novelty Critic | Multi-agent systems + LLM evaluation, 8+ yr | High |
| B · Theory Stickler | Theoretical ML + stat testing + multi-agent, 8 yr | High |
| C · Experimentalist | Multi-agent LLM + experimental methodology + NLP stat, 8 yr | High |

**注**:这些是 `paper-review-toolkit` 模拟 persona,**不是真人 reviewer**。但 prompt 是基于真 TMLR reviewer 经验的"hostile critic"模板,**信噪比高**。

---

## 📂 完整 reviewer 文件清单(全 F 盘)

```
F:\Research\PAPER5_CONSOLIDATED\reviews\
├── main.review.llm.md            (standard 模式跑,5 段 prompt,7/11 跑)
├── main.multi\
│   ├── meta-review.md            ← 最重要:汇总 + 8 步 resubmit
│   ├── meta-review.meta.md       ← self_review.py pre-audit
│   ├── reviewer-A_novelty_critic.review.md
│   ├── reviewer-A_novelty_critic.prompt.md
│   ├── reviewer-B_theory_stickler.review.md
│   ├── reviewer-B_theory_stickler.prompt.md
│   ├── reviewer-C_experimentalist.review.md
│   └── reviewer-C_experimentalist.prompt.md
```

---

## 🪤 本次操作教训(给未来的我)

1. **verify_p5.py (硬规则) ≠ reviewer 真意见(软判断)**:前者抓格式,后者抓实质。前一轮我专注 verify,差点忘了 reviewer 真意见就在 `reviews/main.multi/*.review.md`
2. **full review 成本 $0.15 vs paper 改版成本 6-12 周**:`full` review 是最便宜的"决策前置"动作,**投前必跑**
3. **meta-review 是金**:单 reviewer 信息噪声大,**3 reviewer + meta = 共识 = 修订方向**
4. **3 reviewer 三票共识 = 必杀**(C2 n=3 seeds):不修必 reject
5. **本会话起点已经晚了**:7/11 10:33 review 已跑完,但 13:50 audit + 我刚才 14:05 都只看 verify,**差点错过 reviewer 真意见**

---

## 🟢 下一步(给未来的我)

按 meta-review 8 步 → **RFC: 6 周作战**(详见 `paper5-improvement-rfc-2026-07-11.md`,下个文件)

_最后更新:2026-07-11 14:55 · 凝练自 3 reviewer + meta review_