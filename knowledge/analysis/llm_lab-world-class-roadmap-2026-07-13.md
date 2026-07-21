# llm_lab 世界级影响力推进计划

_2026-07-13 凌晨整理。基于公开战略框架 + 刘泽文实际项目状态(100% 测试 / ruff + mypy / API→Runner 分层 / Langfuse)定制。_

## 一句话目标

**18 个月内把 llm_lab 从"个人高质量项目"推到"CNCF 孵化级 / 5K+ Star / 10+ 企业采用者"**。

## 当前状态(2026-07-13)

| 维度 | 现状 |
|---|---|
| 测试覆盖 | 100% / 337+ 测试 |
| 静态检查 | ruff + mypy 全绿 |
| 架构 | API → Runner → Provider/Verifier/Tracer/DB |
| 可观测性 | Langfuse + SQLite tracer 回退 |
| 部署 | Dockerfile + docker-compose |
| CI | pre-commit hooks |
| License | MIT(待确认) |
| Star | 0(假设刚开源) |

## 18 个月路线图

| 阶段 | 月份 | 工作量 | 核心动作 | Star 目标 |
|---|---|---:|---|---|
| **一 · 基础** | 1-3 | 52h | 治理文件 + CI + 性能基准 + 视频 + v1.0.0 | 200+ |
| **二 · 社区** | 4-6 | 38h | Discord + 月度会议 + 5 外部贡献者 + 3 博客 | 1000+ |
| **三 · 生态** | 7-12 | 91h | Plugin Registry + 云服务 Beta + 会议演讲 + CNCF Sandbox | 5000+ |
| **四 · 认证** | 13-18 | 28h+ | 团队扩展 + CNCF 孵化 + 安全审计 | 10000+ |

**总工时 ~209h**(1 人 18 个月 ≈ 4-5h/周,可执行)

## 商业化:Open Core + 云服务

| 组件 | 免费/收费 |
|---|---|
| 核心代码 / 插件 / 模板 | 免费(Apache 2.0)|
| 托管云服务 / 企业版 / 培训 | 收费 |

**18 个月 MRR 预测**:$120K = **$1.44M ARR**(保守)

## 阶段一细节(立刻可启动)

### Month 1:治理 + 文档(22h)

- GOVERNANCE.md / CONTRIBUTING.md / CODEOWNERS / ADOPTERS.md
- CHANGELOG.md / CODE_OF_CONDUCT.md / SECURITY.md
- .github/ISSUE_TEMPLATE + PULL_REQUEST_TEMPLATE
- README 重写(1 分钟快速开始 + GIF)
- ADR-001(为什么用同步 Runner + ThreadPool)

### Month 2:CI/CD + 性能基准(15.5h)

- GitHub Actions:lint + test + type-check + coverage
- SemVer tag 自动发布
- Docker image 自动构建
- 性能基准脚本(100 steps 延迟 / 内存 / 吞吐)
- docs/PERFORMANCE.md

### Month 3:视频 + v1.0.0(15h)

- 5 分钟"5 分钟跑通"视频
- 故障注入视频(OpenAI 断网 / Langfuse 宕机)
- v1.0.0 正式发布
- "从 0 到 v1.0"博客
- HN / Reddit / Twitter 发布

## 立即可做的 3 件事

1. **写 ADR-001**(同步 Runner + ThreadPool 的架构决策)
2. **录 30 秒视频**(terminal 跑 + 报告生成)
3. **发 HN**(标题:"100% test-covered LLM evaluation framework")

## 关键风险

| 风险 | 概率 | 缓解 |
|---|---|---|
| 社区不活跃 | 高 | 第一年主动找 10 人 PR |
| LLM 评估太卷 | 高 | 差异化:可审计 + 离线 + 合规 |
| 时间不够 | 中 | 阶段一最小化 |
| 被大厂抄 | 中 | 提前建社区护城河 |
| 企业采用慢 | 高 | 第一年 toC,第二年 toB |

## 5 条具体建议

1. 先把阶段一 12 个文件做出来(1 周 22h)
2. v1.0.0 标签一定要打(心理告别个人项目)
3. 第一个视频就用清晰直接的风格
4. CNCF Sandbox 不是目标是手段
5. 找 3 个导师(LLM 评估 / 开源治理 / 商业化 各 1 个)

## 触发条件

**今晚不启动**。**下次精力足时启动阶段一 Month 1**(22h)。

**触发启动**:
- taixuan-web v1.2 ECS 部署完
- PAPER5 投递完一轮
- 有连续 3 天精力充沛

---

_刘泽文专属 · 18 个月路线 · 2026-07-13 01:00 整理_