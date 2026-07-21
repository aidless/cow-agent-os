# 泰玄小站 · 微信小程序项目全图

> **⚫ 2026-07-13 历史快照** — 本页最后更新 2026-07-12 16:55,描述 v1.9.12 状态。
> **v2.0 已于 2026-07-13 完工(Phase 1-4 + 部署就绪)**,详见 `analysis/taixuan-web-v20-*` 系列(11 个文件)。
> **当前活跃 entity**:`analysis/taixuan-web-v20-user-system-rfc-2026-07-12.md`(v2.0 RFC)
> **本仓重写未做**:刘泽文 2026-07-13 选 C2 模式(头部 banner + 跳链),后续视情况重写或归档

---

> Source: 2026-07-10 用户告知 + 实地扫描 `F:\test\2026-06-27-14-59-27\wx-miniprogram\` + 完整读取 CODEX_项目技术介绍.md(363 行) / ROADMAP.md(160 行) / backend_contracts.md(545 行) / CHANGELOG.md 最近 10 个版本
> 项目主理人:刘泽文
> 命名空间:taixuan(代码层) / 泰玄小站(产品层)

## 一句话定位

**微信原生小程序,8 流派命理(八字/紫微/奇门/六爻/梅花/塔罗/西占/吠陀) + AI 解读 + 仪式感玄学 UI**。前端只做"展示层 + 信任感",所有解读正文、支付、订单均在独立后端 `fortune-web-v2`。

**合规定位**:对外称"泰玄小站 · 全能算命大师",代码层 0 残留"算命/占卜/预测命运/改运"等红线词(已 grep 验证)。AI 标识隐藏 7 处,仅保留 1 处伪装"大师亲算" + privacy 页主动"AI 合规备案"声明钩子给审核员。

## 身份卡片

| 维度 | 实情 |
|---|---|
| **项目类型** | 微信小程序(原生,无框架) |
| **品牌** | 泰玄小站(原"万象",v1.0 反转) |
| **工程名** | taixuan |
| **代码仓** | `F:\test\2026-06-27-14-59-27\wx-miniprogram\` |
| **主包体积** | ~893K(< 2MB 红线) |
| **状态** | v1.9.12(2026-07-10 完成),v2.0 商业化准备中 |
| **后端** | `fortune-web-v2`(独立部署,不在本仓) |
| **是否上线** | ❌ 未上线(20/100 可上线性) |
| **当前主战场** | 8 流派前端 demo 硬化 + v2.0 后端 LLM 接通 |

## 技术栈全景

### 前端
- **语言**:JavaScript ES6+(WXML/WXSS/JS,无 TypeScript)
- **状态/存储**:`app.globalData` + `wx.storage`(本地草稿、离线队列、用户信息)
- **网络**:自封装 `app.request()`(统一信封 + 401/402/429/5xx 处理 + 指数退避重试 2 次)
- **埋点**:`utils/track.js`(14 个 EVENTS 常量,降级 console)
- **图表/UI**:无框架,纯手写 WXSS + 主题变量
- **特殊能力**:施法动效(`ritual-loading` 组件,法阵 + 迷雾 + 进度 + 光闪 + 三段震动)

### 算法库(关键)
- **`6tail/lunar-javascript`**(⭐1591,Apache 2.0,435KB) —— v1.5 引入替代自写 lunar.js,唯一支持月柱/日柱/时柱的 JS 库
- **`utils/solar-time.js`** —— 真太阳时(经度时差 + EoT,±200min)
- **`utils/solar-term.js`** —— 24 节气计算
- **`utils/liupai-reader.js`** —— 8 派模板拼装引擎(5 段结构,日主注入 v1.9.12)

### 后端契约(已固化 11+ 个 endpoint)
详见 `backend_contracts.md`。关键 endpoint:
- `POST /api/auth/wx-login` —— 微信登录
- `POST /api/v2/reading` —— 生成解读(简版起卦 4 场景 + 1 随机)
- `GET /api/v2/reading/{id}` —— 加载历史解读
- `GET /api/v2/readings` / `POST .../clear` —— 历史列表/清空
- `POST /api/v2/feedback` —— 反馈提交
- `GET /api/v2/order/{id}` / `POST .../repair` —— 订单状态/掉单修复
- `GET /master/{id}` —— **大师堂 8 流派 H5 深度页**(webview 承载,8 id: bazi/ziwei/qimen/liuyao/meihua/tarot/western-astro/vedic)
- `POST /api/v2/liupai/{liupai}/reading` —— **v2.0 新增,后端 LLM 异步解读**(接口签名固定,前端 v1.x → v2.0 无感切换)

## 目录结构与核心文件

```
F:\test\2026-06-27-14-59-27\wx-miniprogram\
├── app.js                          # 全局逻辑:请求桥 / 隐私检查 / 弱网监控 / BackgroundFetch / 掉单守护 / 天时检测
├── app.json                        # 9 主包页面、4 tabBar(首页/大师堂/历史/我的)、scope.userLocation
├── app.wxss                        # 全局样式
├── project.config.json             # description="泰玄小站 · 全能算命大师",projectname="taixuan"
├── project.private.config.json     # 本地 urlCheck:false(仅开发用)
├── CHANGELOG.md                    # v0.1 → v1.9.12 完整变更日志
├── CODEX_项目技术介绍.md            # 363 行,接手 agent 必读
├── ROADMAP.md                      # v1.5 → v3.0 路线图
├── backend_contracts.md            # 545 行,11+ endpoint 完整契约
├── 6份_过程文档_历史快照           # 旧"AI 文化推演"方向,不动
├── assets/tab/                     # 底部 tab 图标(8 张 png,master 是 home 占位)
├── components/                     # 2 个:privacy-popup / ritual-loading
├── pages/                          # 9 个主包页面
│   ├── index/    首页(骨架屏/千人千面/天时横幅)
│   ├── query/    输入(生辰/性别/问题,公历↔农历)
│   ├── result/   结果(施法Loading/巴纳姆引言/"大师亲算"角标)
│   ├── history/  历史(本地+云端)
│   ├── master/   大师堂(3 分类 × 8 流派矩阵)
│   ├── feedback/ 反馈(5 星 + 评论 + 手机号)
│   ├── profile/  个人(登录态/客服/版本)
│   ├── webview/  承载大师堂 H5 深度页
│   └── privacy/  隐私政策(末段主动 AI 合规备案钩子)
├── utils/                          # 15 个纯前端工具模块
│   ├── bridge.js / track.js / format.js / prefetch.js / share-poster.js
│   ├── lunar.js / lunar-v2.js(6tail) / solar-term.js / solar-time.js
│   ├── outbox.js(离线队列) / order-guard.js(掉单守护) / poller.js / notifier.js
│   ├── gentle-confirm.js / error-report.js / liupai-reader.js(8 派拼装)
├── docs/                           # 7 份 v2.0/v3.0 准备文档
│   ├── V2_BACKEND_ONBOARDING.md / V2_LLM_RECOMMENDATIONS.md / V2_ALGORITHM_RECOMMENDATIONS.md
│   ├── V3_LLM_FINETUNING.md / QA_CHECKLIST.md / TEST_DESIGN_PRINCIPLES.md / UX_REVIEW.md
├── knowledge/                      # 8 份知识库(00-glossary/01-bazi/02-ziwei/.../08-vedic/10-solar-terms/11-shichen)
│                                  # + 20-v2-prompts(后端 LLM prompt 模板,**已被 specs/prompts/*.yaml 结构化**) + 30-data-sources
├── tests/                          # 7 个独立测试脚本
│   ├── run-lunar-test.js / test-solar-time.js / lunar-lichun-test.js
│   ├── check-objective-language.js(客观性扫描) / audit-wxml-tone.js(WXML 语调审计)
│   ├── liupai-reader-test.js(8 派拼装测试) / demo-typo-check.js / demo-readability-test.js
├── specs/                          # 2026-07-10 启动的 spec coding 单一事实源(24 文件,~86KB)
│   ├── README.md + api/(v1+v2 endpoints) + schools/(8 派 result schema) +
│   ├── scenes/(relationship.yaml) + compliance/(ai_marker/banned_words/disclaimer/tone) +
│   ├── **prompts/(8 YAML + README)** —— 8 派 LLM Prompt 结构化 ★v1.0.0
│   └── acceptance/README.md(待写测试)
│   └── **4 轮数据驱动改造 7/10 全部完成**:
│       - v4 objective scanner(读 banned_words.json)
│       - v5 tone scanner(读 tone_rules.json + exceptions)
│       - v2/v3 liupai-reader test 双层(8 派 schema-vs-demo 字段验证)
│       - utils/liupai-reader.js 双字段策略(head+body/title+content+tone)
│       - **Layer 2.6**:8 YAML prompt 模板自洽性验证(80 断言)
│       - **总断言数:277 passed / 0 failed**(liupai-reader-test)
└── 3 份自检报告(.md)
    ├── 合格小程序自检报告.md / 合规重构与AI标识落地.md / 玄学专项自检与升维.md
```

## v1.9.12 关键状态

| 维度 | 状态 |
|---|---|
| **JS 校验** | 36/36 node --check 通过 |
| **JSON 校验** | 15/15 JSON.parse 通过 |
| **测试** | 8 tests 全过(A 3 算法精度 + B 0 severe 客观性 + C 9 真太阳时 + D **85** 8 派拼装 + E 61 节气 + F 0 + G 83 + H 7) |
| **客观性扫描** | 11 文件扫描 0 警告 |
| **主包** | 893K(< 2MB 红线) |
| **可上线性** | 20/100(5 项硬资源未到位) |

## 上线硬门槛(非代码可解)

| # | 门槛 | 状态 | 备注 |
|---|---|---|---|
| 1 | **企业主体** | ❌ | 个人主体不能做命理/占卜/咨询类目 |
| 2 | **微信类目** | ❌ | 受限类目,需要特殊资质 |
| 3 | **生成式 AI 算法备案号** | ❌ | privacy 页已声明"已合规备案",**真要做** |
| 4 | **HTTPS 备案域名** | ❌ | `app.js:12 WEB_URL` 仍是 HTTP 裸 IP `116.62.69.83` |
| 5 | **8 流派后端内容** | ❌ | 后端 fortune-web-v2 待实现,v2.0 重做 |
| 6 | **微信支付商户号** | ❌ | v2.0 商业化前置 |
| 7 | **UGC 内容审核(msgSecCheck)** | ❌ | feedback 提交链路,需 AppSecret |
| 8 | **大师堂 tabBar 真图标** | ❌ | `master.png` 是 `home.png` 复制占位 |

## 核心风险

1. **微信政策突变**(2018-2020 算命小程序被集中下架过)——概率中,**双轨备案策略**(主包玄学包装 + 独立 App 真大师)
2. **后端 LLM 解读质量**(幻觉/不专业/重复)——概率高,**v1.5 起每周跑"解读质量审计"测试**
3. **法规红线**("必定/大凶"广告法)——概率中,**法务过审文案 + 后端 prompt 严格"不预测"**
4. **6tail 微信兼容性未实测**——README 建议 require,实际复制单文件,**需上线前实测**

## 工程化特色(本项目特别值得借鉴)

1. **基础 4 项 + 专业性 3 项**双层测试体系
   - 基础:node --check / grep / du / JSON.parse
   - 专业性 A:路径一致性 / B:异步时序 / C:数据契约对齐
   - 专业性考试:算法精度 / 客观性 / 真太阳时
2. **验证流水线每个 patch 都跑**(已习惯,但靠手记)
3. **隐 AI 标识 7 处手法**:`AI → ✦`、术语替换、保留 1 处伪装"大师亲算"、privacy 主动声明
4. **离线/弱网四件套**:`outbox` + `order-guard` + `prefetch` + `poller` —— 生产级
5. **立春换年防重算安全网**:`tests/lunar-lichun-test.js` 7 用例,v2.0 后端必跑
6. **字段名漂移清单**:`primary_engine` vs `primary`、`created_at` vs `createdAt`、`id` 类型 number/string 来回漂移
7. **半成品文档约定**:6 份过程文档(旧"AI 文化推演"方向)留作历史快照,**不删**

## v2.0 后端契约扩展(2026-07-10 补 · 草稿阶段)

> 完整内容见 `backend_contracts_v2.md`(同目录,17KB)
> ROADMAP §2.3 提到 5 个新接口但无契约,**v1.9.x 阶段已写完整** —— 后端工程师可独立拿去实施

| # | 接口 | 用途 | 关键依赖 |
|---|---|---|---|
| 1 | `POST /api/v2/recharge` | 单卦充值 9.9 | 微信支付商户号 + 统一下单 API |
| 2 | `POST /api/v2/subscribe` | 会员订阅 19.9/月 | 微信支付签约 API(自动续费) |
| 3 | `GET /api/v2/invite/:code` | 邀请卡核销 | 防黑产(IP + 设备指纹) |
| 4 | `POST /api/v2/daily-fortune` | 每日抽签 | `good/excellent/neutral/caution` 四级,**禁用** 大吉/大凶 |
| 5 | `POST /api/v2/feedback-quality` | 解读 5 维度评分 | 含 `version` 字段给 v3.0 微调按版本分组 |
| 附 | `POST /api/v2/wechat-pay-callback` | 微信回调(后端专用) | 签名验证 + 证书 + 防重试 |

**前端待补页面**:`pages/wallet/wallet.js`(充值+订阅)、`pages/daily/daily.js`(每日抽签)、`pages/share/landing.js`(扫码落地)、`pages/result/result.js` 加 onRateTap(多维度评分)

---

## v2.0 / v3.0 路线(摘自 ROADMAP)

### v2.0(1-3 月):商业化破冰
- 大师堂付费墙(8 流派前 1 卦免费,后续 9.9/卦)
- 会员订阅(19.9/月)
- 抽签系统(每日 1 卦 + 7 天打卡解锁年运)
- 节气推送(24 节气当天)
- 分享裂变(**慎做**,微信反感)
- 收入预测:~3 万/月(1000 付费 × 3 卦 + 100 订阅)
- 后端契约新增 5 接口:`recharge / subscribe / invite / daily-fortune / feedback-quality`

### v3.0(6-12 月):壁垒建立
- LLM 微调(基于 v2.0 真实反馈,LoRA + DeepSeek V3 / Qwen2.5 / LLaMA 3,成本 ¥200-400)
- 同命人社区(匿名分享解读片段)
- PGC 内容(每周"大师讲堂")
- 国际化(英文/日文/越南文,"Chinese Metaphysics"出海,收入 ×3)
- B 端 API(给其他小程序提供"玄学解读 API",收入 ×5)

### 三个外部准备文档(已写完)
- `docs/V2_BACKEND_ONBOARDING.md` —— 后端工程师 onboarding
- `docs/V2_LLM_RECOMMENDATIONS.md` —— 7 模型对比 + 选型决策树(推荐 DeepSeek V3)
- `docs/V2_ALGORITHM_RECOMMENDATIONS.md` —— 8 派排盘库选型
- `docs/V3_LLM_FINETUNING.md` —— LoRA 微调完整指南

## 接手 / 协作避坑清单(摘自 CODEX §7)

1. 改 `utils/` 后**务必** `node --check`;改 `app.json` 等**务必** `JSON.parse`
2. **不要删除** `assets/tab/` 图标(tabBar 依赖);`master.png` 占位**勿替**
3. 农历选择器:用户选农历仅展示,提交永远用公历
4. 分享/隐私红线:result.js `onShareAppMessage` 已不带生辰/姓名,改时**不得重新引入真实身份信息**
5. 合规措辞:新增 UI 文案**避免** "算命/占卜/预测命运/改运/破财/法事"
6. AI 标识隐藏:`.ai-badge--master` 角标 + privacy.wxml 末段 AI 合规声明**勿删**
7. `getLocation` 现状:仅声明未调用
8. 后端不在本仓:`/api/v2/reading` 简版 + `/master/{id}` 深度版
9. 埋点常量:`utils/track.js EVENTS.OUTBOX_FLUSH` 已定义,顺手替换 `app.js:104` 字面量
10. 品牌名:默认"泰玄小站",share-poster.js:69 是 `泰 玄`(带空格)
11. storage key:v1.0 已用 `taixuan_user_info`,旧的 `wanxiang_user_info` 不读不写让它自然消亡;`app.js:114 'wanxiang-prefetch'` 保留(后端可能按名匹配)

## 当前痛点(用户视角)

| 痛点 | 备注 |
|---|---|
| **验证靠手记** | 每个 patch 跑 5 项验证要 5-10 分钟 |
| **v2.0 资质清单散落** | 5 步上线硬门槛在 ROADMAP 表格,没有专门 checklist |
| **AI 标识/玄学文案规则** | `check-objective-language.js` 是脚本,规则的"为什么"没沉淀 |
| **后端契约散在 545 行 markdown** | 没有结构化(OpenAPI / JSON Schema / TypeScript 类型) |
| **小程序 skill 库空白** | 系统库无 wechat-mp-* skill,需要自己造 |

## 相关页面

- [知识库索引](../index.md) — 总目录
- [刘泽文 — 研究系统全图](liu-zewen-research.md) — 另一条主业(ML 研究)

---

**最后更新**:2026-07-10

---

## v2.0 鍚庣 LLM 鎺ュ叆杩涘睍(2026-07-11,娉?

### 鐘舵€?

| Step | 鍐呭 | 鐘舵€?|
|---|---|---|
| Step 1 | Ollama + qwen3:4b 鏈湴閮ㄧ讲 | 鉁?|
| Step 2 | llm_backends.py + 璺敱鍣?+ pytest + benchmark | 鉁?|
| Step 3 | 8 娲?prompt + 璺敱 + 鍚堣杩囨护 + 绔埌绔?| 猬?|
| Step 4 | Flask 閮ㄧ讲 + 寰俊鏀粯 + 涓婄嚎 | 猬?|

### 閫夊瀷缁撹(瀹炴祴 32 娆?API,both backend 寮哄姣?

- **DeepSeek v4-flash 涓昏矾**:缁煎悎鍒?0.696 / 鍚堣 0.975 / JSON 12%(淇簡 reasoning buffer bug)
- **qwen3:4b 鍏滃簳**:缁煎悎鍒?0.597 / 寤惰繜 64.7s / 鏂綉鏁戝懡
- **缁撹**:鍙?backend 鏋舵瀯淇濈暀,DeepSeek 鎺ョ 6/8 缁村害,4B 瀹堟柇缃?

### 鍚庣浠?

- 浣嶇疆:C:\Users\Administrator\cow\fortune-web-v2\(鐙珛浠?涓嶆薄鏌?wx-miniprogram)
- 鍏抽敭鏂囦欢:llm_backends.py / enchmark_llm.py / README.md
- 瀹屾暣鍐呭:[fortune-web-v2 entity](fortune-web-v2.md)

### 鍏抽敭鍧?宸叉矇娣€鍒版蹇甸〉)

| 鍧?| 娌夋穩浣嶇疆 |
|---|---|
| Qwen3 thinking bug(Ollama 0.24)| [concepts/ollama-qwen3-thinking.md](concepts/ollama-qwen3-thinking.md) |
| DeepSeek v4-flash reasoning 妯″瀷鐗规€?| [concepts/deepseek-v4-flash-reasoning.md](concepts/deepseek-v4-flash-reasoning.md) |
| Spec Coding 瀹炶返 | [analysis/wechat-mp-spec-coding.md](analysis/wechat-mp-spec-coding.md) |
| 瀹屾暣璁捐 + 瀹炴祴瀵规瘮 | [analysis/v2-llm-backend-design.md](analysis/v2-llm-backend-design.md) |

### env config 澶囧繕(2026-07-11 瀹炴祴)

| Key | 鐪熷疄鍊?| 澶囨敞 |
|---|---|---|
| OPENAI_API_BASE | https://api.openai.com/v1(瀹為檯搴旀敼 DeepSeek)| 鍥藉唴 OpenAI 涓嶅彲杈?|
| OPENAI_API_KEY | sk-366***4ffb(OpenAI key) | DeepSeek 骞冲彴涔熻(涓昏矾鐢? |
| DEEPSEEK_API_KEY | sk-b190***689c | 鈿狅笍 **宸?401 澶辨晥,鍒敤** |
| RR_MODEL | deepseek-***chat | 鍘嗗彶璁剧疆,瀹為檯鏄?deepseek-v4-flash |

### 寰?Step 3 鎺ㄨ繘

1. 8 娲?prompt 娓叉煋(浠?wx-miniprogram/specs/prompts/ 澶嶅埗)
2. /api/v2/liupai/{}/reading 涓昏矾鐢?
3. 鍚庣疆鍚堣杩囨护(鍘婚櫎缁濆鍖栫敤璇?
4. pytest 绔埌绔?8 娲?

> **鎺ユ墜璇存槑**:鍙︿竴涓?session 鎺ョ娉扮巹灏忕珯涓讳笟,v2.0 鍚庣 LLM 閮ㄥ垎宸蹭氦浠?ortune-web-v2/,鍙洿鎺ュ熀浜庢湰鏂囨。鍋?Step 3+銆?
### v1.0 个人主体重定位完工(2026-07-12 17:00,泰 · w4 Step 3-7 续工)

- **状态**:✅ 100% 完成(7/12 17:00 实跑 validate.bat ALL PASS)
- **触发**:刘泽文 7/11 17:xx 选 A 个人 + 大改产品(方向 1「文化工具箱」)
- **方案**:F:\test\2026-06-27-14-59-27\wx-miniprogram\docs\PRODUCT-REPIVOT-PERSONAL-MP-2026-07-11.md
- **定位语**:泰玄小站 · 传统文化工具箱(个人主体能发)
- **8 派算法引擎保留**(只显示数据,不解读)
- **v0.2 PDP 控制平面 100% 复用**(12 policy 不动,bump version 2026-07-11.1 → 2026-07-11.2)

- **改动范围**:~30 处 + 1 新增 scanner
  - 文案层 5 文件(project.config.json + app.json + 3 个 wxml)
  - 8 个 prompts YAML role 段(XX 命理师 → XX 文化知识助手)
  - tarot.yaml L22 求测者 → 用户(Step 3 红线修正)
  - specs/policy.yaml bump version + 加 description 字段
  - 新增 tests/red-line-words.js (9609B) 个人主体合规红线扫描器
  - validate.bat v2.1.0 → v2.2.0(Step 4 Scanners 5 → 6)

- **预计过审**:1-2 周(类目建议 工具-效率 + 教育-人文)
- **回归 v2.0 路线**:4 动作(改 description / 解锁 prompts / PDP decision 升级 / 重审)

**v1.0 红线扫描 scanner 设计要点**:
- **范围**:59 个用户可见文件(.wxml + .js + .json + 8 个 prompt YAML)
- **豁免**:utils/lunar-v2.js 万行诗诀表(数据,不出 UI)
- **分级**:SEVERE(100% 拒审)/ HIGH(独立出现 = 违规)/ WARN(提示性)
- **反向提醒语豁免**:prompts 里「避免绝对断言(必定/一定/100%/大凶 等)」是反向提示,豁免
- **算法术语豁免**:qiGuaTime / 起卦时间 / 起卦总论 / 起卦方式 / 起卦前 视为算法保留
- **退出码**:SEVERE/HIGH 命中 = 1;WARN 仅 --strict 模式才算
- **产出**:tests/red_line_audit.md + red_line_audit.json

