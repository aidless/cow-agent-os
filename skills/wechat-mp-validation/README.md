# wechat-mp-validation · 快速参考

> 一行话:**泰玄小站"我刚改完代码,跑一下验证"的标准流水线**

## 用法

### 方法 1:跑 batch 脚本(推荐)
```bash
# 把 validate.bat 复制到项目根
copy skills\wechat-mp-validation\validate.bat F:\test\2026-06-27-14-59-27\wx-miniprogram\

# 然后
cd F:\test\2026-06-27-14-59-27\wx-miniprogram
validate.bat
```

### 方法 2:跟我说"跑一下验证"
我会自动定位项目根 + 跑 5 步 + 解读结果。

### 方法 3:手动跑某一步
详见 `SKILL.md` 第 1-5 步命令。

## 5 步流水线速查

| 步 | 内容 | 期望 | v1.9.12 基线 |
|---|---|---|---|
| 1 | JS node --check | 全过 | 36/36 |
| 2 | JSON parse | 全过 | 15/15 |
| 3 | 8 个专业性测试 | 全过 | A 3 + B 0 + C 9 + D 85 + E 61 + F 0 + G 83 + H 7 |
| 4 | 客观性扫描 | 0 severe | 0 severe |
| 5 | 主包体积 | < 2MB | 893K / 2048K |

## 与 ML 研究的区别

| 维度 | ML 论文 | 泰玄小站 |
|---|---|---|
| 验证工具 | verify_p5.py | 5 步流水线 |
| 触发时机 | 完成一个 patch | 完成一个 patch |
| 输出 | "6/6 PASS" | "5/5 PASS" |
| 红线 | 引用 / 实验可复现 | 主包 < 2MB / 客观性 0 severe |

## 历史教训(避坑)

1. **测试必须与生产同步** —— v1.5 引入 6tail 时旧测试测的是已删的 lunar.js
2. **catch 块不能只 setData** —— v1.5.1 才加 `reportError`
3. **picker 状态要持久化** —— 用户回访丢选择
4. **字段名漂移** —— `primary_engine` vs `primary` / `created_at` vs `createdAt` / `id` 类型 number/string 来回
5. **立春换年** —— v1.9.4 修,v2.0 后端必跑 7 个立春用例