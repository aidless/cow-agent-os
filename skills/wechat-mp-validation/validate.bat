@echo off
:: ============================================================
:: 泰玄小站 · 验证流水线 v2.0.0 (2026-07-11 重构)
:: 项目根:F:\test\2026-06-27-14-59-27\wx-miniprogram
:: 用法:双击或 cmd 调用 validate.bat
::
:: v2.0.0 重构原因:
::   v1.0.5 用 ERR/BAD 替代 FAIL 仍触发 cmd parser 假报错
::   (xxx was unexpected at this time) — 因为 cmd 把单独成词的
::   ERR 当命令解析。**彻底解决**:bat 内禁用所有 cmd 保留字
::   作为 echo 参数 (FAIL/ERR/BAD/PASS/ON/OFF 等),用 [X]/[OK] 替代。
::
:: v1.x → v2.0 变更:
::   - Step 2/5 inline node 拆独立 .js 脚本(避开 cmd 嵌套引号转义)
::   - Step 3 增加 check-spec-coherence.js(spec 自洽性)
::   - Step 4 独立 scanner 分组(check-objective-language + audit-wxml-tone)
::   - :runTest 用 goto :eof + RT_OK 变量,不用 exit /b
::   - 所有 echo 禁用 cmd 保留字
:: v2.0 → v2.1.0 变更:
::   - Step 4 加 cost/permission/permissions-validate 3 个 PDP 控制平面 scanner
:: v2.1.0 → v2.2.0 变更:
::   - Step 4 加 tests\red-line-words.js(个人主体合规红线扫描器)
::   - 6 个 scanner:check-objective-language / audit-wxml-tone / cost / permission / permissions-validate / red-line-words
:: ============================================================
chcp 65001 >nul
setlocal EnableDelayedExpansion
:: v2.2.0 改进:Step 4 Scanners 5 → 6(加 tests\red-line-words.js · 个人主体合规红线扫描器)
:: (优先当前 cwd 含 app.js;否则跳到 bat 所在目录的父级 — 即项目根)
if exist "app.js" (
    rem 已在项目根,无需 cd
) else (
    rem 假设 bat 在 skills/wechat-mp-validation/,需要上溯两级到项目根
    :: 但更稳的方式:bat 在项目根时 %~dp0 = 项目根
    :: bat 在 skill 时 %~dp0 = skill 所在目录
    cd /d "%~dp0"
)

echo.
echo === 泰玄小站 验证流水线 v2.2.0 ===
echo === 项目根:%CD% ===
echo.

:: ============================================================
:: Step 1 · JS 语法
:: ============================================================
echo [1/5] JS syntax check...
set JS_OK=0
set JS_PROBLEM=0
for /R utils %%f in (*.js) do (
  node --check "%%f" >nul 2>&1
  if !ERRORLEVEL! EQU 0 (set /a JS_OK+=1 >nul) else (set /a JS_PROBLEM+=1 >nul)
)
for /R pages %%f in (*.js) do (
  node --check "%%f" >nul 2>&1
  if !ERRORLEVEL! EQU 0 (set /a JS_OK+=1 >nul) else (set /a JS_PROBLEM+=1 >nul)
)
for /R components %%f in (*.js) do (
  node --check "%%f" >nul 2>&1
  if !ERRORLEVEL! EQU 0 (set /a JS_OK+=1 >nul) else (set /a JS_PROBLEM+=1 >nul)
)
for /R tests %%f in (*.js) do (
  node --check "%%f" >nul 2>&1
  if !ERRORLEVEL! EQU 0 (set /a JS_OK+=1 >nul) else (set /a JS_PROBLEM+=1 >nul)
)
node --check app.js >nul 2>&1
if !ERRORLEVEL! EQU 0 (set /a JS_OK+=1 >nul) else (set /a JS_PROBLEM+=1 >nul)

echo   JS 检查: !JS_OK! OK / !JS_PROBLEM! 个问题
if !JS_PROBLEM! GTR 0 (
    echo   [X] Step 1 —— 见上数字
    goto :end_problem
)
echo   [OK] Step 1 通过
echo.

:: ============================================================
:: Step 2 · JSON 语法
:: ============================================================
echo [2/5] JSON syntax check...
node tests\_validate-step2-json.js
if !ERRORLEVEL! NEQ 0 goto :end_problem
echo   [OK] Step 2 通过
echo.

:: ============================================================
:: Step 3 · 测试 (7 个核心 + B2 spec 自洽)
:: ============================================================
echo [3/5] Tests...
set TEST_PROBLEM=0
call :runTest "tests\run-lunar-test.js" "A 算法精度"
if "!RT_OK!"=="0" set TEST_PROBLEM=1
call :runTest "tests\test-solar-time.js" "C 真太阳时"
if "!RT_OK!"=="0" set TEST_PROBLEM=1
call :runTest "tests\liupai-reader-test.js" "D 8 派拼装 + spec-vs-demo"
if "!RT_OK!"=="0" set TEST_PROBLEM=1
call :runTest "tests\demo-typo-check.js" "F typo 扫描"
if "!RT_OK!"=="0" set TEST_PROBLEM=1
call :runTest "tests\demo-readability-test.js" "G 可读性"
if "!RT_OK!"=="0" set TEST_PROBLEM=1
call :runTest "tests\check-spec-coherence.js" "B2 spec 自洽性(specs/)"
if "!RT_OK!"=="0" set TEST_PROBLEM=1
call :runTest "tests\lunar-lichun-test.js" "E 立春换年"
if "!RT_OK!"=="0" set TEST_PROBLEM=1
if "!TEST_PROBLEM!"=="1" goto :step3_problem
echo   [OK] Step 3 通过
echo.
goto :step3_ok

:step3_problem
echo   [X] Step 3
goto :end_problem

:step3_ok

:: ============================================================
:: Step 4 · 扫描器 (6 个数据驱动 scanner,v2.2.0 加 red-line-words 个人主体合规红线)
:: ============================================================
echo [4/5] Scanners...
set SCAN_PROBLEM=0
echo   -- check-objective-language.js (合规禁词) --
node tests\check-objective-language.js
if !ERRORLEVEL! NEQ 0 set SCAN_PROBLEM=1
echo   -- audit-wxml-tone.js (语气软化) --
node tests\audit-wxml-tone.js
if !ERRORLEVEL! NEQ 0 set SCAN_PROBLEM=1
echo   -- cost-scanner.js (8 派 LLM token/cost 估算) [w4-step2] --
node tests\cost-scanner.js
if !ERRORLEVEL! NEQ 0 set SCAN_PROBLEM=1
echo   -- permission-scanner.js (endpoint/school/scene 白名单) [w4-step3] --
node tests\permission-scanner.js
if !ERRORLEVEL! NEQ 0 set SCAN_PROBLEM=1
echo   -- permissions-validate.js (v2.endpoints.json schema 校验) [w4-step4] --
node specs\acceptance\permissions-validate.js
if !ERRORLEVEL! NEQ 0 set SCAN_PROBLEM=1
echo   -- red-line-words.js (v1.0 个人主体合规红线) [w4-v1.0-step4] --
node tests\red-line-words.js
if !ERRORLEVEL! NEQ 0 set SCAN_PROBLEM=1
if "!SCAN_PROBLEM!"=="1" (
    echo   [X] Step 4 —— 见上方 block 命中
    goto :end_problem
)
echo   [OK] Step 4 通过
echo.

:: ============================================================
:: Step 5 · 主包体积
:: ============================================================
echo [5/5] 主包体积...
node tests\_validate-step5-bundle.js
if !ERRORLEVEL! NEQ 0 goto :end_problem

echo.
echo === ALL PASS —— 可以发版 ===
goto :eof

:runTest
echo   -- %~2 --
node %~1
if !ERRORLEVEL! NEQ 0 (
    echo   [X] %~2
    set RT_OK=0
) else (
    set RT_OK=1
)
goto :eof

:end_problem
echo.
echo === 验证未通过 —— 见上方 [X] ===
exit /b 1