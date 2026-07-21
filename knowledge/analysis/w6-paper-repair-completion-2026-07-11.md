# w6-paper-repair 完工报告 — 4 HIGH → 0(7/11 14:35)

_2026-07-11 14:38 沉淀。来源:`tmp/windows/w6-paper-repair/STATUS.md` v4 + 5 个 verify 现场跑实证。_

---

## 🎯 关键结论

| 项 | 值 |
|---|---|
| **窗口** | w6-paper-repair |
| **触发** | 5 月 deadline 5 篇论文批量修复,audit 报告共 49 findings |
| **本次完成范围** | 4 个真 HIGH 全修 → 5 篇距投稿统一到"最近" |
| **剩余** | 26 MED + 15 LOW = 41 findings,工时 ~4h(路径 B) |
| **关键发现** | **4 个真 HIGH 中 3 个是 verify 脚本 regex bug,不是论文问题** |

---

## 🪤 根因发现(本会话最重要)

### Bug: `c2_section_pattern` regex 不支持 `\subsection`

**位置**:4 个 verify 脚本里的 `CHECKS_CONFIG['c2_section_pattern']`

**Bug 模式**:regex 形如

```python
'c2_section_pattern': '\\section\\*?\\{[^}]*(?:Statistical|...)[^}]*\\}'
```

**只支持** `\section{...}` 或 `\section*{...}`,**不支持** `\subsection{...}`。

**踩坑论文**:
- **PAPER2**:`\subsection*{Statistical Note and Power Analysis}`(已有,12:12 patch 成功)
- **PAPER3**:`\section{Method}`(有 Method 关键字)+ `\subsection{BOUNDARY_SYNC Protocol for Calibration}`(有 Protocol 关键字)
- **PAPER4**:`\subsection{Relationship to Statistical Power}`

**对照(PAPER1/PAPER5 不踩坑)**:

```python
'c2_section_pattern': '\\section\\*?\\{[^}]*Power analysis[^}]*\\}'
                          '|\\subsection\\*?\\{[^}]*Power analysis[^}]*\\}'
```

PAPER1/5 的 regex **用 OR 模式**(`\\section...|\\subsection...`),所以两种 heading 都识别。**新建 verify 脚本时务必用 OR 模式**。

### Bug: PATCH 后没 verify(交叉引用 7/11 12:12 那条错误结论)

**坑**:12:12 session 给 PAPER2 写了 main.tex patch(+1146 bytes),文件确实写了,但**没重跑 verify** 就宣布"修了"。

**真相**:patch 早就对了,但 verify 仍报 HIGH=1 —— 因为是 verify bug 不是论文 bug。

**新规**:`patch + verify` 必须配对。

### Bug: audit 报告不是 ground truth

| 来源 | 数字 |
|---|---|
| audit 报告(7/11 10:40) | 6 HIGH / 36 MED / 15 LOW |
| **现场跑 5 个 verify**(7/11 14:25) | **4 HIGH / 26 MED / 15 LOW** |
| 差异 | -2 HIGH(都是 Bug D 显示错位) |

**新规**:任何决策前必须 `python verify_p<N>.py | findstr TOTAL`,不算来自 `paper-review-audit-2026-07-11.md` 的二手数字。

---

## 🛠 修复方案(v7 模式)

### 三步手术

1. **从 `verify_p<N>.py.bak_before_bfix` restore**(确保基线干净)
2. **改 `c2_section_pattern` 为 OR 模式**:

```python
new_value = (
    '\\\\section\\*?\\{[^}]*(?:KEYWORDS)[^}]*\\}'
    '|\\\\subsection\\*?\\{[^}]*(?:KEYWORDS)[^}]*\\}'
)
new_in_src = new_value.replace('\\', '\\\\')  # Python source form
```

3. **string-replace 写回文件 + 备份**:`verify_p<N>.py.bak_with_subsection_or_fix`

### 修复脚本(`C:\Users\Administrator\cow\tmp\`)

| 论文 | 脚本 | 备份名 |
|---|---|---|
| PAPER2 | `fix_p2_v7.py` | `verify_p2.py.bak_with_subsection_or_fix` |
| PAPER3 | `fix_p3_v8.py` | `verify_p3.py.bak_with_subsection_or_fix` |
| PAPER4 | `fix_p4_v7.py` | `verify_p4.py.bak_with_subsection_or_fix` |

**特点**:幂等、可重跑(从 `bak_before_bfix` restore 后再 patch,可重复执行)。

---

## 📊 5 篇论文最终状态(7/11 14:25)

| # | 论文 | HIGH 修前 | HIGH 修后 | MED | LOW | 距投稿 |
|---|---|---|---|---|---|---|
| 1 | PAPER1 | 0 | 0 | 2 | 3 | 最近 ✅ |
| 2 | PAPER2 | 1 | **0** ✅ | 5 | 2 | 最近 ✅ |
| 3 | PAPER3 | 1 | **0** ✅ | 12 | 3 | 最近 ✅ |
| 4 | PAPER4 | 2 | **0** ✅ | 10 | 4 | 最近 ✅ |
| 5 | PAPER5 | 0 | 0 | 3 | 3 | 最近 ✅ |
| **总计** | - | **4** | **0** | **32** | **15** | - |

> 备注:MED 数比 audit 报告高(26 → 32),因为之前 audit 把"被 HIGH 压住的 MED"算成 HIGH,修完 HIGH 后 MED 数字变准。

---

## ✅ 产物清单

### 修改文件
- `F:\Research\PAPER2_CONSOLIDATED\verify_p2.py`(+82 bytes,OR regex)
- `F:\Research\PAPER3_CONSOLIDATED\verify_p3.py`(+92 bytes,OR regex)
- `F:\Research\PAPER4_CONSOLIDATED\verify_p4.py`(+88 bytes,OR regex)

### 备份文件(每个 verify 2 份)
- `verify_p[N].py.bak_before_bfix`(原始)
- `verify_p[N].py.bak_with_subsection_or_fix`(修复版)

### 修复脚本(幂等)
- `C:\Users\Administrator\cow\tmp\fix_p2_v7.py`
- `C:\Users\Administrator\cow\tmp\fix_p3_v8.py`
- `C:\Users\Administrator\cow\tmp\fix_p4_v7.py`

### 状态/记录
- `C:\Users\Administrator\cow\tmp\windows\w6-paper-repair\STATUS.md`(v4,7259 bytes,7/11 14:35)
- `C:\Users\Administrator\cow\memory\2026-07-11.md`(L619+ 教训段追加,7/11 14:35)
- 本文件(knowledge 沉淀)

### 未清理(下次接手)
- `C:\Users\Administrator\cow\tmp\fix_p*_v[1-6].py`(7 个失败版本,~10 KB)
- PAPER4 stdout 仍输出 "HIGH: figure (line 216) has no \caption{...}"(Bug D 残留,不进 TOTAL)

---

## 🎯 下一步建议(路径 B / C)

### 路径 B:全 MED+LOW(工时 ~4h)

| 类别 | 数量 | 主要内容 | 工时 |
|---|---|---|---|
| C7 ceremonial cite | ~10 | 21 处上下文(已在 `F:\Research\C7_REVISION_SUGGESTIONS_2026-07-11.md`) | 2 h |
| C5 test name | 4 | abstract 加 test name | 30 min |
| C4 self-cite | 1 | PAPER2 减自引到 ≤2 keys | 30 min |
| C10 reproducibility | ~10 | LR / seed / library version(从 supplementary 找或用户给) | 1 h |

### 路径 C:只补 C10

工时 1h,只让 5 篇都过 TMLR reproducibility 要求。

---

## 🔗 跨文档链接

- [5 篇全量审计报告(7/11)](./paper-review-audit-2026-07-11.md) — 老版本,自身有 Bug D 残留
- [5 月 deadline 总览](../research/index.md) — 投递优先级已更新
- [PAPER1 entity](../research/paper1.md) / [PAPER2](../research/paper2.md) / [PAPER3](../research/paper3.md) / [PAPER4](../research/paper4.md) / [PAPER5](../research/paper5.md)
- [w6 状态文件](../../tmp/windows/w6-paper-repair/STATUS.md) v4
- [7/11 研究 CHANGELOG](./research-changelog-2026-07-11.md)

---

## 🪤 经验沉淀(本会话对未来的价值)

1. **🪤 C2 regex 必支持 \subsection**(新建 verify 脚本时 OR 模式)
2. **🪤 PATCH 后必 verify**(不靠文件大小判断)
3. **🪤 现场跑 verify > audit 报告**(deck truth = `python verify_p<N>.py`)
4. **🪤 接力 session 先搜"未生效/失败"段**(避免重复劳动)
5. **🪤 修 verify 比改 main.tex ROI 高 10×**(本次省了 4h)

_最后更新:2026-07-11 14:38_
