# Differential Privacy — 在 Agent OS 数据收集中的应用

_2026-07-11 沉淀。来源:Agent OS V3+V5 数据分级与 DP 演化机制。_

---

## 🎯 定义

**Differential Privacy (DP)** 提供数学上严格的隐私保证:

> 一条记录的加入或移除,不会显著影响算法的输出。

形式化:
```
Pr[M(D) ∈ S] ≤ e^ε × Pr[M(D') ∈ S] + δ
```

- ε (epsilon): 隐私损失上界,**越小越隐私**
- δ (delta): 失败的概率上界,通常取 10^-6 或更小
- D vs D': 相邻数据集(差一条记录)

---

## 📐 Agent OS 中的 DP 应用

### D0-D5 数据分级

| 级别 | 名称 | 全局学习 | DP 处理 |
|---|---|---|---|
| D0 | Public | ✅ | 不需要 |
| D1 | Product Telemetry | ✅ | DP 聚合 |
| D2 | Derived Metadata | ✅ | DP + k-anonymity |
| D3 | User Content | ❌ 默认 | 用户授权 + DP |
| D4 | Sensitive Content | ❌ | 只能本地,不上传 |
| D5 | Regulated Content | ❌ | 专门合规协议 |

### 适合 DP 的数据

- 工具调用成功率
- 任务失败率
- Agent 评分分布
- 错误类别频率
- planner 策略收益
- A2A 调用成功率
- 任务耗时分布

### 不适合 DP 的数据

- 长文本原文
- 源码
- 对话内容
- 用户私有记忆

> DP 适合**聚合统计**,**不适合**直接保护长文本。

---

## 📐 DP 标准参数(Agent OS V3)

```json
{
  "metric": "tool_success_rate",
  "group": "browser_automation.login_flow",
  "count_min_k": 50,
  "epsilon": 1.0,
  "delta": 0.000001,
  "contribution_limit_per_user": 5,
  "noise": "laplace_or_gaussian"
}
```

### 参数含义

- `epsilon = 1.0`: 中等隐私预算(强 = 0.1, 弱 = 10)
- `delta = 10^-6`: (ε, δ)-DP 标准上界
- `count_min_k = 50`: 样本 < 50 不发布(threshold release)
- `contribution_limit = 5`: 单用户每日最多贡献 5 次

---

## 📐 4 阶段诚实演进(Agent OS V5)

```
V1: Centralized Telemetry Hygiene
   服务端可见明文 D1/D2 + 数据分级 + contribution limit + k 阈值 + DP 发布
   → 正式名称:privacy hygiene + controlled telemetry
   → 不是 secure aggregation

V2: Tenant-Isolated Encrypted Transport
   传输加密 + 租户隔离,但聚合服务仍可见明文
   → 仍不是 secure aggregation

V3: TEE-backed Aggregation / Threshold Secure Aggregation
   服务端运维不可见单用户明文
   → 才是 privacy-preserving aggregation

V4: Federated Analytics / Federated Learning
   数据尽量留本地,只上加密/聚合/裁剪后更新
```

**硬规则**:V1/V2 不声称 secure aggregation,只是过渡期隐私卫生。

---

## 📐 流式 DP 管道(Agent OS V4)

```
Client
  ↓ local clipping + local event encoding
Telemetry Gateway
  ↓ validation + tenant isolation
Streaming Aggregator
  ↓ windowed aggregation
Contribution Bounding Service
  ↓ per-user/per-tenant clipping
Secure Aggregation Layer(V3+)
  ↓ threshold aggregation / encrypted aggregation
DP Noise Service
  ↓ add calibrated noise
Metrics Store
  ↓ publish only aggregate metrics
```

### 关键并发原语

- **windowed aggregation**: 按时间窗口
- **contribution bounding**: 限制单用户贡献
- **idempotency key**: 避免重复上报
- **secure aggregation**: 服务端不可见单用户明文(V3+)
- **threshold release**: 样本 < k 不发布
- **privacy budget ledger**: epsilon 消耗追踪

---

## 🪤 DP 在 Agent OS 中的常见漏洞

### 漏洞 1:DP 组合失效(High)

多次 DP 查询的组合下,隐私预算可能耗尽。

**缓解**:
- Privacy Budget Ledger(总 epsilon 消耗记账)
- 查询相关性检查
- Limited Query API

### 漏洞 2:DP 不适合长文本

试图用 DP 保护长文本原文 → 噪声爆炸 → 文本不可用。

**缓解**:
- 接受 DP 只适合聚合
- 长文本走本地学习 + 用户授权

### 漏洞 3:贡献限制可绕过

同一用户用不同 user_id 重复提交 → 污染分布。

**缓解**:
- 跨 ID linking(基于 IP/设备指纹)
- 强制 SSO

---

## 🔗 与研究主线接口

- **隐私 ML 主线**: DP 是核心工具
- **校准主线**: DP 噪声下 calibration 的偏差-方差权衡
- **多 Agent 主线**: Federated planner 演化需要 DP

---

## 📚 经典 DP 论文

- **Dwork & Roth (2014)** — The Algorithmic Foundations of DP(DP 圣经)
- **Dwork et al. (2010)** — Boosting and Differential Privacy
- **Abadi et al. (2016)** — Deep Learning with DP(DP-SGD)
- **McMahan et al. (2018)** — Federated Learning with DP
- **Apple Differential Privacy**(2017) — 工业界实施

---

## 🎓 论文 idea(从 DP 出发)

1. **Streaming DP Composition in A2A**(IDEA-A6) — NeurIPS Privacy in ML
2. **DP 噪声下 Agent 演化质量**(IDEA-B5) — TMLR
3. **Privacy Budget Ledger 的最优分配** — 多 metric 共享 epsilon

---

_最后更新:2026-07-11 12:50_
