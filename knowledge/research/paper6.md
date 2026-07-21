# PAPER6 — Entity

_2026-07-11 创建。从 research-changelog-2026-07-11.md 自动抽取。_
_7/11 17:42 重大更新:**paper 性质从 stub 转型为完整 Empirical Benchmark Study**,W3 完工,verify 11/12 PASS。_

---

## 📖 内容概述(🟡 自动抽 2026-07-11 18:50,w9 v6 补丁)

> ⚠️ **草稿说明**:从 `F:\Research\PAPER6_CONSOLIDATED\main.tex` 自动抽取,精度 ~75%。
> W3 完工后 paper 性质转型 —— **从原 A4 "Capture-Resilient Voting 主张主推" → "诚实 Empirical Benchmark / Negative Result"**。
> 全文 LaTeX 命令已清洗为可读形式,关键数值保留。

### Abstract(草稿)

> **论文标题**:An Empirical Study of Aggregation Methods Under Verifier Capture in Multi-LLM Ensembles: When Does Majority Voting Fail, and Can We Beat It?

多 LLM 验证器集成正越来越多地聚合多个 LLM verifier 的判断,以降低相对单模型的方差和对抗脆弱性。这类集成中一个日益受到关注的问题是 **verifier capture**:一小撮 verifier 的输出被系统性偏差,**能在保持各自表面合理性的同时翻转聚合决策**。本文**作为经验研究**,系统地 benchmark 了 **7 种聚合方法** —— 朴素 majority / PBFT 风格确定性阈值 / uniform-weighted mean / 3 种 trust-score 变体(EMA-weighted mean / EMA-weighted median / Kalman-filter trust tracking)/ 1 种基于 trust-score 浓度切换 weighted mean 和 weighted median 的自适应 hybrid —— 跨 4 个 honest-verifier 准确率和攻击强度变化的 scenario + 3 个攻击模型(prompt injection / rubric injection / majority-bias mimicry)。

**Headline finding 是 negative**:**所有 4 个 scenario 下,我们测试的聚合方法没有一种显著优于朴素 majority voting**,且几种 trust-score 变体**在强 capture 下表现反而比 majority 差**。我们把这归因于该问题的一个**结构性属性**:在我们的设置下,**被 capture 的 verifier 在统计上无法与"假设性的少数 honest-but-wrong verifier"区分**,所以任何用统计偏差来识别 capture 的规则都会**让 false-positive 成本超过 true-positive 收益**。

我们 release 所有代码、合成生成器、以及一个 Beyond-PDF 交互式攻击 demo,让未来工作可以用真实 LLM trace 和额外聚合规则扩展本 benchmark。

### 主论点(三句话)

1. **诚实 Negative Result**:在 4 个 scenario + 3 个 attack × 7 个 aggregation 完整 benchmark 下,**没有任何方法稳定赢 majority**(包括我们自设计的 ATV);
2. **结构性解释**:capture 在统计上 ≡ honest-but-wrong verifier,**用 deviation 检测 capture 的方法同时会排除真 honest 少数错**,净效果 = 0;
3. **诚实记录**:W2 demo 暴露 CRV v1 跟 trust_only 几乎一样;CRV v2 在 f=2/N=7 下反而差 majority 9 个百分点;Appendix Table 2 数字凭印象造 → per_attack.py 实跑数据替换。

### 关键词

- Verifier Capture(验证器俘获)
- Multi-LLM Ensemble(多 LLM 集成)
- Aggregation Methods(聚合方法):majority / PBFT threshold / weighted mean / weighted median / Kalman trust / adaptive hybrid
- Negative Result(负面结果)
- Empirical Benchmark Study(实证基准研究)
- Trust Score / Trust Tracking(信任分数 / 跟踪)
- Attack Models: prompt injection / rubric injection / majority-bias mimicry
- Honest-but-Wrong Verifier(诚实但错误的 verifier)
- Deviation-Based Detection(基于偏差的检测)
- Beyond-PDF Interactive Demo(Beyond-PDF 交互式 demo)
- TMLR Acceptance Criteria(TMLR 接受准则 — technical correctness over subjective significance)

### 章节大纲(主结构)

```
§1 Introduction(verifier capture 问题 + 本文诚实 benchmark 定位)
§2 Background / Framework(7 种聚合方法 + 3 个攻击模型)
§3 Method / Verification Setup(verify_p6.py + 12 check 框架)
§4 Empirical Results(7 methods × 4 scenarios × 5 seeds)
§5 Discussion / Negative Result Interpretation(结构性解释)
§6 Related Work(Byzantine fault tolerance + LLM-as-judge)
§7 Broader Impact(verifier capture 安全启示)✅ W3 完成
§8 Ethics(双用风险 + 披露)✅ W3 完成
§9 Conclusion
Appendix A.1-A.4(per_attack.py 详细 + extended_methods.py)✅ W3 完成
```

### 🎯 核心位置(在主研究主线中)

- **继承**:PAPER5 的多 Agent 校准/偏差传播框架;复用 40 个 L/A scenarios
- **转型时间线**(关键!):W1 主推 CRV → W2 红队发现 CRV v1 跟 trust_only 几乎一样 → **X+Z+P1 转型**(撤 CRV 主方法 + 改写为诚实 benchmark)
- **TMLR 适配**:acceptance criteria 原文"technical correctness over subjective significance" → **negative result + 结构性解释正中 TMLR 偏好**

### ⚠️ 关键统计警示

- 真实数字(per_attack.py 实跑):majority 跟 trust_median 全列并列 mean 0.686,**其他全部 ≤ 0.673**
- 7 methods × 4 scenarios × 5 seeds = 140 cells(部分用合成数据,W4+ 待真 LLM pilot)
- C9 figure captions 留 W5(verify stub 1/12)
- audit 报告(7/11):✅ verify PASS=11 / FAIL=0 / STUB=1 — **W3 完工标准**

---

## ✅ 当前状态(7/11 17:42 更新)

| 字段 | 值 |
|---|---|
| **状态** | 🟢 **W3 完工,可投**(11/12 verify PASS) |
| **路径** | `F:\Research\PAPER6_CONSOLIDATED` |
| **main.tex** | **46898 bytes**,11 章节完整成文 |
| **verify_p6.py** | **14777 bytes**,12 check 框架(11 实装,1 stub C9 figure)|
| **paper 性质** | **Empirical Study / Negative Result**(从原 A4 主推 CRV 转型)|
| **Venue** | TMLR(中位数打法对齐)+ 备选 NeurIPS J2C 申请 |
| **边界** | 刘泽文锁定 **W3 only**,W4-W8 不在泰的当前范围 |

### 与 genesis-master 关系澄清(仍有效)

> 刘泽文 **第 6 篇独立投稿 TMLR 是 [`genesis-master/`](../entities/genesis-master.md)**,已 v1.0 投稿(2026-07-09)。
> 本 `PAPER6_CONSOLIDATED/` 是 **7/9 新起的独立 stub**,与 genesis-master 平行但不同目录。
> 详见 [刘泽文 — 研究系统全图](../entities/liu-zewen-research.md)。

---

## 📜 转型时间线(7/11)

| 时段 | 阶段 | 关键产出 |
|---|---|---|
| 13:22 | w9-fill-todo | 发现 5 篇 CONSOLIDATED 都围绕"多 Agent 通信/校准/偏好耦合",stub 标记 |
| 13:55 | STATUS v2 红队 | 掀掉"5 月 deadline 必含 6 篇"过时假设;3 候选:从零/重构/放弃 |
| 14:02 | 选 A(从零写新主题) | 3 候选:A4 verifier capture / B1 PDP-CAL / B3 DWPG |
| 14:15 | TMLR 中位数打法 + Q1-Q4 默认 | N=7,f=2;3 attacks;5 baselines;3 datasets;venue TMLR+J2C |
| 14:20 | W1 上半场 6 文件 | main.tex 骨架 + tmlr.sty + math_commands.tex + refs.bib seed + protocol.md + verify_p6.py |
| 14:25 | W1.5 ABC(刘泽文批)| verify C1-C3 实装抓出 documentclass 真 bug;3 篇真实 arxiv cite(Blind Curator 2607.07436 等);漏洞 #11 字面命中 |
| 15:00 | W1 下半场 | Threat model 形式化(Def 1.1-1.4 + Thm 1)+ CRV 算法(Def 2.1-2.2 + Alg 1 + Thm 2)+ Background 4 段 |
| 15:30 | W2:算法 + 3 attacks | crv.py / attacks.py / demo.py..demo4.py |
| 15:50 | 🔴 **X+Z+P1 转型** | **撤 CRV 主方法 → 写诚实 benchmark study** |
| 16:00 | v6:7 methods benchmark | extended_methods.py + benchmark.py;**negative result:所有方法 ≤ majority**;标题 / Abstract / Intro / §4 / §5 / §6 / §9 全改 |
| 17:00 | 刘泽文: "你只负责 W3" | 边界锁定 |
| 17:42 | **W3 完工** | §7 Broader Impact + §8 Ethics + Appendix A.1-A.4 + verify C8/C10-C12 + per_attack.py 修真 | 

---

## 🎯 论文性质已标记

### Title

> **"An Empirical Study of Aggregation Methods Under Verifier Capture in Multi-LLM Ensembles: When Does Majority Voting Fail, and Can We Beat It?"**

### Headline finding(§6)

**No aggregation method we tested substantially outperforms plain majority voting.** In all 4 scenarios × 5 seeds:

| Method | S1 | S2 | S3 | S4 | mean |
|---|---|---|---|---|---|
| majority | **0.889** | **0.553** | **0.459** | 0.843 | **0.686** |
| trust_median | **0.889** | **0.553** | **0.459** | 0.844 | **0.686** |
| trust_mean | 0.883 | 0.521 | 0.432 | **0.851** | 0.672 |
| kalman_trust | 0.882 | 0.535 | 0.446 | 0.842 | 0.677 |
| ATV(我设计)| 0.883 | 0.527 | 0.438 | 0.846 | 0.673 |
| bft_pbft | 0.777 | 0.522 | 0.458 | 0.720 | 0.619 |
| weighted_uniform | 0.804 | 0.484 | 0.365 | 0.729 | 0.595 |

### Structural explanation

**Capture is statistically indistinguishable from honest-but-wrong verifier**. Any rule using statistical deviation to identify capture cannot outperform a rule that ignores the distinction.

### TMLR 适配

Acceptance criteria 原文:"technical correctness over subjective significance" + "We explicitly avoid these terms (significant, impactful, novel)" → **negative result + 结构性解释** 正是 TMLR 偏好。

---

## 📂 全部产物(16 文件,~95 KB)

| 路径 | 字节 | 用途 |
|---|---|---|
| `F:\Research\PAPER6_CONSOLIDATED\main.tex` | 46898 | 11 章节完整 paper |
| `F:\Research\PAPER6_CONSOLIDATED\verify_p6.py` | 14777 | 12 check 框架(11 实装,1 stub C9)|
| `F:\Research\PAPER6_CONSOLIDATED\extended_methods.py` | 7768 | 7 aggregation methods |
| `F:\Research\PAPER6_CONSOLIDATED\crv.py` | 6637 | legacy CRV(archival)|
| `F:\Research\PAPER6_CONSOLIDATED\attacks.py` | 5782 | 3 attack families |
| `F:\Research\PAPER6_CONSOLIDATED\demo.py` | 4068 | prototype demo 1 |
| `F:\Research\PAPER6_CONSOLIDATED\demo2.py` | 1984 | strong attack demo |
| `F:\Research\PAPER6_CONSOLIDATED\demo3.py` | 3245 | capture-vs-honest split |
| `F:\Research\PAPER6_CONSOLIDATED\demo4.py` | 2724 | BFT boundary |
| `F:\Research\PAPER6_CONSOLIDATED\benchmark.py` | 3675 | 4 scenarios × 7 methods × 5 seeds |
| `F:\Research\PAPER6_CONSOLIDATED\per_attack.py` | 1080 | Appendix Table 2 数据源 |
| `F:\Research\PAPER6_CONSOLIDATED\protocol.md` | 3330 | 实验协议 |
| `F:\Research\PAPER6_CONSOLIDATED\refs.bib` | 5864 | 13 条真实 cite(7 经典 BFT + 5 LLM-judge + 1 self)|
| `F:\Research\PAPER6_CONSOLIDATED\tmlr.sty` | 6560 | TMLR 模板 |
| `F:\Research\PAPER6_CONSOLIDATED\math_commands.tex` | 5039 | 数学命令 |
| `F:\Research\PAPER6_CONSOLIDATED\main.tex.LLM_FABRICATED_DO_NOT_SUBMIT` | 11372 | 废稿,**未动**(等"清") |
| `F:\Research\PAPER6_CONSOLIDATED\review_report_v1.md` | 8658 | 废稿 review,**未动** |

---

## 📊 verify 现状(7/11 17:42,W3 完工)

**PASS=11 / FAIL=0 / STUB=1,exit 0**
- C1-C8 + C10-C12 ✅
- C9 figure captions ⚪(W5 才做)

---

## 🚦 边界外(明确不动)

- ❌ W4-W8 figure / 投稿 / J2C / rebuttal(超 W3 范围)
- ❌ 兄弟窗口(w1/w2/w4/w5/w6/w7/w8/w9/w10/w11)
- ❌ 废稿 / review_report(等你说"清"才归档)

---

## 🆕 7/11 17:42 真实状态 vs 旧 entity 对比

| 字段 | 旧 entity(7/11 13:55)| **新 entity(7/11 17:42)** |
|---|---|---|
| 状态 | 🔴 stub-only | **🟢 W3 完工** |
| main.tex | 只有废稿 | **46898 bytes 完整 paper** |
| 选题决策 | 待决策 | **A4 verifier capture(已锁定)** |
| paper 性质 | 未定 | **Empirical Study / Negative Result** |
| 实验 | 0 | **7 methods × 4 scenarios × 5 seeds + 3 attacks** |
| verify | 0 | **11/12 PASS** |

---

_最后更新:2026-07-11 17:42(从 14:30 w9 跳过段 → 17:42 完整完工段)_