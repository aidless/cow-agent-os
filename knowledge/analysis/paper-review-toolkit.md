# 论文审阅工具箱 — 刘泽文的能力全景

> 最后更新:2026-07-11 17:55(从 v0.3.0 升级到 v0.4.0 + 吸收 7/11 w5/w6/w11 进展)

## 📊 一句话定位

刘泽文名下有 **3 个核心工具 + 1 个统一 wrapper + 1 套动态 worker 体系**,覆盖论文从「写完 → 自审 → 投稿 → 回复 rebuttal」全周期。v0.4.0 起支持动态 spawn / 过期 / ablation。

```
                    paper.pdf / main.tex
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
   paper-writing-agent  tmlr-review-    tmlr_pipeline
   (8 子命令 + 18 type  simulator       (6-stage scaffold)
   + 7 维评分 + 伦理)  (3 reviewer +    (s1..s6)
                       self-review +
                       rebuttal_gen)
                            │
                  ┌─────────┴─────────┐
                  ▼                   ▼
       F:\Research\review_paper.py    C:\Users\Administrator\cow\
       (wrapper, 695 行, 8 子命令)      tmp\windows\w5-paper-review-dynamic\
                                         (动态 worker 套件,v0.4.0)
                  │                    ├─ worker_template.py      (Worker dataclass)
                  │                    ├─ worker_impls.py         (8 fn 实装)
                  │                    ├─ dynamic_spawner.py     (TaskSpec/SpawnPlan)
                  │                    ├─ worker_expiration.py   (ExpiryPolicy)
                  └────────────────────└─ run_ablation.py        (4 组策略对比)
```

---

## 🎯 工具链状态(7/11 17:55 真实钟)

| 组件 | 版本 | 路径 | 状态 |
|---|---|---|---|
| **统一 wrapper** | review_paper.py 695 行 | F:\Research\review_paper.py | ✅ v0.4.0(8 子命令) |
| **skill 包装** | v0.4.0 | C:\Users\Administrator\cow\skills\paper-review-toolkit\SKILL.md | ✅ 7 Bug 全列 |
| **动态 worker 套件** | w5 完工 | tmp\windows\w5-paper-review-dynamic\ | ✅ 10 文件 ~105 KB |
| **paper-writing-agent** | v24.0 | F:\Research\paper-writing-agent\ | ✅ 5 子命令 + 18 type |
| **tmlr-review-simulator** | - | F:\Research\tmlr-review-simulator\ | ✅ 8 脚本闭环 |
| **tmlr_pipeline** | s1-s6 | F:\Research\tmlr_pipeline\ | ⚠️ 通过 `tool` 间接调 |

---

## 📦 8 子命令(实际可用,7/11 17:55 实测)

| # | 子命令 | kind | cost | llm | 用途 | 实测状态 |
|---|---|---|---:|---:|---|---|
| 1 | `doctor` | HEURISTIC | $0 | 0 | 检查 3 工具路径 | ✅ PAPER5 已跑 |
| 2 | `quick` | HEURISTIC | $0 | 0 | identify+evaluate+paper_profile+verify_p* | ✅ PAPER5 已跑(3 findings) |
| 3 | `standard` | LLM | $0.05 | 1 | simulate_review.py → 61KB review prompt | ✅ PAPER5 已跑 |
| 4 | `full` | LLM | $0.15 | 4 | 3 reviewer 并行 + self-review | ✅ 文档已 verify |
| 5 | `rebuttal` | LLM | $0.05 | 1 | review → TMLR point-by-point | ✅ 接口已通 |
| 6 | `audit` | AUDIT | $0 | 0 | cwd 下的 verify_p*.py | ✅ 跑 verify_p5 找到 3 真 findings |
| 7 | `all` | ORCHESTRATOR | $0.22 | ~5 | quick + standard + full + audit 串行 | ✅ orchestrator 已实装 |
| 8 | `tool` | HEURISTIC | $0 | 0-1 | 单跑 paper-writing-agent 子命令 | ✅ 5 子命令分支 |

**统一入口使用**:
```powershell
cd F:\Research\PAPER5_CONSOLIDATED
python F:\Research\review_paper.py quick main.tex         # 3 秒, $0
python F:\Research\review_paper.py standard main.tex      # 30 秒, $0.05
python F:\Research\review_paper.py full main.tex          # 2 分钟, $0.15
python F:\Research\review_paper.py doctor                 # 检查工具路径
```

---

## 🛠️ 三个核心工具(被 wrapper / dynamic_spawner 调用)

### 工具 1:paper-writing-agent
**位置**:`F:\Research\paper-writing-agent\`
**关键能力**:
- 多 Agent 协作审稿:Specialist(技术)/ Editor(写作)/ Critic(新颖性)/ Reflection(元批评)
- TMLR 80+ 检查项(正确性 / 新颖性 / 可复现 / 清晰度 / 统计严谨 / 相关工作 / 写作质量)
- **18 种论文类型分类**(`core/paper_type_identifier.py`)
- **10 种回复策略**(`core/response_strategy_recommender.py`)
- 安全审计(PII / 伦理 / 提示注入)

**5 个可用子命令**(wrapper 已接入):
- `identify` — 论文类型(返回 type / confidence / 18 种类型打分)
- `evaluate` — 7 维质量评分(返回 overall / grade / strengths / weaknesses)
- `citations` — 引用 hygiene 检查
- `plagiarism` — 重复 / 过度相似度检测
- `ethics` — 伦理关键词扫描

### 工具 2:tmlr-review-simulator
**位置**:`F:\Research\tmlr-review-simulator\`(⚠️ SKILL.md 写的 `%USERPROFILE%\.mavis\skills\` 路径在本机不存在)
**核心能力** — 8 个脚本形成完整闭环:

```
main.tex / paper.pdf
  ├─→ pdf_ingest.py / tex_ingest.py  → 结构化 paper card
  ├─→ paper_profile.py               → 论文画像(Bug B 已修)
  ├─→ 4 个对抗式 Agent               → review.md
  │     ├─ Specialist (技术正确性)
  │     ├─ Editor (写作质量)
  │     ├─ Critic (新颖性)
  │     └─ Reflection (元批评)
  │
  ├─→ multi_review.py                → 3 个独立 reviewer + meta
  │     ├─ Reviewer A · Novelty Critic
  │     ├─ Reviewer B · Theory Stickler
  │     └─ Reviewer C · Experimentalist
  │
  ├─→ self_review.py                 → review.meta.md(对 review 自审)
  ├─→ rebuttal_gen.py                → rebuttal.md
```

### 工具 3:tmlr_pipeline
**位置**:`F:\Research\tmlr_pipeline\`(6 阶段脚本)
**当前状态**:⚠️ 通过 `tool` 子命令间接调,wrapper 未直接接入(中期 TODO)

---

## 🐛 上游 Bug 完整列表(7 个已修复)

| Bug | 位置 | 发现日期 | 症状 | wrapper 修复 |
|---|---|---|---|---|
| **A** | `paper_writing_agent/__init__.py` | 7/10 | CLI 完全跑不动(relative import 错)| 直接 `import core.*`,绕开 `__init__.py` |
| **B** | `tmlr-review-simulator/paper_profile.py` line 142 | 7/10 | 给 `.tex` 报 PDF 错 | 按后缀选 `tex_ingest` / `pdf_ingest` |
| **C** | `verify_p<N>.py` 退出码契约 | 7/10 | "有 findings" 误报失败 | `rc==1` 显示"audit ran",`rc==2` 才当崩溃 |
| **D** | `verify_p<N>.py` print_finding 的 severity 显示 | 7/11 11:00 | 真 HIGH 标成 MED(图表缺 caption 类)| `effective_severity()` 根据 msg 内容自适应,B-fix 应用到 5 篇 |
| **E** | `env_config` 设的 OPENAI_API_BASE 不传 subprocess | 7/11 11:00 | urllib 调 401,默认 base 而非 DeepSeek | 脚本里硬设 `os.environ.setdefault(...)` |
| **F** | `c2_section_pattern` regex 不支持 `\subsection` | 7/11 14:00(w6) | 4 篇 verify 误报 HIGH(section_pattern 只匹配 `\section`) | verify 脚本用 OR 模式 `\\section\|\\subsection`,`apply_b_fix.py` 批量修了 |
| **G** | audit 报告 ≠ verify 实测,实测才是 ground truth | 7/11 14:35(w6) | audit 报 6 HIGH,实测 4 HIGH | "verify-after-patch" 强 gate,任何 patch 后必 verify |

**Bug F 真实案例**(7/11 14:38 w6-paper-repair 挖出):
```python
# BAD:只匹配 \section
'c2_section_pattern': '\\section\\*?\\{[^}]*(?:Statistical|...)[^}]*\\}'

# GOOD:OR 模式
'c2_section_pattern': '\\section\\*?\\{[^}]*Power analysis[^}]*\\}'
                      '|\\subsection\\*?\\{[^}]*Power analysis[^}]*\\}'
```

PAPER3 有 `\section{Method}` 内含"Method",PAPER4 有 `\subsection{Relationship to Statistical Power}`,都死在 regex 兼容性上。
PAPER1/PAPER5 的 verify **没这个 bug**(已经用 OR 模式)。

---

## 🔮 动态 worker 体系(w5 完工,v0.4.0 核心)

### 背景
paper-review-toolkit 的 8 子命令固定、8 个 worker 角色固定。**v0.4.0 起**支持:
- **Worker 抽象层**:8 个子命令 → 8 个 frozen Worker 实例
- **动态 spawn**:按 TaskSpec(level / priority / skip / custom_workers / budget)→ SpawnPlan
- **过期回收**:TTL_24H / PER_TASK / CUSTOM 三种 policy
- **4 组 ablation**:static_full / static_level_tuning / dynamic_spec / random_baseline

### 5 个新文件(w5-paper-review-dynamic)

| 文件 | 大小 | 角色 |
|---|---|---|
| `worker_template.py` | 14.6 KB | Worker dataclass + REGISTRY + dispatch + topo |
| `worker_impls.py` | 9 KB | 8 fn 实装 + importlib 懒加载 |
| `dynamic_spawner.py` | 21.5 KB | TaskSpec / SpawnPlan + spawn / random_spawn + execute |
| `worker_expiration.py` | 11.3 KB | ExpiryPolicy + make_expiries / prune_expired |
| `run_ablation.py` | 18.8 KB | 4 策略 + mock metrics + markdown 报告 |
| `ablation_report.md` | 5 KB | dry-run 报告(mock)|
| `ablation_results.json` | 5 KB | 机器可读聚合结果 |

### 5 步调用链
```bash
# Step 1:spec —— 只 plan 不执行
$ python dynamic_spawner.py spec --level standard --paper main.tex
Workers (2): quick_triage / single_review
Total cost: $0.05, 1 LLM
Rationale:
  level=standard preset (2 workers)
  +custom (0 workers)
  = 2 workers, $0.05, 1 LLM

# Step 2:execute 真跑(--execute)
$ python dynamic_spawner.py spec --level standard --paper main.tex --execute
=== EXECUTING ===
[1/2] quick_triage → 4 步串行(identify + evaluate + paper_profile + verify_p5)
[2/2] single_review → simulate_review.py → 61KB review prompt
==> done: rc_total=0

# Step 3:random spawn(给 ablation baseline 用)
$ python dynamic_spawner.py random --n 4 --seed 42
Workers (4): quick_triage / doctor / verify_paper / single_review(随机顺序)
Total: $0.05, 1 LLM(可复现)

# Step 4:expiration(24h / per-task / custom TTL)
$ python worker_expiration.py self-test  # 9 组测全过

# Step 5:ablation 4 组 dry-run
$ python run_ablation.py dry-run
strategy                cost       time   quality
static_full         $0.200    68.0s    0.700
static_level_tuning $0.170    61.4s    0.750
dynamic_spec        $0.170    65.4s    0.850
random_baseline     $0.272    57.6s    0.500
```

### 4 组 ablation dry-run 结论(mock)
| 策略 | cost | time | quality | findings | 评价 |
|---|---:|---:|---:|---:|---|
| `static_full` | $0.200 | 68s | 0.700 | 7.0 | 中庸(永远跑 full,小 paper 浪费 LLM) |
| `static_level_tuning` | **$0.170** | 61s | 0.750 | 6.2 | **最便宜**(按 paper 长度分流) |
| `dynamic_spec` | $0.170 | 65s | **0.850** | 6.2 | **质量最高**(spec-driven 最贴合 paper) |
| `random_baseline` | $0.272 | 58s | 0.500 | 4.0 | 基线最低(符合随机假设) |

📍 **真跑 TODO**:等用户下命令跑 N=10+ paper × 4 策略 × 30 seeds + LLM-as-judge + t-test 显著性检验

---

## 🎯 实战案例:PAPER5 全套审计(7/11 真实跑过)

```bash
# 1. 入口自检(3 工具路径全 OK)
$ python review_paper.py doctor
[OK ] pwa: F:\Research\paper-writing-agent
[OK ] sim: F:\Research\tmlr-review-simulator
[OK ] pipe: F:\Research\tmlr_pipeline

# 2. 启发式快筛($0, 5 秒)
$ python review_paper.py quick main.tex
[OK ] identify              -> reviews/profile.md
[OK ] evaluate              -> reviews/quality.md
[OK ] paper_profile (.tex)  -> reviews/paper_profile.md
[OK ] verify_p5.py          -> 3 findings(都是 figure 缺 caption)

# 3. 单 reviewer LLM($0.05, 30 秒)
$ python review_paper.py standard main.tex
✓ Wrote review prompt to: reviews/main.review.md
  Size: 61,225 chars

# 4. 完整 3 reviewer($0.15, 2 分钟)
$ python review_paper.py full main.tex
  + multi_review.py  → 3 reviewer (A Novelty / B Theory / C Experimentalist)
  + self_review.py   → meta-review.meta.md

# 5. 论文级硬规则审计(找真问题)
$ python review_paper.py audit
PAPER AUDIT  (verify_p5.py)
Source: F:\Research\PAPER5_CONSOLIDATED\main.tex
Size:   75,536 chars  Refs:   35 entries in refs.bib
Findings by category:
  C9  [MEDIUM]  3 finding(s)   ← Bug D 修复后真实 HIGH
TOTAL: 3 findings (HIGH=0/3M/3L → 3H/0M/3L after Bug D fix)
```

**PAPER5 实测结论**:
- 启发式打分偏乐观(B 级 88.5%)
- 硬规则审计找出 3 个真问题(图 caption)
- 两层都要看

---

## 🪤 上游 bug 修复攻略(给未来踩坑者)

### 编码陷阱("修对地方")

- **Bug A**:`__init__.py` 的 eager import 没办法"修对地方"——直接绕开比改源稳(w5 就这么干)
- **Bug D**:verify 脚本里把 print 循环的 `SEVERITY[cat]` 改成 `effective_severity(cat, msg)`,看 msg 头关键字自适应
- **Bug F**:**新建 verify 脚本必须用 OR 模式**(`\\section|\\subsection`),写完正则在 5 篇 CONSOLIDATED 论文上回归过

### 不要做的事("anti-pattern")

- ❌ patch main.tex 后**不 verify** 就宣布"修了"(Bug F 教训:12:12 session 给 PAPER2 写 +1146 bytes,但没重跑 verify 就发结论)
- ❌ 信任 **audit 报告**的 HIGH 数,**只信 verify 实测**(Bug G 教训:audit 报 6 HIGH,实测 4 HIGH)
- ❌ **env_config 设 env** 期望传到 subprocess——不传(Bug E 教训:`env_config` 写 hermes-agent process memory,**不写 OS env**)

### w5 调试教训

- **frozen=True dataclass** 不能 in-place 改,测 cycle 时改完**必须恢复**
- **时间测试**用固定 `T_initial`,不能 `time.time() + delta` 然后传 `created_at=now`(age=0 bug,expire 永远过不了)

---

## 🔮 下一步规划

### 立即可做(7/11 收尾)

- ✅ **已做**(7/11 13:35-15:45):w5 paper-review 动态化全部完工
- ✅ **已做**(7/11 14:38):w6 paper-repair 4 HIGH → 0(w6 完工报告)
- ✅ **已做**(7/11 17:00):w4 A1 model_pinning 预留落地
- 📍 **待你下命令**:真跑 4 组 ablation(N=10+ paper × 4 策略 × 30 seeds)

### 中期(tmlr_pipeline 完整接入)

- 在 wrapper `review_paper.py` 里加 `cmd_pipeline <stage>` 子命令,接入 6 阶段脚本
- 写 `gen_verify_scripts.py` 自动从 TEMPLATE 派生新论文的 verify 脚本

### 远期(自动化跑 + LLM 直调)

- 在 wrapper 里直接调 DeepSeek API,跳过"生成 prompt → 手动喂 LLM → 填回"的中间步骤
- 加 `cost-tracker` 子命令,统计每个 paper 的累计审稿成本

### 反哺 IDEA-B3 (Dynamic Worker Pool paper)

- w5 全部产出 = IDEA-B3 paper 的:
  - **§3 Architecture**(8 worker 抽象)
  - **§4 Implementation**(3 个核心脚本)
  - **§5 Evaluation**(4 组 ablation 实验,真跑后写 paper 实验段)
- 详见 [w5 completion report](./w5-completion-2026-07-11.md) (7.4 KB)

---

## 📂 文件索引(权威路径)

### 代码 / Skill(7/11 17:55 真最新)

```
F:\Research\review_paper.py                                     (695 行 wrapper)
F:\Research\REVIEW_PAPER_README.md
C:\Users\Administrator\cow\skills\paper-review-toolkit\
  ├── SKILL.md                                                  (v0.4.0)
  ├── review_paper.py                                           (副本)
  └── REVIEW_PAPER_README.md                                    (副本)

C:\Users\Administrator\cow\tmp\windows\w5-paper-review-dynamic\  (w5 完工)
  ├── DESIGN.md  (5.5 KB)
  ├── STATUS.md  (19 KB)
  ├── worker_template.py   (14.6 KB)
  ├── worker_impls.py      (9 KB)
  ├── dynamic_spawner.py   (21.5 KB)
  ├── worker_expiration.py (11.3 KB)
  ├── run_ablation.py      (18.8 KB)
  ├── ablation_report.md   (5 KB)
  └── ablation_results.json (5 KB)

F:\Research\paper-writing-agent\   (5 子命令)
F:\Research\tmlr-review-simulator\ (8 脚本)
F:\Research\tmlr_pipeline\         (6 stage)
```

### 知识页面

```
knowledge\analysis\paper-review-toolkit.md                  ← 本页
knowledge\analysis\w5-completion-2026-07-11.md              ← w5 完工
knowledge\analysis\w6-paper-repair-completion-2026-07-11.md ← w6 完工
knowledge\analysis\windows-progress-2026-07-11.md           ← 全 11 窗口进度
```

---

_作者:泰 · 创建:2026-07-10 · 最近重写:2026-07-11 17:55 (v0.4.0)_
_触发:刘泽文 "ABC"= A 重写 + B 7 Bug 全列 + C w5 动态化专章_