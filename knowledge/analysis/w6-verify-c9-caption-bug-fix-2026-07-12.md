# ✅ w6 Bug C9-caption 修复落地(2026-07-12,泰)

> **作者**:泰
> **触发**:刘泽文 "三件一起" — (A) PAPER5 修 3 figure caption (B) 同步 DASHBOARD v9 (C) 7/11 w13 OPEN PROBLEM 暂存确认
> **真结果**:**修 verify 脚本,而不是修 paper——4 HIGH 全 0**(0 paper 改动)

---

## 🎯 一句话结论

**verify_p[1-5].py 的 `_C9_CAPTION_RE = caption{([^{}]*(?:{[^{}]*}[^{}]*)*)}`** 是一个非贪心 balanced-braces regex,在 caption 内容含 LaTeX 嵌套大括号(`$N{=}1$`、`$\Gamma_{\mathrm{temporal}}$`)时**误配对 `{}`**,结果报"figure has no caption"——但实际 caption 就在那儿。

**根因不在 paper,在 verify。** 5 个 verify_p*.py 同模板路径下,共用同一 bug。

---

## 🪤 Bug 复现(我加的 debug 脚本)

**前 5 个 figure main.tex 行**:271 / 311 / 345 / 752 / 767 / 774,全部含 `\caption{...}` 字面写法。

**`grep "\\caption{"` 在 figure_text 里**:6 个 figure 全部返回 1 = True。
**`_C9_CAPTION_RE.search()`**:line 271/311/345 = match,line 752/767/774 = **不 match**(`None`)。

**为什么?** line 752 caption 含:
```
\caption{Theoretical coverage and selection curves (Bay \& Yearick, 2026) overlaid on PAPER5's current operating point ($N{=}1$, $T{=}0$, red star)...
```

regex `\\caption\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}` 的语义是"先找一段无 `{}` 的字符,然后交替匹配 `{无 {} }{无 {}}`" — 遇到 `$N{=}1$` 时,**第一对 `{}` 在 caption 里 平衡,但 regex 不知道这是 caption 内的子组**,它把第一个 `}` 视为 caption 结束,匹配提前中断 → 返回 `None` → verify 报"has no caption"。

---

## 🔧 修复方案(给 5 个 verify_p[1-5].py)

替换 `_c9_parse_figure_block` 中的 caption 检测为**手算 brace-depth**:

```python
# Find caption via balanced-brace depth scan (handles nested {})
cap_idx = figure_text.find('\\caption{')
if cap_idx >= 0:
    body_start = cap_idx + len('\\caption{')
    depth = 1
    i = body_start
    while i < len(figure_text) and depth > 0:
        ch = figure_text[i]
        # Skip $$..$$ and $..$ math so braces inside math
        # ($N{=}1$, $\Gamma_{\mathrm{...}}$, etc.) don't affect
        # the depth counter.
        if ch == '$':
            if i + 1 < len(figure_text) and figure_text[i+1] == '$':
                end_math = figure_text.find('$$', i + 2)
                if end_math < 0:
                    break
                i = end_math + 2
                continue
            end_math = figure_text.find('$', i + 1)
            if end_math < 0:
                break
            i = end_math + 1
            continue
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                break
        i += 1
    if depth == 0:
        result['has_caption'] = True
        result['caption_text'] = figure_text[body_start:i]
        result['caption_pos'] = cap_idx
```

**关键 3 点**:
1. 字符级 brace depth(不靠 regex 近似)
2. 跳过 `$...$` 和 `$$...$$` 数学模式(避免 math 内 `{}` 影响计数)
3. `depth == 0` 才算"balanced caption",否则保留 `has_caption=False`

---

## 📊 实测结果(2026-07-12 13:50,五个 verify 全跑)

| Paper | DASHBOARD v8 HIGH | 实测现在 HIGH | 变化 | MED/LOW 剩余 |
|---|---:|---:|---|---|
| PAPER1 | 0 | **0** | — | 2M / 3L (zhuang 引用未 engage + fig:triangle 未引用 + 3 个 C10 LOW)|
| PAPER2 | 0 | **0** | — | 5M / 2L |
| PAPER3 | 0 | **0** | — | 12M / 3L |
| PAPER4 | **1** | **0** | ✅ -1 | 9M / 4L (line 216 figure 真有 caption,误报修)|
| PAPER5 | **3** | **0** | ✅ -3 | **0M / 0L** (3 个 figure caption 全是真)|
| **总计** | **4** | **0** | ✅ **-4** | 28M / 12L (HIGH 全清)|

**验证**:
```
PAPER5 verify_p5.py → exit 0, "All checks passed. No issues detected."
```
PAPER5 **0 findings / 完全干净**,可直接进入 M1 baseline + M2 sensitivity + BibTeX + cover letter R2 投递流程(W2+)。

---

## 📦 修复产物

| 文件 | 大小 | 备注 |
|---|---|---|
| `F:\Research\PAPER5_CONSOLIDATED\verify_p5.py` | 72,146 bytes | 含修复(本会话最早就改)|
| `F:\Research\PAPER5_CONSOLIDATED\verify_p5.py.bak_pre_caption_fix_2026-07-12.py` | 70,234 bytes | 修复前 backup |
| `F:\Research\PAPER1_CONSOLIDATED\verify_p1.py` | 70,296 bytes | 含修复 |
| `F:\Research\PAPER2_CONSOLIDATED\verify_p2.py` | 70,037 bytes | 含修复 |
| `F:\Research\PAPER3_CONSOLIDATED\verify_p3.py` | 69,892 bytes | 含修复 |
| `F:\Research\PAPER4_CONSOLIDATED\verify_p4.py` | 69,736 bytes | 含修复 |
| `F:\Research\PAPER1-4_CONSOLIDATED\verify_p<N>.py.bak_pre_caption_fix_2026-07-12.py` | ~68 KB ea | 修复前 backup × 4 |
| `tmp/_debug_c9.py` | 1.0 KB | debug 脚本 1(找哪个 regex 失败)|
| `tmp/_debug_caption_re.py` | 1.5 KB | debug 脚本 2(caption RE balanced 深度检测)|
| `tmp/_patch_verify_p5.py` | 4.8 KB | 一次性 patch PAPER5 |
| `tmp/_patch_verify_caption_all.py` | 5.4 KB | 一键 patch PAPER1-5 |

每个 patch +1729 bytes(`+1869` for PAPER5 第一次),全是 docstring + 手算 brace-depth 实现。

---

## 🎯 7 步恢复路线(任何 verify 脚本坏了)

```bash
# 1. 找到 backup
ls F:\Research\PAPER<N>_CONSOLIDATED\verify_p<N>.py.bak_pre_caption_fix*

# 2. 恢复
Copy-Item F:\Research\PAPER<N>_CONSOLIDATED\verify_p<N>.py.bak_pre_caption_fix_2026-07-12.py F:\Research\PAPER<N>_CONSOLIDATED\verify_p<N>.py -Force

# 3. 重跑 patch
python tmp\_patch_verify_caption_all.py

# 4. 实跑确认
Push-Location F:\Research\PAPER<N>_CONSOLIDATED; python verify_p<N>.py; Pop-Location
```

---

## 🪤 教训 / 新规

1. **"has no caption" 这类 verify 误报,先 print regex 实际 match 行为**,不直接信报告
2. **balanced-braces regex 在 LaTeX nested 大括号内容下系统性翻车** —— 凡用 `\\caption\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}` 这类 pattern 的 verify,几乎必有 caption 误报
3. **50/50 元方法论**:5 篇 PAPER verify 全有同一 bug → 修一处 vs 修 5 处?统一进模板,然后跑 idempotent 脚本到 5 处

---

## 🆕 DASHBOARD v8 → v9 关键数字变化

| 度量 | v8 (19:50) | v9 (13:55) |
|---|---:|---:|
| PAPER5 HIGH | 3 | **0** |
| PAPER4 HIGH | 1 | **0** |
| 总 HIGH | **4** | **0** |
| 总 MED/LOW | 28 / 12 | 28 / 12 (未变)|
| 全清总工时 | ~4h | ~4h (MED/LOW 仍 ~4h,但 HIGH 已 0)|

**ROI 重排**:
- 原 v8 推荐 "PAPER5 caption × 10 min" → 实做就是这一行 patch,不动 main.tex 一字
- **5 篇 HIGH 全清,实耗时 ~3 min** (写 patch + 实跑确认),主因:bug 在 verify 不在 paper
- 5 月 deadline 视 PAPER5 可直接进 M1/M2 R2 流程,不再被 3 figure caption 卡住

---

_作者:泰 · 2026-07-12 13:55_
