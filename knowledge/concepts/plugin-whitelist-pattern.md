# Plugin Whitelist Pattern — 可复用的 per-target 配置

_2026-07-11 沉淀。来源:TEMPLATE v0.5.0 `c11_plugins_enabled` 设计 + 实现。_

---

## 🎯 模式定义

**Plugin Whitelist Pattern**(插件白名单模式):一个可复用的设计模式,允许**每个 target(用户/论文/任务/资源)配置一个允许运行的 plugin 子集**,而全局默认是"运行所有 plugin"。

它解决了"如何给一个长尾的 target 收缩功能"的问题。

---

## 📐 模式三要素

| 要素 | 含义 | 典型取值 |
|---|---|---|
| **Whitelist**(`enabled`) | 仅允许这些 plugin | `['plugin-a', 'plugin-b']` |
| **Blacklist**(`disabled`) | 禁止这些 plugin | `['plugin-c']` |
| **Precedence Rule** | 两者冲突时怎么办 | **enabled wins**,warning logged |

---

## 📐 标准实现模板(Python)

```python
def filter_active(plugins, disabled, enabled=None):
    """Filter plugins by whitelist + blacklist with precedence."""
    enabled_set = set(enabled) if enabled else set()
    disabled_set = set(disabled) if disabled else set()

    # Precedence rule: enabled wins, disabled ignored (with warning)
    if enabled_set:
        if disabled_set:
            log.warning("enabled+disabled both set; enabled wins")
        return {n: c for n, c in plugins.items() if n in enabled_set}

    # Only blacklist (legacy behavior)
    if disabled_set:
        return {n: c for n, c in plugins.items() if n not in disabled_set}

    # No filter → all plugins
    return dict(plugins)
```

---

## 🎯 模式的 4 个使用场景

### 场景 1:Per-paper 锁定(像 tmaudit)

**问题**:某篇论文只想跑特定 plugin(避免 noise)。
**解法**:`paper_configs['paper-5']['c11_plugins_enabled'] = ['flag-todo-markers']`

### 场景 2:Per-user 权限(类比)

**问题**:新用户不应该触发 destructive plugin。
**解法**:`user_policy['newbie']['enabled'] = ['read-only-plugins']`

### 场景 3:Per-task 安全(类比 Agent OS)

**问题**:某些任务风险高,只允许白名单 plugin 跑。
**解法**:`task_policy['payment']['enabled'] = ['audit', 'compliance-check']`

### 场景 4:Per-tenant 隔离(类比 SaaS)

**问题**:不同租户允许的 plugin 不同。
**解法**:`tenant_policy['enterprise']['enabled'] = ['basic', 'audit', 'compliance']`

---

## 🪤 模式的常见反模式(Anti-patterns)

### 反模式 1:只有 Blacklist,没有 Whitelist

```python
# ❌ 只能禁止,不能锁定
def filter_active(plugins, disabled):
    return {n: c for n, c in plugins.items() if n not in (disabled or [])}
```

**问题**:如果某 target 想"只跑这 1 个 plugin",必须列出"所有其他 plugin 都禁止"——不可维护。

### 反模式 2:Intersection(交集)

```python
# ❌ 两者都生效,取交集
def filter_active(plugins, disabled, enabled):
    return {n: c for n, c in plugins.items()
            if n in (enabled or plugins) and n not in (disabled or [])}
```

**问题**:语义模糊 —— "既在白名单又在黑名单" 怎么办?警告?忽略?报错?

**正解**:**Precedence Rule 明确单一来源**(enabled wins)。

### 反模式 3:无 fallback

```python
# ❌ 没设 enabled 时,反而报错
def filter_active(plugins, disabled, enabled):
    if enabled is None:
        raise ValueError("enabled must be set")
```

**问题**:破坏 backward-compat。

**正解**:`enabled=None` 表示"无 whitelist,fall through 到 disabled 检查"。

---

## 🪤 与 Agent OS 方案的对接

| Agent OS 概念 | Plugin Whitelist 映射 |
|---|---|
| **Per-task Permission** | `task_spec['permissions_required']` |
| **PEP hook 8 个** | `task_spec['tools_allowed']` |
| **Risk Level × TTL** | `task_spec['risk_class']` 决定默认 whitelist |
| **Trust Level T0-T4** | `user_profile['trust_level']` 决定默认 blacklist |

### 实际应用示例

```python
# Agent OS 任务执行前:
allowed_plugins = filter_active(
    plugins=all_audit_plugins,
    disabled=user_profile['disabled_plugins'],
    enabled=task_spec.get('plugins_enabled')  # 任务级可选
)
```

---

## 📐 8 条设计启发

来自 TEMPLATE v0.5.0 实战经验:

1. **默认 fallback 友好**:`enabled=None` 不报错,允许"只设置 blacklist"的 legacy 行为
2. **Precedence 必须明确**:不要交集,不要 fallback,选一个单一来源
3. **冲突时 warning log**:enabled+disabled 同时设置时**警告**(用户应该知道自己的 config 有歧义)
4. **未知名字 silently dropped**:whitelist 包含不存在的 plugin 不报错,只是不生效
5. **测试覆盖 4 种组合**:empty/blacklist-only/whitelist-only/both
6. **Meta-test 覆盖 precedence swap**:专门写 inject 把顺序颠倒,验证测试 catch
7. **文档说明 precedence 一句话**:`enabled wins, disabled ignored (with warning)`
8. **Backwards-compat 是底线**:v0.5.0 加 whitelist 时,v0.4.0 调用方式继续工作

---

## 🔗 与研究主线对接

- **校准主线**:whitelist 的"准确性"——用户设的 enabled 是否反映真正想要的 plugin 集合?(calibration error)
- **偏好耦合主线**:不同用户的 whitelist 偏好如何学习?(RLHF/DPO)
- **多 Agent 协作主线**:多个 agent 协作时,如何合并各自的 plugin 偏好?(类似 ensemble)

---

## 📚 参考来源

- **TEMPLATE v0.5.0 release**:`F:\Research\TEMPLATE\RELEASE_NOTES_v0.5.0.md`
- **V050_PLAN.md §16.4**(precedence rule)
- **`_check_all_regressions.py` Bug 15 + 16**(meta-test 验证)
- **Agent OS 完整方案** §3.3(Cedar-like policy)
- **本知识库**:[Multi-Agent 协作](./multi-agent-collaboration.md)

---

## 🎓 论文 idea

1. **Whitelist Calibration**:用户偏好 vs whitelist 准确性的 ECE 测量
2. **Precedence Rule Robustness**:不同 precedence 设计(enabled wins vs intersection vs merge)对系统鲁棒性的影响
3. **Plugin Discovery vs Lock-down Trade-off**:开放 plugin 生态 vs 严格 whitelist 的设计平衡

---

_最后更新:2026-07-11 13:40_