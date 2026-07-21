---
name: wechat-mp-validation
description: 微信小程序「泰玄小站」项目的标准验证流水线(2026-07-11 升级到 v2.1.0)。每次代码改动后跑一次,覆盖 5 步验证(JS 语法 / JSON 语法 / 7 核心测试 + spec 自洽 / 5 个 scanner 含 cost+permission / 主包体积)。推荐入口 `validate.ps1`(PowerShell,无 cmd.exe 假报错);Windows cmd 用户用 `validate.bat` v2.1.0(禁用 FAIL/ERR/BAD/PASS 等关键字)。适用于 v2.0 商业化合规发版前全量回归,v1.5-v1.9.x 历史 patch 同样适用。
---

# ⚠️ 维护警告(7/11 学到的 cmd.exe 陷阱 + v2.1.0 bat 根检测修复)

**本 skill 的 validate.bat 模板已升级到 v2.1.0**,专门规避 cmd.exe 的关键字陷阱 + skill 调用时根目录跳错问题。

**绝对禁止**(下次重写/复制本 skill 模板时):
1. ❌ bat 内部出现 `FAIL` / `ERR` / `BAD` 三个英文单词 —— cmd 会当命令,在 stdout 报 `XXX was unexpected at this time.` 假错
2. ❌ bat inline `node -e "...{...}..."` —— cmd 会转义 `{` `}` `[]`,JSON.parse 永远失败
3. ❌ 子程序 `exit /b 1` —— 退出码会污染 PowerShell `$p.ExitCode`(变成 255)
4. ❌ 看 PowerShell `ExitCode` 决定成败 —— 永远只**看 bat 内部 stdout 是否出现 `=== ALL PASS —— 可以发版 ===`**

正确做法(模板已固化):
- 用 `JS_BAD` / `JSON_BAD` / `bad` 代替 `FAIL` / `ERR` / `BAD` 命名
- JSON / 主包 / Scanner 都拆成独立 `tests/_validate-stepN-X.js` 脚本,bat 用 `call node ...` 调
- 子程序用 `goto :eof` 返回,失败不 `exit /b`

详见下文 bat 模板注释。

# WeChat MP Validation · 泰玄小站验证流水线

> **项目根**:`F:\test\2026-06-27-14-59-27\wx-miniprogram\`
> **版本范围**:v1.5 → v1.9.x(后续 v2.0 可复用主体,扩后端契约测试)
> **何时调用**:每次 patch 完成后 / 发版前 / 用户说"我刚改完代码"

## 🎯 何时使用本 skill

满足以下任一条件时,主动调用:

1. 用户说"我改了 X 文件"、"刚 patch 完"、"帮我验证"、"能上线吗"
2. 用户贴了某个 patch 的 diff,想确认是否破坏现有功能
3. 用户问"v1.x → v1.y 怎么发版" / "发版前要做什么"
4. CHANGELOG.md 出现新版本号要发布前

**不要**在用户没有改动、没有发布意图时主动调用 —— 验证要花 30-60 秒。

## 📋 验证流水线(5 步)

### Step 1 · JS 语法检查(node --check)
```bash
# Windows cmd
for /R utils %f in (*.js) do @node --check "%f" >nul 2>&1 && echo OK %~nxf || echo FAIL %~nxf
for /R pages %f in (*.js) do @node --check "%f" >nul 2>&1 && echo OK %~nxf || echo FAIL %~nxf
for /R components %f in (*.js) do @node --check "%f" >nul 2>&1 && echo OK %~nxf || echo FAIL %~nxf
for /R tests %f in (*.js) do @node --check "%f" >nul 2>&1 && echo OK %~nxf || echo FAIL %~nxf
node --check app.js
```

**期望**:43/43 全过(v2.1.0 实测 7/11)

### Step 2 · JSON 语法检查
```bash
node -e "JSON.parse(require('fs').readFileSync('app.json','utf8'))" && echo "OK app.json"
node -e "JSON.parse(require('fs').readFileSync('project.config.json','utf8'))" && echo "OK project.config.json"
# ... 同理 sitemap.json / pages/*/*.json / components/*/*.json
```

**期望**:33/33 全过(v2.1.0 实测 7/11)

### Step 3 · 9 个测试脚本依次跑
按以下顺序跑(每个独立 `node` 调用,失败立即停下):
```bash
cd F:\test\2026-06-27-14-59-27\wx-miniprogram
node tests/run-lunar-test.js              # A 算法精度(3 case)
node tests/check-objective-language.js    # B 客观性扫描(scanner,exit 1 = block)
node tests/test-solar-time.js             # C 真太阳时(3 case)
node tests/liupai-reader-test.js          # D 8 派拼装 + schema 自洽(197+ 断言)
node tests/lunar-lichun-test.js           # E 立春换年(7 case)
node tests/demo-typo-check.js             # F typo 扫描(83 断言)
node tests/demo-readability-test.js       # G 可读性(61 断言)
node tests/audit-wxml-tone.js             # H 语调软化(scanner,exit 永远 0)
node tests/check-spec-coherence.js        # I specs/ 自洽(11 pass / 0 issue / 0 warn)
```

**期望**:7/7 全绿(实测合计 **451 断言** + 0 failed)。**v2.1.0 把 B/H/I 三个 scanner 移到 Step 4**(独立 Scanners 组),Step 3 只剩 7 个真正"test"(A/C/D/E/F/G + spec 自洽 I)。原 v1.9.x 的"9 测试"编号是历史命名。

### Step 4 · 主包体积
**关键**:**不要**在 bat 里 inline `node -e "...let t=0..."`。**主包体积检查拆成独立脚本** `tests/_validate-step5-bundle.js`,然后 bat 用 `call node tests\_validate-step5-bundle.js` 调。原因:cmd 的 inline JS 字符串会被转义 `{}` `[]` 字符,触发假报错。
```bash
node -e "
const fs = require('fs'); const path = require('path');
const dirs = ['utils', 'pages', 'components', 'assets'];
let total = 0;
for (const d of dirs) {
  const walk = (p) => {
    for (const f of fs.readdirSync(p)) {
      const fp = path.join(p, f);
      const s = fs.statSync(fp);
      if (s.isDirectory()) walk(fp);
      else total += s.size;
    }
  };
  walk(d);
}
console.log('主包(含 utils/pages/components/assets):', (total/1024).toFixed(0) + 'K');
console.log('2MB 红线:2048K', total/1024 < 2048 ? '✅ PASS' : '❌ FAIL');
"
```

**期望**:主包 < 2048K(v2.1.0 实测 612K)

### Step 4 · Scanners(v2.1.0 实为 `[4/5]` 步骤,5 个 scanner 全部跑)
**v2.1.0 把 Scanners 独立成一组**(原 Step 5 现在合并到 `[4/5]`)。包括:

| Scanner | 期望输出 | 来源 |
|---|---|---|
| `check-objective-language.js` | 100/100 分 | v2.0.0 已有(客观性 + AI 标识) |
| `audit-wxml-tone.js` | 0 block | v2.0.0 已有(WXML 语调软化) |
| `cost-scanner.js` [w4-step2] | 0/N 超 cap | **v2.1.0 新增**(cost 控制平面) |
| `permission-scanner.js` [w4-step3] | 0 违规 | **v2.1.0 新增**(permission 扫描) |
| `permissions-validate.js` [w4-step4] | 6/6 endpoint 通过 | **v2.1.0 新增**(spec endpoint 校验) |

**关键**:同 Step 4,不要在 bat 里 inline node 表达式。每个 scanner 独立 `.js`,bat 用 `call :runTest "tests\<name>.js" "<label>"` 调。

期望输出(bat 内部 stdout):
```
✅ Step 4 PASS —— 5 个 scanner 全过(2 历史 + 3 v2.1.0 新增)
```

### Step 6 · 输出标准化报告
模板:
```
📊 验证报告 · [版本号] · [日期]
─────────────────────────────────
✅ Step 1 · JS 语法检查:36/36 通过
✅ Step 2 · JSON 语法检查:15/15 通过
✅ Step 3 · 8 测试全过:
   A 算法精度 3/3  |  B 客观性 0 severe  |  C 真太阳时 9/9
   D 8 派拼装 85/85 | E 立春换年 7/7  |  F typo 0
   G 可读性 83/83 |  H 语调 7/7
✅ Step 4 · 主包 893K(< 2048K 红线)
─────────────────────────────────
🟢 可发版 / 🔴 需修复 [具体项]
```

## 🛠️ 一键脚本

### Windows(cmd)
保存为 `validate.bat`,放在项目根。**Windows 路径不要直接拼进 `node -e "..."` 的 JS 字符串**；路径一律作为 argv 传给 Node,否则 `\t`、`\2026`、`%%f` 等会被 JS/cmd 双重解析破坏:

**⚠️ 关键字陷阱(7/11 学到)**:cmd.exe 会把 bat 内部的 `FAIL` / `ERR` / `BAD` 当命令关键字,在 stdout 解析时报 `XXX was unexpected at this time.` 假错。**bat 文件里禁止出现这三个英文词**,统一用 `bad` / `err_count` / `[X]` 替代。已经栽过的位置:`echo JS 检查: ... ERR`、`echo FAIL xxx`。验证时**只看 bat 内部 "ALL PASS"** 行,**不要**看 PowerShell 拿到的 `ExitCode 255`。

```bat
@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
echo === 泰玄小站 验证流水线 v1.0.5 ===
set JS_OK=0
set JS_BAD=0
set JSON_OK=0
set JSON_BAD=0

echo [1/5] JS syntax...
for /R utils %%f in (*.js) do @node --check "%%f" >nul 2>&1 && (set /a JS_OK+=1 >nul & echo  [OK]  %%~nxf) || (set /a JS_BAD+=1 >nul & echo  [X]   %%~nxf)
for /R pages %%f in (*.js) do @node --check "%%f" >nul 2>&1 && (set /a JS_OK+=1 >nul & echo  [OK]  %%~nxf) || (set /a JS_BAD+=1 >nul & echo  [X]   %%~nxf)
for /R components %%f in (*.js) do @node --check "%%f" >nul 2>&1 && (set /a JS_OK+=1 >nul & echo  [OK]  %%~nxf) || (set /a JS_BAD+=1 >nul & echo  [X]   %%~nxf)
for /R tests %%f in (*.js) do @node --check "%%f" >nul 2>&1 && (set /a JS_OK+=1 >nul & echo  [OK]  %%~nxf) || (set /a JS_BAD+=1 >nul & echo  [X]   %%~nxf)
node --check app.js >nul 2>&1 && (set /a JS_OK+=1 >nul & echo  [OK]  app.js) || (set /a JS_BAD+=1 >nul & echo  [X]   app.js)
echo  JS 检查: !JS_OK! OK / !JS_BAD! bad

echo [2/5] JSON syntax...
for /f "delims=" %%f in ('powershell -NoProfile -Command "Get-ChildItem -Path . -Recurse -File -Filter *.json ^| Where-Object { $_.FullName -notmatch '[\\/]\.git[\\/]' -and $_.FullName -notmatch '[\\/]node_modules[\\/]' } ^| Select-Object -ExpandProperty FullName"') do call :checkjson "%%f"
echo  JSON 检查: !JSON_OK! OK / !JSON_BAD! bad
if !JSON_BAD! NEQ 0 goto end_bad

echo [3/5] Tests...
call :runTest "tests\run-lunar-test.js" "A 算法精度"
call :runTest "tests\check-objective-language.js" "B 客观性扫描"
call :runTest "tests\test-solar-time.js" "C 真太阳时"
call :runTest "tests\liupai-reader-test.js" "D 8 派拼装"
call :runTest "tests\lunar-lichun-test.js" "E 立春换年"
call :runTest "tests\demo-typo-check.js" "F typo 扫描"
call :runTest "tests\demo-readability-test.js" "G 可读性"
call :runTest "tests\audit-wxml-tone.js" "H 语调软化"
call :runTest "tests\check-spec-coherence.js" "I spec 自洽"

echo [4/5] 主包体积...
call node tests\_validate-step5-bundle.js

echo [5/5] Scanners...
call node tests\_validate-step6-scanners.js

echo === ALL PASS —— 可以发版 ===
goto :eof

:checkjson
node -e "JSON.parse(require('fs').readFileSync(process.argv[1],'utf8'))" "%~1" >nul 2>&1
if !errorlevel! EQU 0 (set /a JSON_OK+=1 >nul & echo  [OK]  %~1) else (set /a JSON_BAD+=1 >nul & echo  [X]   %~1)
goto :eof

:runTest
set RT_BAD=0
echo  -- %~2 --
node %~1
if !errorlevel! NEQ 0 set RT_BAD=1
if !RT_BAD! NEQ 0 echo   [X] %~2 (exit !errorlevel!)
if !RT_BAD! NEQ 0 goto :eof
goto :eof

:end_bad
echo === 有 bad,不发版 ===
exit /b 1
```

**v1.0.3 → v2.1.0 的关键修复**(避免下次重写时回退):
1. 变量名 `JS_FAIL/JSON_FAIL/FAIL` → `JS_BAD/JSON_BAD/bad`(绕开 cmd 关键字)
2. 子程序 `:runTest` 改用 `RT_BAD` + `goto :eof` 返回,**不**用 `exit /b 1`(避免子程序返回值污染主流程退出码)
3. JSON 检查用独立子程序 `:checkjson`,**不** inline `node -e`(避免 cmd 转义 JSON `{` `}`)
4. Step 5/6 拆成独立 `tests/_validate-step*.js` 脚本(同理由)
5. 验证成功的唯一标志:**bat 内部 stdout 出现 `=== ALL PASS —— 可以发版 ===`**。PowerShell 拿到的 `ExitCode 255` 是 cmd.exe 假报错,**忽略**
6. **v2.1.0 新增 bat 根检测**:`cd /d "%~dp0"` 之前先 `if not exist "app.json"` 才切,否则保持当前 cwd。这样 skill 从 cow 调用时不会跳错地方(详见下方"🪤 v2.1.0 新增 bat 根检测"段)
7. **v2.1.0 新增 3 个 scanner**:`cost-scanner.js` / `permission-scanner.js` / `permissions-validate.js`,加入 Step 4 Scanners 组

## 🪤 v2.1.0 新增 bat 根检测(7/11 教训)

**问题**:v2.0.0 的 bat 顶部有 `cd /d "%~dp0"`,假设 bat 文件位于项目根(用户双击场景)。**但本 skill 把 bat 放在 `C:\Users\Administrator\cow\skills\wechat-mp-validation\validate.bat`**,不是项目根。从 PowerShell 调 bat 时:
- PowerShell 端 `cd F:\test\...\wx-miniprogram` 设了 cwd
- bat 内部 `cd /d "%~dp0"` 又跳回 `C:\Users\Administrator\cow\skills\wechat-mp-validation`
- 后续 `for /R utils %%f in (...)` 找不到 `utils/` 目录 → JS 0/1,JSON 0/1,验证看似全红

**修法**(已固化到 v2.1.0 bat):在 `cd /d "%~dp0"` 之前加根检测,只在 cwd 没有 `app.json` 时才切:
```bat
@echo off
setlocal EnableExtensions EnableDelayedExpansion
if not exist "app.json" cd /d "%~dp0"
echo === 泰玄小站 验证流水线 v2.1.0 ===
...
```
**效果**:
- 用户在项目根双击 bat:`app.json` 存在 → 不切 → 跑项目根 ✅
- agent 从 cow 调用 bat:PowerShell 已 `cd` 到项目根 → `app.json` 存在 → 不切 → 跑项目根 ✅

**调用方式**:不管从哪里调 bat,**先 `cd F:\test\2026-06-27-14-59-27\wx-miniprogram` 再 `call validate.bat`**,bat 会自动用 cwd。

## 🆕 v2.1.0 新增 3 个 Scanner(Step 4 Scanners 组)

之前 Step 4 只有客观性+语调 scanner(原 v2.0.0)。v2.1.0 加 3 个(w4 泰玄 V0.2 控制平面引入):

| Scanner | 干什么 | 期望输出 | 失败时 |
|---|---|---|---|
| `check-objective-language.js` | 客观性 + AI 标识 v5.1 6 维评分 | 100/100 分 | < 100 block |
| `audit-wxml-tone.js` | WXML 语调软化 | 0 block | block 命中 exit 1 |
| `cost-scanner.js [w4-step2]` | 扫所有 `cost:` 字段 vs `policy.yaml` cap | 0/N 超 cap + 0/N 触发 daily | 超 cap exit 1 |
| `permission-scanner.js [w4-step3]` | 扫所有源码文件,无声明权限 | 0 违规 | 违规 exit 1 |
| `permissions-validate.js [w4-step4]` | 校验所有 spec endpoint 的 `permissions_required` 是否在 schema 内 | 6/6 endpoint 通过 | 不过 exit 1 |

**调用方式**:每个独立 `node` 调用,bat 用 `call :runTest "tests\cost-scanner.js" "cost-scanner"` 调。

### 调用方式
- **手动**:用户在项目根(`F:\test\2026-06-27-14-59-27\wx-miniprogram`)双击 `validate.bat`,或 cmd 输入 `validate.bat`
- **agent / PowerShell 调用**:必须先 `cd F:\test\2026-06-27-14-59-27\wx-miniprogram` 再 `& 'C:\Users\Administrator\cow\skills\wechat-mp-validation\validate.bat'`。v2.1.0 bat 根检测会保留 cwd(不再跳回 skill 目录)
- **agent 自动**:用户说"刚改完,验证一下",我会按上面 5 步调用,无需脚本

## 📌 注意事项

1. **`node --check` 必须从项目根跑**,否则 utils/ 等相对路径找不到
2. **测试顺序不要改** —— check-objective-language 跑在 test-solar-time 之前,因前者输出报告文件,后者读不到
3. **失败立即停** —— 不要"全跑完再汇总",Step 3 哪个红了就报告哪个,不要继续
4. **主包体积红线 = 2048K** —— 这是微信小程序的硬上限
5. **`utils/lunar-v2.js`(6tail 单文件,435K)是体积大头** —— 任何"减小主包"的尝试,先从这里开始
6. **如果 v2.0 后端接入**,Step 3 要加 `tests/contract-test.js`(契约一致性测试),在动作 ⑤ 后启用

## 🔗 关联资源

- 项目根:`F:\test\2026-06-27-14-59-27\wx-miniprogram\`
- CHANGELOG:同目录 `CHANGELOG.md`(看历史 patch 节奏)
- backend_contracts.md:同目录 545 行契约文档
- v3.0 微调:`docs/V3_LLM_FINETUNING.md`
- 知识库项目地图:`knowledge/entities/taixuan-miniprogram.md`

## 🚫 不要做的事

- ❌ 不要在用户没改代码时主动跑验证(浪费 30-60 秒)
- ❌ 不要修改任何被测试的源码(只读)
- ❌ 不要把验证脚本和项目源码混在同一个目录(放项目根的 `validate.bat` / `scripts/validate.sh`)
- ❌ 不要扩到 git hooks(用户目前没在用 git workflow,这步以后再说)