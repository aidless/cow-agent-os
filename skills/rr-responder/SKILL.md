---
name: rr-responder
version: 0.1.0
status: live
description: |
  把审稿人意见转换为 R&R(rebuttal)回应草稿。4 段 pipeline:
  1. review2queries.py — 把段落级意见拆成原子子问题
  2. deep_critique.py — 对每条子问题做 reviewer-side 刁难(A+B 的 "+B" 部分)
  3. draft_response.py — author-side 综合输出 R&R draft,可选融入 author notes
  4. render_latex.py — draft → Markdown 或 LaTeX 可粘贴片段
triggers:
  - "rr"
  - "rebuttal"
  - "revise"
  - "resubmit"
  - "reviewer"
  - "审稿"
  - "写 R&R"
  - "rebuttal 回应"
  - "reviewer 意见"
  - "修改回信"
requires:
  - OPENAI_API_KEY
  - OPENAI_API_BASE (default https://api.deepseek.com/v1)
  - python 3.10+
runtime:
  - llm:      # needs api key
  - partial:  # stage 1/4 also work w/o key (worst-case stub output)
inputs:
  - --review PATH.md|txt
  - --author-notes PATH (optional, 推荐写「已做修改」摘要)
outputs:
  - JSONL  (stage1/stage2/stage3 中间态)
  - Markdown / LaTeX  (stage4 终态,paste into paper appendix)
---

# rr-responder

## 它做什么

**4 段 pipeline**:review 段落 → 原子子问题 → reviewer 刁难 → author draft → 可粘贴文本。

A+B 双重模式:
- **A(Draft)**:子问题直接生成中性化、R&R 措辞的回复
- **B(Critique)**:在生成前,先做一轮"模拟 reviewer 反弹",确保每个回复都直面潜在追问

## 何时用

- 你刚拿到 TMLR / NeurIPS / ICLR 审稿意见,需要写 rebuttal
- 你写完 R&R 想检验"是否每个 follow-up 都被答到"
- 想批量给 PAPER1/2/3/4 各路意见做 R&R draft(每路 ≤1 小时)

## 工作流

```
┌──────────────────────┐    ┌────────────────────────┐    ┌──────────────────────────┐    ┌────────────────────┐
│ 1. review2queries.py │ →  │ 2. deep_critique.py    │ →  │ 3. draft_response.py     │ →  │ 4. render_latex.py │
│ 段落 → 原子子问题    │    │ + 模拟 reviewer 刁难   │    │ 1+2+author-notes → draft │    │ → markdown/LaTeX   │
│ JSONL  ↓             │    │ + follow-ups           │    │ 中性化 R&R 措辞          │    │ 直接贴论文 appendix│
└──────────────────────┘    └────────────────────────┘    └──────────────────────────┘    └────────────────────┘
```

### 默认用法(orchestrate 一键)

```bash
python skills/rr-responder/scripts/orchestrate.py \
    --review reviews/reviewer1.md \
    --author-notes drafts/changes_summary.md \
    --out-md response.md
```

输出:`tmp/rr_run_<timestamp>/{stage1..3.jsonl, response.md}` + 中间态保留。

### 单独跑某个 stage

```bash
# 仅跑 stage 4(已有 stage3 JSONL)
python scripts/render_latex.py --in stage3.jsonl --out response.md --format md

# 跳过 stage 2(预算紧 / 只想快速过)
python scripts/orchestrate.py --review review.md --skip-critique --out-md response.md

# LaTeX 模式(stage 4 直接出 LaTeX 片段)
python scripts/render_latex.py --in stage3.jsonl --out response.tex --format latex
```

### Author notes 写什么

**一段 free-form 文本**,说明这版修改已经做了哪些动作。建议格式:

```markdown
- Added Table N with cross-model results (model-A, model-B) in §X.Y
- Extended proof of Theorem 1 (Appendix C); renumbered
- Added §Z.W "Robustness to Adversarial Agents" — ...
- Expanded Limitations §7: ...
- Added comparison to CONSENSUS-X (NeurIPS 2026) in §2; new Table M
```

LLM 会把这些**融进每条 reply**,确保"我们的回复"和"论文实际修改"对得上。

## 输出质量(已实测)

9 条子问题 → 1 段中性化 R&R + 1 段具体修改清单 + 2-3 个 follow-up Q&A,**每条都引用 §/Table/Figure**。

✅ 没有 "future work" / "we will consider" 这类搪塞式结尾
✅ 每条以 "We thank Reviewer X for..." 开头
✅ Follow-up 都被直面回答(不会留 "<TODO>" 占位)

## 系统默认配置

| 项 | 默认值 |
|---|---|
| Reviewer id 提取 | 自动(从 "Reviewer 1" / "## R1" 检测) |
| 模型 | `deepseek-v4-flash` |
| 并发 | stage 1/2/3 默认 3-4 workers |
| Stage 4 输出 | Markdown(`--format latex` 切 LaTeX) |
| 评分 | paper-side 1-5 严重度(stage 1 LLM guess) |

## 失败兜底

| 错误 | 兜底 |
|---|---|
| `OPENAI_API_KEY` 未配 | stage 1/2/3 输出 `[no_api_key]` 占位;stage 4 仍可跑(stub) |
| Stage 1 LLM 输出非纯 JSON | 调用 `_try_extract_json` 提取首个平衡 `{...}`;再失败走 paragraph fallback |
| Stage 3 follow-up 答案被截断 | 自动 `[LLM 输出超 max_tokens]` → 你的本地编辑补全 |
| arxiv-style <category> 解析失败 | 同上;不影响 stage 3/4 |
| 输入 review 段落过长 | stage 1 `--max-chars` 默认 6000,自动截断 |
| LLM 输出非标准 JSON escape (7/11 Fix 1) | `_json_safety._fix_invalid_escapes` + `strict=False` 兜底 |

---

## 🆕 7/11 真测试 + 5 Fix

### 7/11 真测试(3 个 review 形态全跑)

跑 `PAPER1_CONSOLIDATED/` 的 **3 个真实 review 文件**,验证 pipeline 在真实数据上的稳健性:

| Test | 文件 | 类型 | 输入大小 | 产出 | is_fatal | avg_body |
|---|---|---|---|---|---|---|
| 1 | review_honest.md | 真人 v24.0 自审 | 945 chars | 9 drafts | 3 | 692 chars |
| 2 | review_report_v3.md | 4 角色对抗式 | 5355 chars | 16 drafts | 6 | 835 chars |
| 3 | review_report_v4_honest.md | 诚实重审(rev5→rev6) | 5628 chars | 11 drafts | 5 | 891 chars |
| **合计** | — | — | ~12 KB | **36 drafts** | **14** | **806 chars** |

**关键数据**:**36/36 = 100% 跑通,0 失败**。所有 draft 都是真 LLM 输出(非 fallback),平均 body 长度匹配真实 TMLR rebuttal 段落。

对比报告:`tmp/PAPER1_RR_FINDINGS.md`(146 行,横向对比 3 test)

### 5 个 Fix(打磨发现)

| # | 改动 | 解决了什么 | 验证 |
|---|---|---|---|
| **Fix 1** | `_json_safety._fix_invalid_escapes` + `strict=False` | `Invalid \escape: line 2 column 31` —— LLM 偶尔输出 `\d` `\u`(不完整)等非标准 escape | 5/5 反向验证 (`tmp/rr_paper1_test1/verify_fixes.py`) |
| **Fix 2** | `draft_response.py` SYSTEM_PROMPT 加规则:**`is_fatal=false` 时 `followup_qa=[]`** | Stage 3 过度生成 followup(avg 3.3 个/条),真实 R&R 通常不写 | prompt 内容检查通过 |
| **Fix 3** | `review2queries.py` 的 `fallback_paragraphs` 升级 4 级拆分(markdown heading → 段落 → 句群 → 行) | 整篇 review 当 1 个 atomic 时,fallback 完全无意义 | 4/4 测试(heading / 段落 / 句群 / 行) |
| **Fix 4** | `orchestrate.py` 加 `check_env()` + `--check-env-only` + DEEPSEEK fallback | env_config 写在 hermes-agent 内部,subprocess 看不到 → 需 shell `set "VAR=value"` | `--check-env-only` 跑通 |
| **Fix 5** | `RULE.md` 新增 `Environment Variable Doors` 章节(3 个 trap + 诊断 + 修法) | 7/11 凌晨踩坑沉淀,下次不再犯 | 文档已写入 |

### 关键产物路径

```
tmp/
├── rr_paper1_test1/                    Test 1 产物(9 drafts)
├── rr_paper1_test2/                    Test 2 产物(16 drafts)
├── rr_paper1_test3/                    Test 3 产物(11 drafts)
├── rr_post_fix2/                       Fix 1/2 后端到端重跑
├── PAPER1_RR_FINDINGS.md               横向对比报告(146 行)
└── rr_paper1_test1/verify_fixes.py     反向验证脚本(5/5 过)
```

---

## 🪤 7/11 多脚本 JSON 容错最佳实践

`deep_critique.py` + `draft_response.py` 都必须在 `import` 区加 `sys.path.insert(...)` 后才能用 `_json_safety`:

```python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _json_safety  # 或 from _json_safety import _fix_invalid_escapes
```

或者用 `importlib.util.spec_from_file_location()`(更鲁棒)。



## 与现有 tool 的边界

| 工具 | 关系 |
|---|---|
| `paper-writing-agent` | 写论文**正文**,不写 rebuttal |
| `tmlr-review-simulator` | 模拟**得分 reviewer**给反馈;不写 author 端 rebuttal |
| 本 skill | 写**author 端 rebuttal**,接 pipeline 二者可串 |

## 自定义关键词 / 模板

所有 prompt 都在 `scripts/*.py` 顶部,**system prompt 可改**:
- SYSTEM_PROMPT 控语气(中性化、We thank...)
- USER_TEMPLATE 控输入结构

## 关联资源

- 自身目录:`C:\Users\Administrator\cow\skills\rr-responder\`
- 测试样本:`C:\Users\Administrator\cow\tmp\sample_review_R1.md`(6 段人造 TMLR-style review)
- 测试 author notes:`C:\Users\Administrator\cow\tmp\sample_author_notes.md`
- 实测产物:`C:\Users\Administrator\cow\tmp\rr_run_v2\response.md`(253 行 R&R draft)