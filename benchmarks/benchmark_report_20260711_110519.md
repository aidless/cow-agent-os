# DeepSeek vs qwen3:4b 对比测试报告

- 开始时间:`2026-07-11T11:05:19.707754`
- 结束时间:`2026-07-11T11:07:32.847433`
- 每个 prompt 跑 2 次

## 🏆 总分对比

| Backend | 综合分(加权) | 平均分 | 合规分 | JSON 可解析率 | 平均延迟 |
|---|---|---|---|---|---|
| **qwen3_4b** | 0.0 | 0.0 | 0.0 | 0% | 7.57s |

## 📊 分维度对比

| 维度 | Prompt ID | DeepSeek | qwen3:4b | 胜者 |
|---|---|---|---|---|
| 基础对话 | basic_1_liupai_summary | — | — | — |
| 基础对话 | basic_2_liupai_list | — | — | — |
| 基础对话 | basic_3_liupai_vs_science | — | — | — |
| 结构化 JSON | json_bazi | — | — | — |
| 命理专项 | term_bazi_3points | — | — | — |
| 命理专项 | term_ziwei_setup | — | — | — |
| 合规 | compliance_cautious | — | — | — |
| 合规 | compliance_good_news | — | — | — |

## 📝 原文样例(每个 prompt 第一跑)

### basic_1_liupai_summary (基础对话)

**输入**:`用一句话向小白用户介绍命理学。......`

#### [deepseek]
❌ 错误:`HTTPError: HTTP Error 401: Authorization Required`

#### [qwen3_4b]
- 长度:0
- 中文占比:0%
- 合规分:0
- JSON 有效:False
- 延迟:5.02s

> 

### basic_2_liupai_list (基础对话)

**输入**:`列出中国传统命理的主要流派(5-7 个)。......`

#### [deepseek]
❌ 错误:`HTTPError: HTTP Error 401: Authorization Required`

#### [qwen3_4b]
- 长度:0
- 中文占比:0%
- 合规分:0
- JSON 有效:False
- 延迟:6.28s

> 

### basic_3_liupai_vs_science (基础对话)

**输入**:`命理学和现代科学的关系应该怎么看?......`

#### [deepseek]
❌ 错误:`HTTPError: HTTP Error 401: Authorization Required`

#### [qwen3_4b]
- 长度:0
- 中文占比:0%
- 合规分:0
- JSON 有效:False
- 延迟:7.8s

> 

### json_bazi (结构化 JSON)

**输入**:`排盘:男,1990-06-15 12:00 北京,甲子 乙丑 丙寅 丁卯。问题:近期事业如何?......`
**System**:`你是资深命理师,严格输出合法 JSON,不要任何额外文字。
格式:
{"summary":"...","sections":[{"title":"...","c...`

#### [deepseek]
❌ 错误:`HTTPError: HTTP Error 401: Authorization Required`

#### [qwen3_4b]
- 长度:0
- 中文占比:0%
- 合规分:0
- JSON 有效:False
- 延迟:13.4s

> 

### term_bazi_3points (命理专项)

**输入**:`排盘:甲子年 乙丑月 丙寅日 丁卯时。请用专业术语点评这个人 3 个最主要的命局特点。......`
**System**:`你是八字命理师,用专业但易懂的语言回答。...`

#### [deepseek]
❌ 错误:`HTTPError: HTTP Error 401: Authorization Required`

#### [qwen3_4b]
- 长度:0
- 中文占比:0%
- 合规分:0
- JSON 有效:False
- 延迟:10.38s

> 

### term_ziwei_setup (命理专项)

**输入**:`请用一段话向从未接触过紫微的用户解释「命宫」、「身宫」两个概念的区别。......`
**System**:`你是紫微斗数命理师。...`

#### [deepseek]
❌ 错误:`HTTPError: HTTP Error 401: Authorization Required`

#### [qwen3_4b]
- 长度:0
- 中文占比:0%
- 合规分:0
- JSON 有效:False
- 延迟:7.76s

> 

### compliance_cautious (合规)

**输入**:`盘主问近期感情。用 100 字回应,确保不出现'必定'、'一定'、'绝对'等词。......`
**System**:`你是命理解读师,务必避免绝对化用词,使用'通常'、'可能'、'建议'、'可考虑'等。...`

#### [deepseek]
❌ 错误:`HTTPError: HTTP Error 401: Authorization Required`

#### [qwen3_4b]
- 长度:0
- 中文占比:0%
- 合规分:0
- JSON 有效:False
- 延迟:5.61s

> 

### compliance_good_news (合规)

**输入**:`盘主近期家里添丁,如何用 80 字给出温暖但合规的祝贺?避免'大吉'、'必定发财'等绝对词。......`
**System**:`你是命理解读师,只做参考性解读。...`

#### [deepseek]
❌ 错误:`HTTPError: HTTP Error 401: Authorization Required`

#### [qwen3_4b]
- 长度:0
- 中文占比:0%
- 合规分:0
- JSON 有效:False
- 延迟:4.91s

> 

## 🎯 自动结论

- **综合胜者**:`qwen3_4b`(综合分 0.0)

**详细对比需要看上面原文 + 自己判断,客观分数只是参考。**