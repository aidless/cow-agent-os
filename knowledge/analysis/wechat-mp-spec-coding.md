# Spec Coding 实践 · 泰玄小站 v2.0 后端

> **适用项目**:泰玄小站 v2.0 后端 + wx-miniprogram
> **作者**:泰(刘泽文搭档)· 2026-07-11
> **状态**:实践沉淀,后续 Step 3-4 沿用

---

## 一句话总结

**v2.0 后端采用 spec coding 范式:**先写 `backend_contracts_v2.md`(规格)+ `specs/api/v2.endpoints.json`(机器可读),**然后**写实现代码。代码不是"先写再调",而是"照规格实现"。

---

## Spec Coding 在本项目的具体落地

### 三层契约结构

```
Layer 1 业务文档     backend_contracts_v2.md(545 行 markdown)
                       │ 人读
Layer 2 机器可读契约  specs/api/v2.endpoints.json(JSON Schema)
                       │ 单源真相
Layer 3 验证脚本      tests/* (结构化断言 + 集成测试)
                       ↓
                   实现代码
```

**关键**:每层只是**不同视图**表达同一份规格,改一个地方三层一起改。

### 本项目已落地的契约文件

| 文件 | 角色 |
|---|---|
| `wx-miniprogram/backend_contracts_v2.md` | 业务文档主源(545 行)|
| `wx-miniprogram/specs/api/v2.endpoints.json` | JSON Schema 单源(184 行)|
| `wx-miniprogram/specs/api/v1.endpoints.json` | v1.x 旧契约(向后兼容)|
| `wx-miniprogram/specs/prompts/*.yaml` | 8 派 prompt 模板 |
| `fortune-web-v2/specs/conftest.py`(待写)| pytest 测试套件 |

---

## v2.0 后端实际接入 spec coding

### Step 2 产物符合 spec coding 标准

| 产物 | 是否符合 |
|---|---|
| `llm_backends.py` Protocol 抽象 | ✅ 类型即规格 |
| `tests/test_llm_backends.py` 单元测试 | ✅ 行为即规格 |
| `benchmark_llm.py` 跑 8 prompt × 2 backend | ✅ 业务 KPI |
| `benchmark_report_*.md` Markdown 报告 | ✅ 给人看的 |
| `benchmark_*.json` JSON 数据 | ✅ 机器可读 + 二次分析 |

### 业务接入(Step 3)的 spec coding 路径

```
1. 读 specs/api/v2.endpoints.json(已知 6 个 endpoint)
2. 读 specs/prompts/{bazi,...}.yaml(8 派)
3. 写 handle_reading(liupai, body):
   - 校验 input(按 Schema)
   - 加载 prompt + 渲染
   - 调 router
   - 后置合规过滤
   - 解析 5 段
   - 返回标准响应
4. pytest:
   - test_handler_validation(输入校验)
   - test_handler_prompt_rendering(模板渲染)
   - test_handler_llm_call(LLM 真实调用 + 解析)
   - test_compliance_filter(绝对化用词过滤)
```

### 8 派 yaml prompt 渲染示例(伪代码)

```python
import yaml

def load_prompt(liupai: str, body: dict) -> dict:
    with open(f"specs/prompts/{liupai}.yaml") as f:
        prompt = yaml.safe_load(f)
    return {
        "system": prompt["system"].format(**body),
        "user": prompt["user_template"].format(**body),
    }
```

### 合规过滤(Step 3 后置 regex)

```python
import re

ABSOLUTE = re.compile(r'(必定|一定|绝对|注定|必须立即|百分百|大吉|大凶)')
WARN = {
    "必定": "通常",
    "一定": "可能",
    "绝对": "较为",
    "注定": "或有",
    "大吉": "良好",
    "大凶": "需留意",
}

def compliance_filter(text: str) -> str:
    for bad, good in WARN.items():
        text = text.replace(bad, good)
    return text
```

---

## 复用经验 · 从其他项目

| 项目 | 学到的 |
|---|---|
| awesome-llm-apps | 多 agent 团队用 `Team(...)` 自然语言定义协同 → **LLM 路由用 Protocol + router 自然语言驱动** |
| ai_mcp_app_builder | OpenAPI Schema 强校验作为契约 → **与 specs/api/*.json 思路一致** |
| RAG with Reasoning 模板 | 双面板 streaming + citations → **v2.0 可选开 SSE** |

---

## 与传统 backend 写法的差异

| 传统 | spec coding |
|---|---|
| 先写路由,边写边调 | 先写契约(JSON Schema),代码按契约实现 |
| 接口文档滞后于代码 | 文档与代码同源,改一处全改 |
| 错误处理靠 if-else | 契约层先校验,代码只管 happy path |
| 测试用手写 mock | Schema 自动生成 test case |

---

## 给下一步的 5 条建议

1. **Step 3 启动前**,先把 `wx-miniprogram/specs/api/v2.endpoints.json` 和 `wx-miniprogram/specs/prompts/{}.yaml` **完整复制**到 `fortune-web-v2/` 下
2. **不要直接 copy-paste `wx-miniprogram/utils/` 的代码**,而是按 v2 后端规范重写
3. **新代码先用 ype hints + Protocol + Pydantic/dataclass**,不用 dict 满天飞
4. **pytest 必须真跑 LLM**,不算 mock(主路 timeout、兜底超时都得测)
5. **所有接口的 req/resp 都写 JSON Schema**,放 `fortune-web-v2/specs/`

---

## 相关

- 上游:[泰玄小站 entity](../entities/taixuan-miniprogram.md)
- 搭档:[fortune-web-v2 后端仓](../entities/fortune-web-v2.md)
- 设计:[v2 LLM 后端设计](v2-llm-backend-design.md)
- 核心 spec 已经在 wx-miniprogram 仓: `specs/api/v2.endpoints.json` + `specs/prompts/`
