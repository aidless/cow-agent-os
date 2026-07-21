---
name: paper-review-toolkit
description: 统一入口调起 paper-writing-agent + tmlr-review-simulator + tmlr_pipeline 三个工具。当用户说"审稿 / 模拟审稿人 / 投稿前自检 / 跑 review / 出 reviewer 报告 / 用对抗视角看 paper / 多 reviewer 并行 / TMLR format / 给 rebuttal"时启动。8 个子命令: doctor / quick / standard / full / rebuttal / audit / all / tool。已修复 7 个上游 bug(A:CLI import 失败 / B:paper_profile.py 写死 PDF / C:verify_p*.py 退出码误判 / D:verify severity 显示错位 / E:env_config 不传给子进程 / F:C2 regex 兼容性 + verify-after-patch 强 gate / G:verify 实测 ≠ audit 报告)+ 7/11 w5 self-evolve 加 1 个(H:跨 paper ablation 时 None verify_py 崩溃)。**v0.4.1(7/11 19:50):Bug D 真修复落地 5 个 verify_p[1-5].py,加 effective_severity() 函数 + 5 处调用点;实测 PAPER5 从 0H/3M 变为真 3H/0M,PAPER4 从 0H/10M 变 1H/9M**。
user-invocable: true
version: 0.4.2
author: Mavis + User
license: MIT
dependencies:
  - python >= 3.9
  - pdfplumber >= 0.11 (PDF 解析)
tags:
  - paper-writing
  - reviewing
  - tmlr
  - wrapper
  - multi-tool
---

# Paper Review Toolkit (wrapper)

把 `paper-writing-agent` + `tmlr-review-simulator` + `tmlr_pipeline` 三个工具
统一封装成 `review_paper.py`,8 个子命令覆盖所有审稿场景。

## 何时启动

**启动条件**(用户明确要做审稿相关动作):

- "帮我审稿 / 模拟审稿人 / 投稿前自检"
- "跑一下 review / 出个 reviewer 报告"
- "用对抗视角看 paper / 3 reviewer 并行"
- "TMLR 格式 review / 给 rebuttal"
- "audit 一下 / 跑 verify_p5"
- "跑 review_paper / paper review"

**不启动**(直接路由到其他 skill):

- "写论文 / 改摘要 / 润色" → paper-writing-agent 的 writing 部分
- "查文献 / 找 related work" → arxiv-tracker / light-literature-search
- "画图" → light-figure-drawing

判据：**用户在"审稿 / 模拟审稿人 / 投稿前对抗式审视 / 跑工具" → paper-review-toolkit**。

## 快速上手

```powershell
cd F:\Research\PAPER5_CONSOLIDATED
python F:\Research\review_paper.py quick main.tex         # 3 秒, $0, 启发式
python F:\Research\review_paper.py standard main.tex      # 30 秒, $0.05, 1 LLM
python F:\Research\review_paper.py full main.tex          # 2 分钟, $0.15, 4 LLM
python F:\Research\review_paper.py doctor                 # 检查工具路径
```

## 8 个子命令

| 命令 | 干啥的 | LLM | 成本 | 时间 |
|---|---|---|---|---|
| `doctor` | 检查 3 个工具是否到位 | 0 | $0 | 0.5s |
| `quick <paper>` | identify + evaluate + paper_profile + verify_p* | 0 | $0 | ~5s |
| `standard <paper>` | 单 reviewer(走 simulate_review.py) | 1 | ~$0.05 | ~30s |
| `full <paper>` | 3 reviewer 并行 + self-review | 4 | ~$0.15 | ~2min |
| `rebuttal <review> [--paper <tex>]` | review → TMLR rebuttal prompt | 1 | ~$0.05 | ~30s |
| `audit` | 仅跑当前目录的 verify_p<N>.py | 0 | $0 | ~3s |
| `all <paper> [--skip ...]` | quick + standard + full + audit | ~5 | ~$0.22 | ~3min |
| `tool <subcmd> --file <paper>` | 单跑 paper-writing-agent 子命令 | 0 | $0 | ~1s |

## 已修复的 5 个上游 bug

### Bug A · paper-writing-agent CLI 跑不动

`paper_writing_agent/__init__.py` eager-import `.core` 模块,导致:
- `python cli.py` → `ImportError: attempted relative import`
- `python -m paper_writing_agent.cli` → `ModuleNotFoundError`

**修复**: wrapper 直接 `import core.paper_type_identifier` 等模块,绕开坏掉的 `__init__.py`。

### Bug B · paper_profile.py 写死 PDF

`paper_profile.py` line 142: `card = build_paper_card(sys.argv[1])` 永远走 pdf_ingest,
给 `.tex` 也试图当 PDF 解析 → `PdfminerException: No /Root object!`

**修复**: wrapper 检测后缀,`.tex` → `tex_ingest.py`,`.pdf` → `pdf_ingest.py`。

### Bug C · verify_p<N>.py "有 findings" = exit non-zero

审计脚本的契约是"找到问题就退出非零",但朴素 wrapper 把这当失败。

**修复**: `rc==1` 显示"audit ran with findings",`rc==2` 才当崩溃。

### Bug D · `verify_p<N>.py` print_finding 的 severity 显示 bug(2026-07-11 发现)

每篇 verify_p*.py 的 print 循环用 `SEVERITY[cat]` 查表决定显示 `[HIGH]` / `[MEDIUM]` / `[LOW]`,
但很多 finding 内部消息以 `"HIGH:"` / `"MED:"` / `"LOW:"` 开头,**两个标签可能不一致**。
典型样本:`[MEDIUM] C9 (line 216) HIGH: figure fig:xxx has no caption` — 外层 MED, 真实 HIGH。

**症状**: 跑 `verify_p5.py` 拿到 0/3/3 (0 高/3 中/3 低),看起来都是 medium 不严重 ——
但实际里那 3 个 C9 全部是 HIGH 级问题(图表缺 caption = 投稿前必修)。

**修复**: 在每篇 verify_p*.py 的 print 循环里,**根据 msg 内容自适应 severity**:
```python
def effective_severity(cat, msg):
    base = SEVERITY[cat]
    first_line = msg.split('\n', 1)[0]
    if first_line.startswith('HIGH:'):
        return 'HIGH'
    if first_line.startswith('LOW:'):
        return 'LOW'
    return base
```
然后所有 summary 计数 / TOTAL / rc 都用 effective_severity 而不是 SEVERITY[cat]。

**已批量修复(2026-07-11 19:50,v0.4.1)**: `tmp/_apply_bug_d_fix.py` 把 effective_severity 应用到 PAPER1/2/3/4/5 的 verify_p[1-5].py,共 5 处调用点替换:
1. `Findings by category:` 段的 `sev = SEVERITY[cat]`(注:此段仍用类别默认,因为是按 cat 聚合)
2. `all_findings.sort(key=lambda x: ...)` 用 `effective_severity(x[0], x[1])`
3. DETAILED FINDINGS 循环的 `sev = SEVERITY[cat]` → `sev = effective_severity(cat, msg)`
4. TOTAL 行的 `sum(summary[c] for c in summary if ...)` → `sum(1 for c, m, _ in all_findings if effective_severity(c, m) == "HIGH")`(关键:从 category 级计数改为 per-finding 计数)
5. 退出码的 `any(SEVERITY[c] == 'HIGH' for c, _, _ in all_findings)` → `any(effective_severity(c, m) == 'HIGH' for c, m, _ in all_findings)`

**备份**: 每个 verify_p<N>.py 备份为 `verify_p<N>.py.bak_pre_bugD_2026-07-11`。

**实测影响**(v0.4.1 后):

| Paper | v0.4.0 旧数字 | **v0.4.1 真数字** | 含义 |
|---|---|---|---|
| PAPER1 | 0H/2M/3L | 0H/2M/3L | 无变化(此 paper 无 HIGH: 前缀的 finding) |
| PAPER2 | 0H/5M/2L | 0H/5M/2L | 无变化 |
| PAPER3 | 0H/12M/3L | 0H/12M/3L | 无变化 |
| **PAPER4** | 0H/10M/4L | **1H/9M/4L** | 1 个 finding msg 有 `HIGH:` 前缀,真升级 HIGH |
| **PAPER5** | 0H/3M/0L | **3H/0M/0L** | 3 个 C9 全部 HIGH — paper 真正的"投稿前必修" |

**对 5 月 deadline 决策的冲击**: PAPER5 的 "0H 可投" 叙事 **被推翻**,真状态是 **3H**(3 个 figure 缺 caption)。w6-paper-repair 14:25 报告的 "4 HIGH → 0" 是基于错误计数。
**真投 PAPER5 前必做**: 给 3 个 figure 加 `\caption{...}`(PAPER5 main.tex line 767/774 附近)。

**PAPER6**(verify_p6.py 14,777 bytes,2026-07-11 17:41):**独立脚本**,不来自 verify_p[1-5].py 模板,**无 Bug D 风险**。

**🪤 教训(7/11 19:50)**:
1. SKILL.md 写"已批量修复 apply_b_fix.py"是 **STALE 文档** —— 真代码根本没改
2. v0.4.0 升级时只改了文档,没动 verify_p*.py 实际代码
3. 任何"已修复"声明必须以 **git diff 或 sha 验证** 为准,不是文档
4. **下次 audit 任何 paper 前必先 `git diff verify_p<N>.py` 确认 Bug D 实际状态**

### Bug E · `env_config` 设的 OPENAI_API_BASE 不会被子进程继承(2026-07-11 发现)

`env_config` 内部维护自己的 env 副本(hermes-agent process memory),**不写 OS env**。
当 Python `subprocess` / `urllib` 启动时,只继承 OS env,看不到 env_config 配的 BASE → 默认会回落到
`https://api.openai.com/v1` 而不是 DeepSeek。表现:`urllib` 调用 401 Unauthorized,
即使 curl 测试时是通的(curl 在同一个 shell,看到的是 shell 的 env)。

**症状**:
- `env_config get OPENAI_API_BASE` = `https://api.deepseek.com/v1`(配置正确)
- 但 `python -c "import urllib...urlopen..."` 用的是 `https://api.openai.com/v1`(默认)
- `OPENAI_API_KEY` 设了也白搭(目标根本不是 DeepSeek)

**正确做法**(在批量调用脚本里):
```python
import os
os.environ.setdefault('OPENAI_API_BASE', 'https://api.deepseek.com/v1')  # 硬设 fallback
os.environ.setdefault('OPENAI_API_KEY', '...')  # 同样硬设 或 强制从 env_config reload
```
不要假设 env_config 的设置会"自动"传播到子进程。

**已经踩坑的脚本**: `run_review_llm.py` 加了硬设 fallback 后重跑全部 25 个调用成功。

### Bug F · C2 HIGH 报警的 regex 兼容性陷阱 + verify-after-patch 强 gate(2026-07-11 self-evolve)

**真坑**: 5 篇 verify_p*.py 的 `c2_section_pattern`(C2 = "Statistical analysis section must include power analysis")都用单形态 `\\section\\*?\\{...\\}`。PAPER2 12:12 patch 把 power analysis 写进 `\\subsection*{Statistical Note and Power Analysis}` —— regex **不支持 `\\subsection`**,所以无论 patch 内容多正确,verify 永远报 HIGH C2。

**跨篇共性**: 同一 regex bug 在 PAPER2 / PAPER3 / PAPER4 的 verify_p<N>.py 都中招(PAPER3 有 `\\section{Method}` 内含"Method",PAPER4 有 `\\subsection{Relationship to Statistical Power}`,都死在 regex 兼容性上)。PAPER1 / PAPER5 的 verify **没这个 bug**(它们已经用 OR 模式 `\\\\section|\\\\subsection`)。

**根因**: skill 模板没强调 "C2 section 检测 regex 必须兼容 `\\subsection`",导致每个新写的 verify_p<N>.py 都会重蹈覆辙。

**修复**:
- 治标:把所有 verify_p*.py 的 `c2_section_pattern` 改为 OR 模式 `(?:\\\\section|\\\\subsection)\\*?\\{...\\}`
- 治本:**任何 C2 HIGH 报警,先验证 verify regex 是否支持 `\\subsection` —— 不要立刻改 main.tex**

```python
# WRONG(只能匹配 \section)
C2_SECTION_PATTERN = re.compile(r'\\section\*?\{[^}]*[Pp]ower[^}]*\}')

# RIGHT(支持 \section 和 \subsection)
C2_SECTION_PATTERN = re.compile(r'\\(?:section|subsection)\*?\{[^}]*[Pp]ower[^}]*\}')
```

**配套硬 gate(2026-07-11 反复踩的另一个坑)**:**PATCH 后必 verify,不靠文件大小涨没涨判断**。

- ❌ 错: `python apply_fix.py` → `main.tex` 大小 +1146 bytes → 报告"PATCH 完成"
- ✅ 对: `python apply_fix.py` → `python verify_p<N>.py` → 确认 HIGH/MED/LOW 计数真降了 → 才算"PATCH 完成"

**12:12 那个反例**: PAPER2 patch 写了 1146 bytes,文件大小也涨了,但 verify 仍报 HIGH=1 —— 因为 patch 进了 `\\subsection` 而 verify regex 不识别,**没人现场跑 verify 所以没发现**。接力 session 浪费一轮诊断时间。

**自动 gate**(在 apply_fix.py 里加):
```python
# PATCH 后立即 verify 一次,必须看到目标 finding 数下降
def verify_after_patch(before_total, expected_drop):
    rc, stdout, _ = run(f'python verify_p{args.paper}.py')
    after_total = parse_total(stdout)
    assert after_total <= before_total - expected_drop, (
        f'PATCH 无效: {before_total} → {after_total} (期望至少降 {expected_drop})'
    )
```

### Bug G · audit 报告 ≠ verify 实测,后者才是 ground truth(2026-07-11)

**真坑**: paper-review-toolkit 的 `audit` / `full` 子命令把 verify_p<N>.py 输出 + LLM review 整合成"audit 报告"。但:

- PAPER5 audit 报 3 HIGH(3 figure caption),实测 verify_p5.py 真 HIGH = **0**(Bug D 残留把 HIGH 显示成 MED,但 EFFECTIVE_SEVERITY 修正后 MED 还是 MED)
- PAPER1 audit 报 6 MED,实测 verify_p1.py MED = **2**(audit 把 LOW 误升 MED)
- 真数字 = **现场跑 verify 的 stdout**,不是 audit 报告里的计数

**为什么 audit 计数会偏**: audit 综合 verify_p* + LLM review + 启发式三层,LLM 经常把 LOW 误判 MED 或反之。**verify_p*.py 是 deterministic rule-based**,直接读 main.tex,跟 LLM 不挂钩,结果是 ground truth。

**修复**:
- `audit` 子命令必须输出 3 段:**verify 实测** + **audit 推断** + **差异**(实测和推断不同的地方标 ⚠️)
- 任何决策以 **verify 实测** 为准,audit 推断只作补充

```markdown
## Verify 实测(ground truth)
| PAPER | HIGH | MED | LOW | TOTAL |
| --- | --- | --- | --- | --- |
| PAPER1 | 0 | 2 | 3 | 5 |
| PAPER2 | 1 | 4 | 2 | 7 |
| ... |

## Audit 推断(LLM-assisted)
| PAPER | HIGH | MED | LOW | TOTAL |
| ... |

## 差异 ⚠️
- PAPER5:audit 报 3 HIGH → 实测 0(Bug D 残留,已修)
- PAPER1:audit 报 6 MED → 实测 2(LLM over-flag LOW)
```

**新规**:任何"修 HIGH/MED/LOW"的决策前必跑 `python verify_p<N>.py | findstr TOTAL`,**不靠 audit 报告的描述**。

### Bug H · 跨 paper ablation 时 `verify_py=None` 崩溃(2026-07-11 w5 ablation 发现)

**真坑**: `ablation_real.py` 的 `run_verify_py(paper.verify_py, ...)` 假设 `verify_py` 非空。
但在 cross-paper ablation 里,paper list 可能包含:
- 你的 `PAPER*_CONSOLIDATED/main.tex`(有 verify_p<N>.py)
- 别人的 arxiv paper `.tex`(没 verify_p<N>.py)

→ `RealPaper.discover` 让 `verify_py = None`,调用方没 None check → `subprocess.run([None, ...])` 触发
`FileNotFoundError: [WinError 2]` 或 `PermissionError`,**整个 ablation 跨掉**,问题静默。

**典型症状**: 前 N 个有 verify 的 paper 跑完 N×4 strategy ≈ 24 runs,遇到 arxiv paper 时
stdout / stderr 突然断流,python 进程消失或 review 文件半截。

**根因**:
- `RealPaper` dataclass 把 `verify_py` 标 `Path`(非 `Optional[Path]`)→ type hint 误导
- `discover_all_papers` 的 `if rp and rp.verify_py` 允许 None 漏过 type hint
- `run_verify_py` 没处理 None

**修复**(在 `ablation_real.py` 里):
```python
def run_verify_py(verify_py: Optional[Path], ...) -> Tuple[int, str, int, int, int]:
    if verify_py is None or not verify_py.exists():
        return (0, "no verify script", 0, 0, 0)  # 跑下个 paper,不影响整体
    ...
```

**配套**: 任何"跨 paper" / "novel paper" ablation 必须**先验 `verify_py` 存在**,再算 findings。
```python
findings_total = sum(c[0] for c in findings) if verify_py else 0
```

**🪤 教训(2026-07-11 w5)**:
1. 跨 paper 跑 ablation 时,**先列 paper 类型分布**(有 / 无 verify_p<N>.py)
2. dataclass 字段如果是真可能为 None,**type hint 必写 `Optional[Path]`**
3. subprocess / Path 调用前**第一件事**是 None check + exists check,不要靠 try/except
4. 任何"通用 ablation runner"必须有**partial failure 容忍**(一个 paper crash 不应拖垮 11 paper)

---

## 路径覆盖

```powershell
$env:REVIEW_TOOL_PWA = "F:\Research\paper-writing-agent"
$env:REVIEW_TOOL_SIM = "F:\Research\tmlr-review-simulator"
$env:REVIEW_TOOL_PIPE = "F:\Research\tmlr_pipeline"
python F:\Research\review_paper.py doctor
```

## 文件结构

```
F:\Research\review_paper.py                        # 主脚本(695 行, 纯 stdlib)
F:\Research\REVIEW_PAPER_README.md                 # 完整文档
C:\Users\Administrator\cow\skills\paper-review-toolkit\
    ├── SKILL.md                                    # 本文件
    ├── review_paper.py                             # 副本(让 skill 库自包含)
    └── REVIEW_PAPER_README.md                      # 副本
```

## 已知限制

1. `standard` / `full` / `rebuttal` 需要 `OPENAI_API_KEY` (或兼容 base,你已配 DeepSeek)
2. PDF 解析对图表/双栏布局有限制,推荐 `.tex`
3. `tmlr_pipeline` 暂未直接接入 — 通过 `tool` 间接调用

## 测试结果(2026-07-10, PAPER5)

- `doctor` ✅ 5/5 工具路径 OK
- `quick` ✅ 5/5 子任务全 OK
- `tool evaluate --file main.tex` ✅ 输出 PAPER5 整体 B 级 88.5%
- `tool identify --file main.tex` ✅ 输出 18 种类型打分, top "analysis" 9.09%

启发式打分偏乐观(B 级 88.5%),硬规则审计找出 7 个真问题 → 两层都要看。

## CHANGELOG

### v0.4.2(2026-07-11 23:50,w5 self-evolve,Bug H 文档化)

- **新增 Bug H**:跨 paper ablation 时 `verify_py=None` 崩溃(`Optional[Path]` type hint 缺失 + `run_verify_py` 无 None check)
- **症状**:cross-paper ablation 中,跑完自有 PAPER1-6 后遇到无 verify 脚本的 arxiv paper 时,python 进程消失 / review 文件半截 / `subprocess.run([None, ...])` 触发 `FileNotFoundError`
- **修复**: 在 `ablation_real.py` 加 `if verify_py is None or not verify_py.exists(): return (0, "no verify script", 0, 0, 0)`
- **应用范围**: 任何 `paper-review-toolkit` 衍生 ablation 脚本(ablation_real.py / ablation_pilot.py / ablation_judged.py / run_ablation.py)
- **配套教训**:
  1. cross-paper ablation 前先验 `verify_py` 存在分布
  2. dataclass 字段真可能 None 时,**type hint 必写 `Optional[Path]`**
  3. 通用 ablation runner 必须 partial-failure tolerant
- **来源**: w5 paper-review-dynamic 收工 session(`tmp/windows/w5-paper-review-dynamic/`)

### v0.4.1(2026-07-11 19:50,Bug D 真修复)

- **真修**:5 个 verify_p[1-5].py 加 `effective_severity()` 函数 + 5 处调用点替换
- **实测**:PAPER5 从 0H/3M 变为 **3H/0M**(3 个 figure caption 缺失升级为 HIGH);PAPER4 从 0H/10M 变 1H/9M
- **备份**:`verify_p<N>.py.bak_pre_bugD_2026-07-11` 在每个 PAPER_CONSOLIDATED 目录
- **脚本**:`tmp/_apply_bug_d_fix.py`(可重用,5 文件幂等修复)
- **教训**:v0.4.0 SKILL.md 写"已批量修复 apply_b_fix.py"是 STALE 文档;真代码未改。**任何"已修复"声明必以 sha256 diff 验证**。
- **影响**:
  - PAPER5 "0H 可投" 叙事被推翻,真状态 3H 需修 3 个 figure caption
  - w6-paper-repair 14:25 报告"4 HIGH → 0"基于错误计数

### v0.4.0(2026-07-11 14:25,Bug F/G self-evolve)

- **新增 Bug F**:C2 HIGH 报警的 regex 兼容性陷阱(OR 模式) + verify-after-patch 强 gate
- **新增 Bug G**:audit 报告 ≠ verify 实测,后者才是 ground truth
- **状态**:文档已记录,但**部分实现未落地**(Bug D 修复只改了文档,没改代码 → v0.4.1 才真补)
- **配套**:tmp/fix_p*_v*.py 9 个失败版本归档至 `tmp/_archive/w6-fix-attempts-2026-07-11/`,只留 `fix_p2_v7.py`(真修)

### v0.3.x 及之前

- Bug A:CLI import 失败 → 修
- Bug B:paper_profile.py 写死 PDF → 修
- Bug C:verify_p*.py "有 findings" = exit non-zero → 修(`rc==1` vs `rc==2` 区分)
- Bug D:verify severity 显示错位 → **v0.4.1 才真修**
- Bug E:env_config 不传给子进程 → 修(脚本内硬设 fallback)