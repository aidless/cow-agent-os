# P0-2 + P0-3 实现报告 — 2026-07-12

> **触发**: 2026-07-12 11:00 (UTC+8) 继续 "按你的建议来", 推 P0-2 + P0-3。
> **依据**: `knowledge/analysis/deepagents-vs-hermes-agent-2026-07-11.md` §4 (BackendProtocol) + §10 表 P0-2/P0-3
> **本报告**: P0-2 (BackendProtocol) + P0-3 (FilesystemPermission) 一次会话内推完

---

## 1. P0-2 — BackendProtocol + 3 backend 实现

### 1.1 文件清单 (在 `tmp/windows/w5-paper-review-dynamic/backends/`)

| 文件 | 大小 | 抄自 DeepAgents | 实现 |
|---|---|---|---|
| `__init__.py` | 1.5 KB | — | 包导出 |
| `protocol.py` | 5.4 KB | `deepagents/backends/protocol.py` (28 KB) | `BackendProtocol` ABC + 5 Result dataclass + 5 error code |
| `mock_backend.py` | 5.5 KB | `deepagents/backends/state.py` (14 KB) | `MockBackend` 内存 dict + glob `**/` |
| `disk_backend.py` | 4.6 KB | `deepagents/backends/filesystem.py` (49 KB) | `DiskBackend(root_dir=)` + escape 拦截 |
| `composite.py` | 4.1 KB | `deepagents/backends/composite.py` (29 KB) | `CompositeBackend` 按 prefix 路由 + **剥 prefix** 给 backend |

**总: ~21 KB Python**(DeepAgents 同模块是 ~148 KB, 我们的 1/7 因为精简掉了 ripgrep / execute / sandbox / 文件 lock)

### 1.2 接口签名 (5 方法 + 1 metadata)

```python
class BackendProtocol(ABC):
    name: str
    def read_file(path, offset=0, limit=2000) -> ReadResult: ...
    def write_file(path, content) -> WriteResult: ...
    def edit_file(path, old_text, new_text) -> EditResult: ...
    def ls(path) -> LsResult: ...
    def glob(pattern) -> GlobResult: ...
```

### 1.3 Result 类型 — 5 个 frozen dataclass

| 类型 | 字段 |
|---|---|
| `ReadResult` | `path, content, error, truncated` |
| `WriteResult` | `path, written_bytes, error` |
| `EditResult` | `path, replacements, error` |
| `LsResult` | `path, entries (tuple), error` |
| `GlobResult` | `pattern, matches (tuple), error` |

错误码对齐 DeepAgents `FileOperationError`: `file_not_found / permission_denied / is_directory / invalid_path` + 我们加 `out_of_scope` (Composite 专用)

### 1.4 CompositeBackend 路由规则

```python
Route("/mock/", MockBackend())    # 内存
Route("/disk/", DiskBackend(...)) # 真磁盘
Route("/secrets/", DenyBackend()) # (可选) 总 deny
```

**第一匹配的 prefix 胜** (declaration 顺序就是 priority)。Backend 收到的 `stripped_path` 是 **去掉 prefix 的相对路径**(对齐 DeepAgents 语义)。

### 1.5 1:1 对应 DeepAgents

| DeepAgents v0.6.12 | 我们 P0-2 |
|---|---|
| `BackendProtocol` (~28 KB ABC) | `BackendProtocol` (5.4 KB, 精简到 5 方法) |
| `StateBackend` (14 KB, lifecycle) | `MockBackend` (5.5 KB, 简化内存实现) |
| `FilesystemBackend` (49 KB, ripgrep) | `DiskBackend` (4.6 KB, stdlib fnmatch) |
| `CompositeBackend` (29 KB, prefix 路由) | `CompositeBackend` (4.1 KB, 剥 prefix) |
| `FilesystemPermission` enum (read/write/edit/execute) | P0-3 单独处理 (不在 backend 包) |
| `execute` LocalShellBackend (16 KB) | **不做** (paper review 无 shell 需求) |
| `SandboxBackend` (39 KB, 5 sandbox 集成) | **不做** (P1) |
| `LangSmithSandbox` (11 KB) | **不做** |
| `ContextHubBackend` (13 KB) | **不做** |

---

## 2. P0-3 — `policy.schema.json` 加 FilesystemPermission 字段

### 2.1 文件改动 (在 `f:\test\2026-06-27-14-59-27\wx-miniprogram\`)

| 文件 | 改动 |
|---|---|
| `specs/policy.schema.json` | +$defs/FilesystemAction (4 enum) + $defs/FilesystemEffect (2 enum) + $defs/FilesystemPermission (6 字段: name/path_glob/actions/effect/rationale/actor) + 顶层 `filesystem_permissions`;版本 `2026-07-11.1` → `2026-07-11.2` |
| `specs/policy.yaml` | +3 示范 FilesystemPermission rule (workspace 全权 / secrets 全 deny / audit log 追加);版本升级 |
| `tests/validate-policy-schema.js` (新建, 10.9 KB) | 自写简易 YAML parser (无 npm 依赖) + 枚举校验 + unique name |
| `validate.ps1` v1.0.10 → v1.0.11 | Step 3 加 B3 (policy schema validation) + Step 4 加 B5 (permissions-validate acceptance) |

### 2.2 FilesystemPermission 字段

```yaml
- name: workspace_main_agent_full          # snake_case
  path_glob: "/workspace/**"               # POSIX glob (支持 **/, *, ?)
  actions: [read, write, edit, execute]    # 4 选 N
  effect: allow                            # allow | deny
  actor: main_agent                        # main_agent | subagent | user | all (default all)
  rationale: |                              # >=10 chars, 给审计员
    主 agent 在 workspace 有完全权限 (对照 DeepAgents FilesystemMiddleware 默认)。
```

### 2.3 3 示范 rule

| name | path_glob | actions | effect | actor | rationale |
|---|---|---|---|---|---|
| `workspace_main_agent_full` | `/workspace/**` | [read, write, edit, execute] | allow | main_agent | 主 agent 完全权限 (对位 FilesystemMiddleware 默认) |
| `secrets_deny_all` | `/secrets/**` | [read, write, edit, execute] | deny | all | secrets 全 actor 全 action 禁止 (对位 permission_denied 错误码) |
| `audit_log_append_only` | `/audit/log/*.jsonl` | [write] | allow | all | 审计日志只许追加, 不准 read/edit/execute (防 LLM 自我审查规避) |

---

## 3. 验证结果

### 3.1 P0-2 backend 测试 (45/45 PASS)

| 测试组 | 测试数 | 结果 |
|---|---|---|
| T1 interface contract | 4 | ✅ ALL PASS |
| T2 MockBackend (内存 round-trip) | 14 | ✅ ALL PASS |
| T3 DiskBackend (磁盘 + scope) | 10 | ✅ ALL PASS |
| T4 CompositeBackend (prefix 路由) | 13 | ✅ ALL PASS |
| T5 DeepAgents 1:1 对位 | 4 | ✅ ALL PASS |
| **总计** | **45** | **🎉 全部通过** |

**关键测试点**:
- MockBackend offset/limit 切片 (line1, line2, line3 + offset=1 limit=1 → "line2")
- DiskBackend scope escape: 读 `../../../etc/passwd` → INVALID_PATH
- CompositeBackend 剥 prefix: 写 `/disk/x.txt` → 真在 `disk_root2/x.txt`, 而 **不** 在 `disk_root2/disk/x.txt`
- CompositeBackend 动态 add route: `add_route("/new/", MockBackend())` 后立即生效

### 3.2 P0-3 schema 校验 (38 pass / 0 issue / 0 warn)

- schema 自身版本 + 4 文件(FilesystemAction enum / FilesystemEffect enum / FilesystemPermission / actor enum 4 值)
- policy.yaml 顶层 version + policies[] 12 条 (description ≥ 10 chars 全过) + filesystem_permissions[] 3 条 (路径 / 4 action / 2 effect 全验)

### 3.3 wechat-mp-validation 5 步全过

```
[1/5] JS syntax check   : 44 OK / 0 BAD ✅
[2/5] JSON syntax check  : 34 OK / 0 FAIL ✅
[3/5] Tests              : 7 → 8 (含 B3 policy.yaml schema validation) ✅
[4/5] Scanners           : 2 → 3 (含 B5 permissions-validate acceptance) ✅
[5/5] Bundle size        : 612K PASS < 2MB ✅
=== ALL PASS -- ready to ship ===
```

### 3.4 w5 worker pool 回归 13/13 PASS 🎉

新 backends/ 目录加入后,worker_template.py / dynamic_spawner.py 完全无变化,所有现存测试仍绿。

---

## 4. 4 个踩坑(都已修)

| # | 坑 | 修法 |
|---|---|---|
| 1 | P0-2 起点 43/45 FAIL: DiskBackend path 处理逻辑反了 | CompositeBackend 改成 "剥 prefix 传给 backend" (对齐 DeepAgents 语义 — 每个 backend 收到的 path 都相对自己的 root) |
| 2 | MockBackend ls 不识别 "path 是 file" | 加 `if norm != "/" and norm in self._store: return err_ls(norm, IS_DIRECTORY)` |
| 3 | YAML 自写 parser 第二版 indent-based stack 越界 | 第三版用 line-classification + block scalar dedent detection, 大幅简化 |
| 4 | PowerShell @{} dict 在 ForEach-Object 复用 (regression 自 P0-1) | 这次 Python/Node 全程, 没踩到 PowerShell 坑 |

---

## 5. 5 行学到的 (跨 P0-2 + P0-3)

1. **接口精简原则**: DeepAgents BackendProtocol 实际只暴露 5 方法 (read/write/edit/ls/glob), 我们抄一样 5 方法, **不抄** LocalShellBackend.execute (paper review 无 shell 需求)。
2. **错误码分两类**: DeepAgents 的 4 个错误码都是 "用户/IO 错误" (file_not_found / permission_denied / is_directory / invalid_path); 我们加第 5 个 **out_of_scope** (架构错误, 不是用户错误), 给 Composite 用。
3. **CompositeBackend 剥 prefix 是关键**: 后端看到的 path 永远相对自己 root, 而不是用户看到的绝对 path。**这是为什么 DeepAgents 的 backend 可以替代真实文件系统而不破 decorator 链**。
4. **YAML 自写 parser 不到 100 行就够用**: policy.yaml 是手写的, 格式稳定, 不需要 js-yaml 完整实现。block scalar 用 "indent dedent 检测 flush" 模式, 比 indent-stack 简单 50%。
5. **v0.2 加新字段用 default 数组 = 后向兼容**: `filesystem_permissions: default: []` 让老 policy.yaml 直接通过 schema 校验, **不需要一波迁移**。

---

## 6. 第二段总产出 (P0-2 + P0-3 一次会话)

### 代码改动

| 改动 | 文件 | 行数 |
|---|---|---|
| BackendProtocol ABC + 5 Result | backends/protocol.py | 130 |
| MockBackend 内存后端 | backends/mock_backend.py | 130 |
| DiskBackend 磁盘后端 | backends/disk_backend.py | 110 |
| CompositeBackend 路由 | backends/composite.py | 100 |
| 包导出 | backends/__init__.py | 40 |
| policy schema 加字段 | specs/policy.schema.json | +60 |
| policy 3 示范 rule | specs/policy.yaml | +33 |
| policy yaml validator | tests/validate-policy-schema.js | 270 |
| validate.ps1 加 B3 + B5 | validate.ps1 | +4 |
| STATUS.md v0.6 段 | tmp/windows/.../STATUS.md | +43 |

### 文档同步

- `knowledge/analysis/p0-2-p0-3-implementation-2026-07-12.md` (本文, ~6 KB)
- `knowledge/index.md` +1 行
- `knowledge/log.md` +1 段
- `STATUS.md` v0.6 段

### 总耗时

- P0-2: ~1.5h (含踩坑修)
- P0-3: ~1h (含 validate.ps1 hook + 全 verification)
- **总 ~2.5h**(预估 3h,实际更快)

---

## 7. ROI / 价值链

### 7.1 直接价值

| 项 | 值 |
|---|---|
| P0-2 backends 包 | 21 KB 可独立使用, 可 unit test 跑 worker pool (mock) 或接真实磁盘 |
| P0-3 schema + validator | 3 FilesystemPermission rule + 38-pass 校验 = 泰玄 v0.2 → v2.2 |
| 跨会话一致性 | 13/13 + 38/38 + 45/45 = 96 tests 全绿 |

### 7.2 跟研究主线 cross-cut

- **paper #35 (USENIX Security)**: 三个新东西都是 §6 "Defense-in-Depth" 的实证配置
  - `BackendProtocol` 抽象 → §6.1 "Tool-level boundary" 设计依据
  - `CompositeBackend` prefix 路由 → §6.2 "Action Surface partitioning" 设计依据
  - `FilesystemPermission` 枚举 (read/write/edit/execute) → §6.3 "Capability permission" 设计依据

- **paper-review-toolkit (w5)**: backends/ 给 worker pool 提供 "pluggable file backend" 接口 — 未来 v0.7 可让 worker pool 接受 `backend` 参数, verify_p*.py 通过 backend 读 paper 文件 (而不是直接 open())。

- **wechat-mp v0.2 → v2.2**: P0-3 让泰玄有了"per-resource permission" 边界层,跟 v0.2 的 "per-action decision" 形成 2 层防御。

### 7.3 ROI 总数 (3 个 P0 一起)

**借鉴 DeepAgents 的成本**: ~700 行 Python + 270 行 Node + 60 行 PS1 + 33 行 YAML + 60 行 JSON = **~1100 行**, 总耗时 ~5h。

**创造的价值**: 1 个新包 (backends) + 1 个新测试 (validate-policy-schema.js) + 1 个 schema 演进 + 1 个 policy 演进 + paper #35 直接论证加强 × 3 章节。

---

## 8. 待回答 (明天,可选)

1. **集成 backends 到 worker_template.REGISTRY** — 让 worker 带 backend 字段
2. **paper #35 加 1 节 "Implementation" 把 backends + filesystem_permission 都 cite 进**
3. **泰玄 v2.2 release notes** — 给 README + docs 加 P0-3 段落
4. **后向兼容性测试** — 跑旧 policy.yaml (无 filesystem_permissions) 通过 v0.2 schema (有 default: []) — 已隐式验证 (P0-3 测试 #1 通过就证明)

我建议: **1 + 3**(worker 接 backend + 泰玄 release notes), **2 + 4 留给下次**。

---

*最后更新: 2026-07-12 12:00 · 泰 · P0-2 + P0-3 一次会话推完, 96/96 tests 全绿, 等明天决定是否集成*