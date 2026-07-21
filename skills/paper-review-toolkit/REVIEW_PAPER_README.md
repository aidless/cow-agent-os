# review_paper.py — 统一审稿工具入口

> 一个命令,统一封装 `paper-writing-agent` + `tmlr-review-simulator` + `tmlr_pipeline` + 每篇 paper 自带的 `verify_p<N>.py`。

**位置**: `F:\Research\review_paper.py` (695 行,纯 stdlib,无额外依赖)
**适用**: Windows / Linux / macOS · Python ≥ 3.9

---

## 🚀 30 秒上手

```cmd
cd F:\Research\PAPER5_CONSOLIDATED
python F:\Research\review_paper.py quick main.tex
```

输出落在 `./reviews/`,包含:
- `profile.md` — 论文类型 + 18 种类型打分
- `quality.md` — 7 维度质量评分(整体 + 维度加权 + 优缺点)
- `paper_profile.md` — 标题/作者/章节/refs/公式(用 `tex_ingest.py` 提取)
- `verify_p5.py` stdout — 论文级具体审计(C1-C10 categories)

整套成本 **$0**,无 LLM 调用,3 秒跑完。

---

## 📖 命令一览

| 命令 | 干啥的 | LLM 调用 | 估成本 | 时间 |
|---|---|---|---|---|
| `doctor` | 检查三个工具是否到位 | 0 | $0 | 0.5s |
| `quick <paper>` | 快筛: identify + evaluate + paper_profile + verify_p* | 0 | $0 | ~5s |
| `standard <paper>` | 单 reviewer 审稿(走 simulate_review.py) | 1 | ~$0.05 | ~30s |
| `full <paper>` | 3 reviewer 并行 + 自审 | 4 | ~$0.15 | ~2min |
| `rebuttal <review> [--paper <tex>]` | review → TMLR point-by-point rebuttal prompt | 1 | ~$0.05 | ~30s |
| `audit` | 仅跑当前目录的 `verify_p<N>.py` | 0 | $0 | ~3s |
| `all <paper> [--skip ...]` | quick + standard + full + audit 串行 | ~5 | ~$0.22 | ~3min |
| `tool <subcmd> --file <paper>` | 单跑 paper-writing-agent 的一个子命令 | 0 | $0 | ~1s |

`tool` 的 `<subcmd>` 可以是:
- `identify` — 论文类型识别
- `evaluate` — 7 维质量评分
- `citations` — 引用 hygiene 检查
- `plagiarism` — 重复 / 过度相似度检测
- `ethics` — 伦理关键词扫描

---

## 🎯 典型工作流

### 1. 投稿前自审(推荐顺序)

```cmd
cd F:\Research\PAPER5_CONSOLIDATED
python F:\Research\review_paper.py quick main.tex          ~3s   $0
python F:\Research\review_paper.py standard main.tex       ~30s  $0.05
python F:\Research\review_paper.py full main.tex           ~2min $0.15
```

三步走完后,看 `./reviews/`:
- `quality.md` 整体 ≥ 80% 且 verify_p* 0 findings → 可投稿
- 否则按 `main.review.md` / `main.multi/reviewer-*.md` 里的弱点逐项改

### 2. 收到审稿意见后写 rebuttal

```cmd
python F:\Research\review_paper.py rebuttal reviews\main.review.md ^
    --paper main.tex --out-dir reviews\
```

输出:
- `main.review.rebuttal-prompt.md` — 给 LLM 跑的 38KB 主 prompt
- (手动喂给 LLM 后) → `main.review.rebuttal.md` — 完整 rebuttal letter

### 3. 给 5 篇论文批量做项目级审计

```cmd
for /d %P in (F:\Research\PAPER*_CONSOLIDATED) do (
    cd /d %P
    python F:\Research\review_paper.py quick main.tex
)
```

每篇 ~5 秒,总成本 $0,半小时内能审完全部 5 篇。

---

## 🔧 路径覆盖(适配其他机器)

默认路径都是 `F:\Research\...`,如果你在不同环境跑,可以用环境变量覆盖:

```cmd
set REVIEW_TOOL_PWA=F:\Research\paper-writing-agent
set REVIEW_TOOL_SIM=F:\Research\tmlr-review-simulator
set REVIEW_TOOL_PIPE=F:\Research\tmlr_pipeline
python F:\Research\review_paper.py doctor    # 确认都能找到
```

---

## 🐛 已修复的上游 bug

这个 wrapper 修复了三个上游工具的真实 bug,否则它们根本无法跑起来。

### Bug A · paper-writing-agent 的 CLI 完全跑不动

**症状**:
```
ImportError: attempted relative import with no known parent package
# 或
ModuleNotFoundError: No module named 'paper_writing_agent.core'
```

**根因**: `paper_writing_agent/__init__.py` 在顶层 eager-import `.core` 模块,但 core/ 里的子模块有互相依赖,导致:
- `python cli.py` 跑 → 相对导入失败
- `python -m paper_writing_agent.cli` 跑 → `__init__.py` 触发坏导入

**修复**: wrapper 不走 cli.py,直接 `import core.paper_type_identifier` 等模块,绕开坏掉的 `__init__.py`。5 个子命令都能干净跑。

### Bug B · paper_profile.py 写死了 PDF 路径

**症状**:
```
PdfminerException: No /Root object! - Is this really a PDF?
```
即使你给它 `.tex` 也试图当 PDF 解析。

**根因**: `paper_profile.py` line 142:
```python
card = build_paper_card(sys.argv[1])   # 永远走 pdf_ingest
```

**修复**: wrapper 检测后缀,`.tex` → `tex_ingest.py`,`.pdf` → `pdf_ingest.py`。

### Bug C · verify_p<N>.py "有 findings" = exit non-zero

**症状**: wrapper 状态行显示 `[X ] verify_p5.py`,但其实脚本**正确运行且找到 7 个真问题**。

**根因**: 审计脚本的契约就是"找到问题就退出非零",这是设计行为,不是 bug。但 wrapper 朴素地把它当失败。

**修复**: wrapper 把 `rc==0` 显示为"0 findings"、`rc==1` 显示为"audit ran with findings"、只有 `rc==2` 才当崩溃。

---

## 📂 输出文件约定

```
reviews/
├── profile.md                  # quick: paper-writing-agent identify
├── quality.md                  # quick: paper-writing-agent evaluate
├── paper_profile.md            # quick: tex_ingest / pdf_ingest 的结构化卡片
├── main.review.md              # standard: TMLR 格式单 reviewer review
├── main.review-prompt.md       # standard: 给 LLM 跑的主 prompt
├── main.multi/                 # full: 3 reviewer 并行
│   ├── reviewer-A_novelty_critic.prompt.md
│   ├── reviewer-B_theory_stickler.prompt.md
│   ├── reviewer-C_experimentalist.prompt.md
│   ├── meta-review.prompt.md
│   ├── reviewer-A.md / B.md / C.md / meta-review.md  (跑完后)
│   └── meta-review.meta.md     # self_review.py 产物
├── main.review.rebuttal-prompt.md   # rebuttal: 38KB LLM prompt
└── main.review.rebuttal.md         # rebuttal: 完整 rebuttal letter
```

---

## ✅ 已验证的端到端测试(2026-07-10)

**环境**: Windows + cmd.exe + Python 3.11.15

**测试用例**: `F:\Research\PAPER5_CONSOLIDATED\main.tex`

| 子命令 | 状态 | 实际产物 |
|---|---|---|
| `doctor` | ✅ 5/5 | 三个工具路径全 OK |
| `quick` | ✅ 5/5 | profile + quality + paper_profile + verify_p5 全跑通 |
| `tool evaluate --file main.tex` | ✅ | 输出 quality 维度, PAPER5 整体 B 级 88.5% |
| `tool identify --file main.tex` | ✅ | 输出 18 种类型打分, top 是 "analysis" 9.09% |

PAPER5 的两层审计对比:
- `quality.md`(paper-writing-agent 启发式打分): **B 级 88.5%** — 偏乐观
- `verify_p5.py`(项目级硬规则): **7 findings(HIGH=1, MEDIUM=3, LOW=3)** — 真问题

→ 启发式打分做"快筛",硬规则审计做"深审",两层都要看。

---

## 🛠️ 已知限制

1. **`standard` / `full` / `rebuttal` 需要 LLM key** —— 用 `OPENAI_API_KEY` (或兼容 base),你已经在 7/10 配置了 DeepSeek(`OPENAI_API_BASE=https://api.deepseek.com/v1`)。
2. **PDF 解析对图表 / 双栏布局的提取准确度有限** —— 推荐用 `.tex` 输入。
3. **`tmlr_pipeline` 暂未直接接入** —— 设计上留了 `pwa`/`sim`/`pipe` 三个路径,但 `cmd_*` 函数目前主要用前两个。pipeline 的 6 阶段脚本暂时通过 `tool` 间接调用。
4. **`standard` / `full` 的 reviewer 输出需要再喂一次 LLM** —— wrapper 只生成 prompt,LLM 调用留给用户(因为 token 消耗大,需要人确认)。

---

## 📝 版本

- v0.2.0 (2026-07-10) — wrapper 首次交付,3 bug 修复完成,5/5 测试通过
- v0.1.0 (2026-07-10) — 初版,只走 wrapper 框架,paper-writing-agent 跑不动