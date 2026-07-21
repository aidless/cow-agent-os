# Calibration — 校准方法在 LLM 中的应用

_2026-07-11 沉淀。来源:刘泽文研究主线之一(5 篇 CONSOLIDATED 论文)。_

---

## 🎯 定义

**Calibration**(校准)是衡量模型"说出的概率 vs 实际准确率"一致性的方法。

形式化:如果模型说"我有 70% 把握",那么**长期看,模型应该有 70% 的预测是正确的**。

### 核心公式

```
Expected Calibration Error (ECE) =
Σ_b (|accuracy(b) - confidence(b)|) × (n_b / N)

b: confidence bin
accuracy(b): bin b 中模型的真实准确率
confidence(b): bin b 中模型的平均 confidence
```

---

## 📐 常见校准方法

### 1. Temperature Scaling(温度缩放)

最简单有效:
```python
logits = model(x)
scaled_logits = logits / T
probabilities = softmax(scaled_logits)
```
T > 1 → 概率更均匀(underconfident);T < 1 → 更尖锐(overconfident)。

### 2. Platt Scaling

对 logistic regression 输出做 Platt 缩放:
```
P(y=1|x) = 1 / (1 + exp(A*f(x) + B))
```
A、B 通过 validation set 学习。

### 3. Conformal Prediction

给出 **prediction set** 而非 point prediction,保证 coverage:
```
P(Y_true ∈ C(X)) ≥ 1 - α
```
适合 high-stakes 决策。

### 4. Histogram Binning

分箱后重新校准每箱的概率。

### 5. Isotonic Regression

保序回归校准,更灵活但需要更多数据。

---

## 📐 LLM 特有的校准挑战

### Challenge 1:Hallucination 概率校准

LLM "看起来很自信但其实错了" 的概率需要专门校准。

### Challenge 2:Task-specific 校准

同一个 LLM 在不同任务上需要不同校准(数学 vs 创意写作)。

### Challenge 3:分布偏移下的校准

训练分布 vs 测试分布不同时,校准失效。

### Challenge 4:Verifier Capture

校准后的 verifier 可能被串通方攻击(见 [Trust 概念](./trust.md))。

---

## 🪤 与 Agent OS 的对接

### 应用场景

- **PDP 决策校准**(IDEA-B1) —— `allow/deny` 概率校准
- **Verifier 投票加权**(IDEA-B4) —— 用 calibration 决定 verifier 权重
- **Trust rating 校准** —— trust rating 的 calibration error

### 校准可应用位置

```
Cognition Plane(Executor / Verifier)
   ↓
校准前的 output → 校准方法 → 校准后的 probability
   ↓
PDP / Multi-Agent Trust / A2A Verified
```

---

## 🔗 与研究主线接口

- **校准主线** —— 直接就是本研究的核心方法
- **校准 + 偏好耦合** —— 用户偏好对校准目标的影响
- **校准 + 多 Agent** —— Multi-Agent 系统中的 calibration propagation

---

## 📚 已发表/在研的校准工作

- **Guo et al. (2017)** — "On Calibration of Modern Neural Networks"(ECE 普及)
- **Platt (1999)** — Platt Scaling 原始论文
- **Vovk et al. (2005)** — Conformal Prediction 理论
- **Minderer et al. (2021)** — "Revisiting the Calibration of Modern Neural Networks"(LLM 校准)
- **刘泽文 5 篇 CONSOLIDATED 论文** —— 在该领域有 5+ 论文沉淀

---

## 🎓 论文 idea(从 Calibration 出发)

1. **PDP 决策校准**(IDEA-B1) —— 把 ECE 引入 Agent OS 控制平面
2. **Multi-LLM Ensemble 校准**(IDEA-A4 修正版) —— N 个 LLM 校准后聚合
3. **Trust Rating 校准** —— trust score 的 calibration

---

_最后更新:2026-07-11 12:50_
