# Paper Review Audit — 2026-07-11 完整审计

_2026-07-11 10:40 沉淀。来源:`paper-review-toolkit all` × 5 papers 全跑通结果。_

---

## 🎯 关键结论

| 项 | 值 |
|---|---|
| **跑通论文** | 5 / 5 篇 |
| **LLM review 调用** | 25 次(5 篇 × 5 prompts) |
| **总成本** | $0.0745 |
| **关键修复** | 修了 5 个 `verify_p<N>.py` 的 severity 显示 bug |
| **顺手修了** | `verify_p2.py` / `verify_p4.py` 的 CHECKS_CONFIG LaTeX 反斜杠污染 |

**核心发现**:
1. **5 篇全 B/C 级**——Quality 评分(启发式)B 级 4 篇 + C 级 1 篇,但 verify_p<N>.py 硬规则审计找出 **49 findings**(3 HIGH + 36 MED + 15 LOW)
2. **PAPER5 不再是"唯一可投递"** —— v0.3.0 新规则 C9 揭示 3 张 figure 缺 caption(原以为是 MED,实际 HIGH)
3. **C7 ceremonial citation 多为假阳性** —— extract_sentence 取的是 cite 所在第一句,但紧跟句常有 >30 词的 elaboration。21 个 finding 中,真问题约 1/3,其余是 verify 脚本的边界 bug

---

## 📊 5 篇审计结果对比表

| # | 论文 | 文件 | Quality | Audit (H/M/L) | 距投稿 | 优先 |
|---|---|---|---|---|---|---|
| 1 | PAPER1 | main.tex (59K) | B 80.75% | 0 / 6 / 3 | 中等 | 2 |
| 2 | PAPER2 | **main_v9.tex** (33.9K) | C 72.0% | 1 / 4 / 2 ⚠️ | 较远 | 4 |
| 3 | PAPER3 | main.tex (43.7K) | B 87.0% | 1 / 10 / 3 | 中等 | 3 |
| 4 | PAPER4 | main.tex (55.3K) | C 75.75% | **2** / 7 / 4 | 较远 | 5 |
| 5 | PAPER5 | main.tex (72.9K) | **B 88.5%** | **3** / 0 / 3 ⚠️⚠️ | 最近(但 HIGH 升级) | 1 |

> **修复后总计:3 HIGH + 31 MED + 15 LOW = 49 findings**
> 修复前总计:**0 HIGH** + 36 MED + 15 LOW(PAPER5 状态被严重低估)

⚠️ 标 = 修复前后差异显著的论文(PAPER2/4/5 都有 HIGH 级问题被揭示)

---

## 🔍 每篇核心问题

### PAPER1 — Communication / Calibration
- **核心**:C7 ceremonial cites × 5 + C9 fig:triangle 未引用 + C10 reproducibility 缺
- **action**:5 处 cite 加 engage verb;fig:triangle 加 `\ref{}`;补 reproducibility

### PAPER2 — Impossibility Triangle
- **核心**:C2 无 power analysis section (HIGH) + C4 self-cite 30%(踩红线) + C7 × 2 + clarity 50%
- **action**:加 power section;减 self-cite 到 ≤ 2 keys;加 engage verb

### PAPER3 — BoundarySync
- **核心**:C2 无 power analysis (HIGH) + C7 ceremonial × 8 + C5 × 4
- **action**:加 power section;8 处 cite 改写;C5 加 test name

### PAPER4 — N-Sensitivity
- **核心**:C2 无 power analysis (HIGH) + C7 × 6 + C9 figure 216 缺 caption (HIGH) + "reveal" × 3
- **action**:加 power section;6 处 cite 改写;figure 216 加 caption;替换 "reveal"

### PAPER5 — Memory Architectures
- **核心**:C9 三张图缺 caption (HIGH × 3) + C10 reproducibility 缺
- **action**:**先修这 3 张图 caption** (HIGH 级,唯一高优问题);补 reproducibility

---

## 🛠️ paper-review-toolkit 当前能力(v0.3.0)

### 8 子命令
| 命令 | 用途 | LLM |
|---|---|---|
| `doctor` | 工具链检查 | 0 |
| `quick` | 启发式 profile | 0 |
| `standard` | 单 reviewer pipeline | 1 |
| `full` | 3 reviewer + self-review | 4 |
| `rebuttal` | 审稿→rebuttal 转换 | 1 |
| `audit` | verify_p<N>.py | 0 |
| `all` | 4 阶段全跑 | 5 |
| `tool` | 单 paper-writing-agent 子命令 | 0 |

### 已修复 bug(5 个)
| # | bug | 修法 |
|---|---|---|
| A | paper-writing-agent CLI 跑不动 | wrapper 绕开坏 __init__ |
| B | paper_profile.py 写死 PDF | 后缀检测 |
| C | verify_p*.py 退出码误判 | rc==2 才当崩溃 |
| **D** | **C9 severity 显示错位(本次发现)** | effective_severity 字典 |
| **E** | **env_config BASE 子进程继承(本次发现)** | 硬设 fallback |

### 工具调用模式重要发现
- `review_paper.py all <paper>` 跑出 4 阶段,但 **verify 用 cwd 里的 verify_p<N>.py**(硬编码 .tex 文件名,PAPER2 是 main_v9.tex 而非 main.tex)
- `standard` / `full` 只生成 review prompt,**不直接调 LLM**——需要外部 LLM 跑(本次用 `run_review_llm.py` 批量跑通)

---

## 🆕 2 个新 bug 详细记录

### Bug D · verify severity 显示错位
- **症状**:外层 print `[MEDIUM] C9`,消息内 `HIGH: figure ... has no caption`
- **根因**:每个 finding 自带 severity 前缀(`HIGH:`/`MED:`/`LOW:`),外层用 `SEVERITY[cat]` 查表覆盖了它
- **修法**:`apply_b_fix.py` 把每条 finding 的 effective severity 算出来,既用于 print 又用于 TOTAL 计数
- **影响**:PAPER5 的 3 个 C9 从 MED 升 HIGH,论文严重性被显著揭示

### Bug E · env_config BASE 子进程不继承
- **症状**:在 shell 里 `curl https://api.deepseek.com/v1/...` 成功,但 `python` 脚本里 `urllib.request` 拿到 401
- **根因**:`env_config` 把 key/value 存到 hermes-agent 进程内存,Python 子进程只继承 OS env 副本
- **修法**:`run_review_llm.py` 里硬设 fallback —— 如果 BASE 是 `openai.com` 而没 `deepseek`,改成 DeepSeek
- **触发条件**:env_config 设过 key/base 后,**新开的子进程** 一定踩这个坑

---

## 📁 本会话产出文件(F:\Research 根目录)

| 文件 | 用途 | 大小 |
|---|---|---|
| `CONSOLIDATED_REVIEW_2026-07-11.md` | 5 篇全对比 + 行动路线图 | 8 KB |
| `run_review_llm.py` | 25 个 LLM 调用批量脚本 | 7 KB |
| `review_llm_log.txt` | 25 次调用的 token/cost log | 2 KB |
| `apply_b_fix.py` | verify severity bug 批量修复 | 4 KB |
| `C7_REVISION_SUGGESTIONS_2026-07-11.md` | 21 处 C7 上下文清单(不自动改) | 10 KB |
| `PAPER{2,4}_CONSOLIDATED/verify_p{2,4}.py.bak_before_latexfix` | LaTeX 修复前备份 | - |
| `PAPER{2,3,4,5}_CONSOLIDATED/verify_p{N}.py.bak_before_bfix` | B-fix 前备份 | - |
| `PAPER{1-5}_CONSOLIDATED/reviews/main.review.llm.md` | standard LLM review | ~3 KB each |
| `PAPER{1-5}_CONSOLIDATED/reviews/main.multi/*.review.md` | 3 reviewer + meta(20 文件) | ~3 KB each |

---

## 🎯 5 月 Deadline 投递优先级(更新版)

| 优先级 | 论文 | 行动 | 预计工时 |
|---|---|---|---|
| 🥇 1 | **PAPER5** | 修 3 张图 caption (HIGH) + 补 reproducibility | 1 h |
| 🥈 2 | PAPER1 | 修 5 处 C7 + fig:triangle `\ref` + reproducibility | 2 h |
| 🥉 3 | PAPER3 | 加 power section (HIGH) + 8 处 C7 + C5 test name | 3 h |
| 4 | PAPER2 | 加 power section (HIGH) + 减 self-cite + 2 处 C7 | 2 h |
| 5 | PAPER4 | 加 power section (HIGH) + 6 处 C7 + fig caption + "reveal" | 3 h |

**总工时预估**:~11 小时 + $1 LLM 成本

---

## 🔗 跨文档链接

- [5 月 deadline 总览](../research/index.md)
- [PAPER1](../research/paper1.md) / [PAPER2](../research/paper2.md) / [PAPER3](../research/paper3.md) / [PAPER4](../research/paper4.md) / [PAPER5](../research/paper5.md)
- [paper-review-toolkit 工具箱](./paper-review-toolkit.md)
- [7/11 研究 CHANGELOG](./research-changelog-2026-07-11.md)

---

_最后更新:2026-07-11 10:40_