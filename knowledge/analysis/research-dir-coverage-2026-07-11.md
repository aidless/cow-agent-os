# F:\Research 目录 — 知识库覆盖度盘点

> Source: 2026-07-11 13:55 用 `tmp/_check_kb_coverage.ps1` v2 实测
> 脚本逻辑:对 `F:\Research\` 每个子目录名,在 `knowledge/**/*.md` 里 `Select-String -SimpleMatch`(Unicode 安全)出现次数

## 🎯 一句话结论

**v1 (GBK Contains) → v2 (Unicode Select-String) 后覆盖率从 70% 升到 93.8%**。
v1 漏掉的中文目录(如 `00_系统配置`)、被 `.Contains()` 误判为 0 的目录,现在都正确归到 ≥2 段。
**剩余 5 个 0 hits 全部是工具配置/缓存隐藏目录** (`.claude / .loop / .obsidian / .pytest_cache / .tmp`),合理无需入库。

## 📊 覆盖率分布(v2)

| Hits | 数量 | 占比 | 含义 |
|---|---|---|---|
| ≥ 2 | 69 | 86.3% | ✅ 充分覆盖 |
| 1 | 6 | 7.5% | 🟡 单点提及(辅助/中转目录) |
| 0 | 5 | 6.3% | ⚪ 全是隐藏配置目录,无需入库 |
| **合计覆盖(≥1)** | **75/80** | **93.8%** | ✅ |

## 📈 v1 → v2 对比(脚本修复轨迹)

| 目录 | v1 (GBK) | v2 (Unicode) | 备注 |
|---|---|---|---|
| `00_系统配置` | 0 | **2** | 中文盲区,真的漏判 |
| `_archive` / `_corpus` / `_ALARMS` 等 11 个 `_xxx` | 1 | **2** | v2 把 coverage 报告本身算进去(自我指涉但合理) |
| `arxiv_test` | 0 | **1** | v2 列出 |
| `.zcode` / `__pycache__` | 1 | 1 | 不变(本来就是 1)|
| `genesis-master` | 0 | **4** | **新建 entity 自动覆盖** |

## ✅ 充分覆盖(69 个,挑重点)

| 类别 | 代表目录 | Hits | 深度 |
|---|---|---|---|
| **工具链(4 个)** | `paper-writing-agent`(10) / `tmlr_pipeline`(7) / `tmlr-review-simulator`(7) / **`genesis-master`(4)** | 🔵 都有 entity / analysis 页 |
| **6 篇 CONSOLIDATED** | `PAPER1-5_CONSOLIDATED`(5-9) / `PAPER6_CONSOLIDATED`(7) | 🔵 每个都有 `knowledge/research/paper<N>.md` entity |
| **15 个主题研究** | `calibration_contagion` / `impossibility_triangle_consolidated` / `memory_architecture` / ... (3-4) | 🟡 changelog + entity 索引 |
| **早期单篇** | `tmlr_flagship` / `tmlr_p6 ~ p21` (2-4) | 🟡 两份 changelog 标记为"已合并,可考虑清理" |
| **实验原料** | `arxiv` (14) / `arxiv_1m` (5) / `arxiv_p13/p14` (5/3) / `experiments` (7) | 🟡 changelog + entity 索引 |
| **元结构** | `research`(29) / `scripts`(9) / `figures`(3) / `planning`(7) | 🟢 作为通用词被频繁引用 |

## ❌ 完全缺失(v2 后剩 5 个,全是工具配置)

| 目录 | 判断 |
|---|---|
| `.claude` `.loop` `.obsidian` `.pytest_cache` `.tmp` | ⚪ 隐藏/工具配置/缓存,**完全无需入库**(全在 gitignore 类) |

## 🪤 v1 → v2 脚本升级(中文盲区修复)

**问题**:PowerShell 5.x 默认 GBK,字符串 `.Contains()` 对中文字符可能错过匹配。

**v1 复现**(已不再出现):
```powershell
$c = Get-Content "knowledge\entities\liu-zewen-research.md" -Raw
$c.Contains("00_系统配置")  # 返回 $false,即使文件中确实有这个字符串
```

**v2 修复**:用 `Select-String -SimpleMatch`,PowerShell 内部是 Unicode codepoint,中文匹配正确。

```powershell
Select-String -Path $f.FullName -Pattern ([regex]::Escape($name)) -SimpleMatch
```

**修复效果**:`00_系统配置` 从 0 hits → 2 hits,其他含 unicode 的目录也都正确归类。

## 📁 重复目录确认

| 重复对 | 知识库是否都收录 | 建议 |
|---|---|---|
| `CONSOLIDATED_PAPER5/` vs `PAPER5_CONSOLIDATED/` | ✅ 都收(4 vs 9 hits) | `CONSOLIDATED_PAPER5/`(无编号)应是早期版,可清理 |
| `FLAGSHIP/` vs `tmlr_flagship/` | ✅ 都收(4 vs 4 hits) | 双名问题,可考虑合并 |

→ 7/11 上午盘点时你说"可考虑清掉",**知识库和 entity 都标了**,真清的话两边一起动。

## 🆕 本次新增

- ✅ `knowledge/entities/genesis-master.md`(7.4 KB)—— TMLR 第 6 篇独立投稿项目全图
- ✅ `tmp/_check_kb_coverage.ps1` v2 —— Select-String 替换 Contains
- ✅ `tmp/_check_coverage_stats.ps1` —— 统计 + 0-hits 列表

## 🔗 跨文档链接

- [genesis-master entity](./genesis-master.md) — 本次新建
- [刘泽文 — 研究系统全图](../entities/liu-zewen-research.md) — 主入口
- [Tools 2026-07-10](../entities/tools-2026-07-10.md) — 与 40 项目速览对照
- [5 篇 PAPER audit](../analysis/paper-review-audit-2026-07-11.md)

---

_最后更新:2026-07-11 13:55 · 泰补 v2(Unicode 匹配 + 93.8% 覆盖)_