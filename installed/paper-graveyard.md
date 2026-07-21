# paper-graveyard

- **首次记录日**: 2026-07-11
- **来源路径**: `F:\Research\.graveyard\`(本地派生,非 cc-switch 继承)
- **来源 URL**: Derived from `Shubhamsaboo/awesome-llm-apps/agent_skills/project-graveyard`(Apache-2.0)
- **派生方式**: 复用 project-graveyard 的 SKILL.md 骨架 + causes-of-death.md 9 类死因 + ASCII 墓碑卡片 + epitaph 规则,适配到 paper 领域(9 类 paper 死因 + 25 个测试用例)
- **为什么装**: 把 awesome-llm-apps 仓库的高质量 agent skill 移植到论文生命周期管理,与 `paper-changelog` 互补(正交审计 + 反向 autopsy)
- **symlink 路径**: 不需要 — 本地脚本,直接 `python F:\Research\.graveyard\scripts\graveyard.py`
- **卸载步骤**:
  1. `rm -rf F:\Research\.graveyard` (整目录回滚)
  2. `rm C:\Users\Administrator\cow\installed\paper-graveyard.md`

## 使用方式

**单 paper 审计**:
```bash
python F:\Research\.graveyard\scripts\graveyard.py --paper-dir "F:\Research\PAPER1_CONSOLIDATED"
```

**全盘扫描**:
```bash
python F:\Research\.graveyard\scripts\graveyard.py "F:\Research" --days 90
```

**JSON 输出**(给 paper-changelog 联动用):
```bash
python F:\Research\.graveyard\scripts\graveyard.py "F:\Research" --json tmp/paper_graveyard_report.json
python F:\Research\.graveyard\scripts\combine_reports.py \
    --gr tmp/paper_graveyard_report.json \
    --out tmp/paper_dashboard.md
```

**标记复活**:
```bash
python F:\Research\.graveyard\scripts\graveyard.py \
    --state ~/.paper-graveyard.json \
    --mark-resurrected "F:\Research\PAPER3_CONSOLIDATED"
```

## 当前文件

| 文件 | 大小 | 内容 |
|---|---|---|
| `references/causes-of-paper-death.md` | 8.9 KB | 9 类 paper 死因 schema(signal + confidence + resurrection angle) |
| `SKILL.md` | 13.0 KB | skill spec(frontmatter + 13 段,含 ASCII 墓碑卡片 + epitaph 规则) |
| `scripts/graveyard.py` | ~31 KB | scanner + 9 detectors + pulse + state |
| `scripts/combine_reports.py` | ~7 KB | paper-changelog × paper-graveyard 交叉报告 |
| `tests/test_graveyard.py` | ~11 KB | 25 个 unittest(noise filter 5 + detector 14 + pulse 2 + integration 4) |

## 测试状态

✅ **25/25 unittest passed**(`python F:\Research\.graveyard\tests\test_graveyard.py`)
- 5 noise filter 测试(arxiv_id / short_hash / named_hash / non_paper_hints / paper_dir_has_upload)
- 14 detector 测试(sibling_killer × 2 / finished × 2 / experiment_overhead × 2 / rewrite_spiral × 2 / scope_explosion × 2 / slow_fade × 2 / reviewer_killed × 2 / deadline_missed × 2 / autopsy unknown 1)
- 2 pulse 测试(high full draft / low missing everything)
- 4 其他(CLI + integration)

## 与 paper-changelog 的关系

**正交**:
- paper-changelog:正向 audit(静态 status:🟢/🟡/🟠/🔴)
- paper-graveyard:反向 autopsy(动态 death cause)

**联动**:`combine_reports.py` 自动产出 `paper_dashboard.md` + `paper_dashboard.json`,交叉引用 🟠/🔴 × death cause,挑出**高优先级复活候选**。

## 已知限制(v0.2)

- mtime fallback 下 lifespan 估算失真(所有 fallback 都被算成 1 天)— 需要 git log 才行
- noise filter 对真实有 `_NNNN` 后缀命名的论文可能误杀 — 用 `--include-hash` 关闭
- reviewer_killed / deadline_missed 的检测纯靠 commit message 关键字 — 注释风格不同可能漏检

## v0.2 path fix 备注(2026-07-11 11:30+)

- 善后阶段发现 `causes-of-paper-death.md` 在 SKILL.md 承诺的 `references/` 子目录,但实际在根目录 — 已修正为 `references/causes-of-paper-death.md`,跟 project-graveyard 原版 1:1 对齐
- 已同步更新 MEMORY.md / memory/2026-07-11.md / installed/paper-graveyard.md 3 处路径
- 25/25 unittest 重跑全过(0.145s),无回归

## 关联

- `paper-changelog` — 正向 audit,F:\Research 38 个 paper 目录自动盘点
- `arxiv-tracker` — resurrection 计划世界检查(world-check)步骤可调用
- `rr-responder` — reviewer_killed 候选的复活计划可走 4 段 rebuttal pipeline
- awesome-llm-apps deep-dive 知识页: `knowledge/entities/awesome-llm-apps-2026-07-11.md`

## 完整 revert

```bash
rm -rf F:\Research\.graveyard
rm C:\Users\Administrator\cow\installed\paper-graveyard.md
# 同步撤销 installed/README.md 表格 / MEMORY.md 段 / memory/2026-07-11.md 段
```