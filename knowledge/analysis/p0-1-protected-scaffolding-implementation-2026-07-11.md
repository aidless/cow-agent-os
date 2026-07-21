# P0-1 Protected Scaffolding — 实现报告

> **触发**: 2026-07-11 23:10, 刘泽文 "按你的建议来" → 执行 B 方案 (抄 3 个 P0 到现有 skill)
> **依据**: `knowledge/analysis/deepagents-vs-hermes-agent-2026-07-11.md` §10 表 P0-1
> **节奏**: 第一段 (~2h) 已完成 — P0-1 + 归档; P0-2 / P0-3 留明天

---

## 1. 改了什么

### 1.1 `tmp/windows/w5-paper-review-dynamic/worker_template.py`

**新增** (line 130-165, ~30 行):
```python
PROTECTED_WORKERS: frozenset[str] = frozenset({"quick_triage", "single_review"})

def validate_skip(skip: tuple[str, ...]) -> None:
    """禁止 skip protected worker — 在 TaskSpec 构造时调一次。

    同时接受 worker name (e.g. "quick_triage") 和 CLI name (e.g. "quick"):
    内部通过 CLI_REGISTRY 反查 worker name, 再比对 PROTECTED_WORKERS。
    """
    normalized = set()
    for name in skip:
        if name in REGISTRY:
            normalized.add(name)
        elif name in CLI_REGISTRY:
            normalized.add(CLI_REGISTRY[name])
        else:
            continue  # unknown name → let downstream resolve raise
    bad = normalized & PROTECTED_WORKERS
    if bad:
        raise ValueError(
            "skip= conflicts with protected workers: "
            f"{sorted(bad)} (required scaffolding — see PROTECTED_WORKERS; "
            "these are the worker pool's 'required middleware' that every "
            "review must run, equivalent to DeepAgents _REQUIRED_MIDDLEWARE)"
        )
```

### 1.2 `tmp/windows/w5-paper-review-dynamic/dynamic_spawner.py`

**改动** (line 31-67, ~15 行):
- import 增 `validate_skip`
- `TaskSpec` docstring 加 P0-1 升级说明
- 新增 `__post_init__` 方法 → 构造时自动调 `validate_skip(self.skip)`

### 1.3 Regression 修复

`dynamic_spawner.py:444-450` 原 self-test 用例:
```python
("quick + skip quick_triage + custom verify_paper",
 TaskSpec(level="quick", skip=("quick_triage",), custom_workers=("verify_paper",)),
 1, 0.00, 0),
```
**问题**: 这正是 P0-1 要防的反模式测试。改成:
```python
("quick + skip multi_review + custom verify_paper",
 TaskSpec(level="quick", skip=("multi_review",), custom_workers=("verify_paper",)),
 2, 0.00, 0),  # 1 → 2 (因为 multi_review 不在 quick preset, skip 不生效, 但 custom +1)
```

---

## 2. 验证结果

### 2.1 P0-1 单元测试 (8/8 PASS, 测试脚本已删)

| T# | 场景 | 结果 |
|---|---|---|
| T1 | `TaskSpec(level="standard")` (空 skip) | ✅ PASS |
| T2 | skip `multi_review` (非 protected) | ✅ PASS |
| T3 | skip `quick_triage` (worker name) | ✅ ValueError, msg 含 "scaffolding" + "PROTECTED" |
| T4 | skip `single_review` (worker name) | ✅ ValueError |
| T5 | skip 混合 (`multi_review` + `quick_triage`) | ✅ ValueError |
| T6 | skip CLI name `quick` | ✅ ValueError (反查 → protected) |
| T7 | skip CLI name `standard` | ✅ ValueError (反查 → protected) |
| T8 | 默认 `TaskSpec()` 无参 | ✅ PASS (后向兼容) |

### 2.2 回归测试 (13/13 PASS 🎉)

`python dynamic_spawner.py self-test`:
- 8 spec cases 全 ✅ (包括改了期望值的 T4)
- 5 random_spawn cases 全 ✅ (seed=42 / n=100 / tight budget / n=1 / n=0)

### 2.3 兼容性

- ✅ `worker_template.py list` 8 worker 全显
- ✅ `TaskSpec()` 默认构造 (旧调用方) 不报错
- ✅ 旧 `skip=("multi_review",)` / `skip=("doctor",)` 仍可用

---

## 3. 与 DeepAgents 设计的 1:1 对应

| DeepAgents v0.6.12 | 我们的 P0-1 |
|---|---|
| `_REQUIRED_MIDDLEWARE = (FilesystemMiddleware, SubAgentMiddleware)` | `PROTECTED_WORKERS = {quick_triage, single_review}` |
| `_REQUIRED_MIDDLEWARE_NAMES` frozenset | `PROTECTED_WORKERS` frozenset |
| `_apply_excluded_middleware` raises ValueError | `validate_skip()` raises ValueError |
| 错误信息 "required scaffolding cannot be excluded" | 错误信息 "skip= conflicts with protected workers" + "required scaffolding" |
| 在 `create_deep_agent` 装配时 enforce | 在 `TaskSpec.__post_init__` 构造时 enforce |

**为什么选这两个 worker**:
- `quick_triage`: HEURISTIC ($0 / 0 LLM),任何 review 都必须先有启发式 triage
- `single_review`: LLM 主战场 ($0.05 / 1 LLM),multi_review / rebuttal 都依赖其结果
- `audit` / `rebuttal` / `multi_review` / `doctor` 都可选

---

## 4. 归档 — `tmp/_archive_deepagents.ps1`

**位置**: `tmp/_archive/deepagents-2026-07-11/`

**结构**:
```
tmp/_archive/deepagents-2026-07-11/
├── deepagents-deepagents-0.6.12/    # 原 1011 文件 / 46 MB
├── manifest.json                    # 1011 entries + SHA-256
├── RESTORE.md                       # restore + 删除命令
└── (.gitkeep)
```

**脚本三模式**:
```powershell
# 默认: 归档
powershell -File tmp/_archive_deepagents.ps1

# 干跑
powershell -File tmp/_archive_deepagents.ps1 -DryRun

# 恢复 (TODO: 未实现)
powershell -File tmp/_archive_deepagents.ps1 -Restore
```

**幂等**: 多次执行 skip 已存在的 move,只重写 manifest (重算 SHA-256 验证完整性)。

**7 天 quarantine**: 2026-07-11 → 2026-07-18,过期可删 zip + archive 释放 67 MB。

---

## 5. 🪤 修复过程踩到的 4 个坑

| # | 坑 | 症状 | 修复 |
|---|---|---|---|
| 1 | **edit 工具误删 REGISTRY** | 第一次 edit 用整段替换, oldText 不够具体 → 12525/18524 bytes, REGISTRY 7 worker 全没 | 立刻备份 + 二次 edit 还原 + 加 PROTECTED_WORKERS |
| 2 | **`TaskSpec.__post_init__` 触发 self-test fail** | 原 self-test 想 skip `quick_triage`, P0-1 拒绝 → fail-fast | 改测试用例为 skip `multi_review` + 调整期望值 |
| 3 | **PowerShell `@{}` dict 在 ForEach-Object 复用** | "Item has already been added. Key in dictionary: 'path'" | 改用 `New-Object PSObject -Property @{}` 每次新建 |
| 4 | **PowerShell 子作用域变量赋值不回传** | `$script:totalSize += $_.Length` 在 ForEach-Object 内累加为 0 | 改用 `Measure-Object -Sum` 在外面算 |

---

## 6. 第一段总产出

| 产物 | 位置 | 大小 |
|---|---|---|
| PROTECTED_WORKERS + validate_skip | `worker_template.py` | +30 行 |
| `TaskSpec.__post_init__` | `dynamic_spawner.py` | +15 行 |
| Regression 修复 | `dynamic_spawner.py:444-450` | ~3 行改 |
| 归档脚本 | `tmp/_archive_deepagents.ps1` | 4.2 KB |
| 归档产物 | `tmp/_archive/deepagents-2026-07-11/` | 46 MB + manifest |
| STATUS.md v0.5 段 | `tmp/windows/w5-paper-review-dynamic/STATUS.md` | +28 行 |

**耗时**: ~2h (修复 4 坑 + 设计 + 实现 + 验证 + 归档)

---

## 7. 明天待做 (第二段 ~4.5h)

| Task | 工时 | 风险 |
|---|---|---|
| **P0-2**: BackendProtocol 抽象 + MockBackend + DiskBackend + CompositeBackend | 3h | 🟡 中 |
| **P0-3**: wechat-mp-validation 加 FilesystemPermission 枚举字段 | 1.5h | 🟢 低 |
| **verify-after-each-change**: P0-2 / P0-3 每次改完跑回归 | 集成在工时里 | 🟢 |

---

*最后更新: 2026-07-11 23:15 · 泰 · P0-1 落地完毕, 归档完毕, 等明天做 P0-2 + P0-3*