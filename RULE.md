# RULE.md - Workspace Rules

This folder is your home. Treat it well.

## Workspace Directory Structure

```
~/cow/
├── AGENT.md          # Identity and soul
├── USER.md           # User basic info (static)
├── RULE.md           # Workspace rules (this file)
├── MEMORY.md         # Long-term memory index (auto-loaded at session start)
│
├── memory/           # Daily conversation memory
│   └── YYYY-MM-DD.md # Daily events, progress, notes
│
├── knowledge/        # Structured knowledge base
│   ├── index.md      # Knowledge catalog (must maintain)
│   ├── log.md        # Knowledge operation log
│   └── <subdir>/     # Created on demand
│
├── skills/           # Skills
├── websites/         # Web artifacts
└── tmp/              # System temp files
```

## Memory System

Every conversation is fresh; memory files keep you continuous.

### Brain Long-term: `MEMORY.md`
- Auto-loaded at session start
- Core facts, preferences, decisions, important people, lessons
- Stay concise (<200 lines)

### Daily Memory: `memory/YYYY-MM-DD.md`
- Daily events, progress, raw conversation log

### Write It Down - Don't "Keep It In Mind"
- Memory is limited. Write to file.
- "I will remember" doesn't survive session restart; files do.

## Knowledge System

`knowledge/` is your structured knowledge base, accumulates over time.
Cross-reference pages via markdown links.

## Safety

- Never leak API keys etc.
- Don't run destructive commands without asking
- Ask if in doubt

---

## Windows / PowerShell Operation Iron Rules

### 1. Delete Only After Verification (2026-07-10 lesson)
**Do NOT batch-delete zips immediately after extraction.** First run found
that `ExtractToDirectory` silently failed for 5 projects after bulk delete.
Correct order: extract → verify each destination non-empty → verify passed
→ THEN delete source. Backup to `tmp/<backup>-<date>/` for 7-day rollback.

### 2. `ExtractToDirectory` 3rd Parameter is `Encoding` not bool
```python
# WRONG: passes bool as Encoding → silent failure
ZipFile::ExtractToDirectory($src, $dst, $true)

# CORRECT: manual loop + ExtractToFile
```

### 3. PowerShell UTF-8 Encoding Trap (2026-07-11)
PowerShell 5.x defaults to GBK; scripts written with UTF-8 without BOM
get mangled. Two fixes:
- A: Write with `New-Object System.Text.UTF8Encoding $True` (force BOM)
- B: Install `pwsh` and use `pwsh -File` instead of `powershell -File`

### 4. Windows 写 bash 脚本必须 LF 行尾(2026-07-13 教训)
**Symptom**: Linux 跑 Windows 写的 .sh → `': $'\r': command not found` 而且 `sleep: invalid time interval`。
**Root cause**: Write tools 默认写 CRLF(\r\n),bash 在 Linux 上不能处理 \r。
**Fix**: 任何从 Windows 写到 ECS 跑的 .sh 必须用 `sed -i 's/\r$//'` 转 LF,或用 Python 二进制写时强制 `\n`。
**预防**:写 .sh 时 check `b'\r\n' not in data`,上传前必转 LF。

### 4. PowerShell subprocess + emoji → UnicodeDecodeError (2026-07-11)
**Symptom**: PowerShell 跑 Python subprocess 抓 `r.stdout` 看输出时,含 emoji
字符触发 `UnicodeDecodeError`。Python 自己用 `open(..., encoding='utf-8')`
**写文件没事**,只在 shell 端读 stdout 时炸。
**Root cause**: PowerShell 5.x console 默认 GBK,Python stdout 也走 console
encoding,emoji(很多 U+1F000+ 字符)超出 GBK 码位。
**Fix**: 跑 Python 前先设 `$env:PYTHONIOENCODING = "utf-8"`。**只影响 stdout
抓取,文件 I/O 永远用 explicit encoding="utf-8" 不受影响。**

---

## Environment Variable Doors (2026-07-11)

### Trap 1: `env_config` does NOT write to OS env
**Symptom**: `env_config set OPENAI_API_KEY=xxx` shows OK in `env_config list`,
but Python subprocess sees `os.environ.get('OPENAI_API_KEY') = None`.

**Root cause**: `env_config` stores in hermes-agent **process memory**
(internal config + ram), NOT in OS environment variables. When Python
`subprocess` starts, it only inherits the OS env structure → cannot see
hermes-agent's internal memory.

**Diagnosis**:
1. `env_config get OPENAI_API_KEY` shows value → it's hermes-agent memory
2. But `python -c "import os; print(os.environ.get(...))"` shows MISSING → it's OS env

**Correct workarounds (pick one)**:
- **A: Shell `set "VAR=value"`** — both cmd shell + subprocess inherit correctly
- **B: In script body, `os.environ['VAR'] = '...'`** — known anti-pattern (hardcode
  in script), but guaranteed to prevent subprocess env lost

### Trap 2: When using `set VAR=value` (no quotes) — value TRIMS trailing space
**Symptom**: `URL can't contain control characters '/v1 /chat/completions'`
**Root cause**: Without quotes, `set VAR=value` keeps the value as-is.
Trailing space gets preserved → URL concatenation corrupts.
**Correct**: `set "VAR=value"` — quotes trim, URL stays clean

### Trap 3: env key naming mismatch — `OPENAI_*` vs `DEEPSEEK_*`
**Symptom**: OS env has `DEEPSEEK_API_KEY` (real key), but `OPENAI_API_KEY`
is MISSING. rr-responder/arxiv-tracker scripts read `OPENAI_*` env vars.
**Correct**: Either rename in OS env, OR have scripts fall back to
`DEEPSEEK_API_KEY` when `OPENAI_API_KEY` is missing.

### Anti-Pattern: hardcode keys in scripts
Found in production scripts: `os.environ['OPENAI_API_KEY'] = 'sk-***OPENAI-KEY-REVOKED***'` (key redacted, was found hardcoded — must use env var instead).
**Technically works but not healthy** — next key rotation requires script update.
Better: read from OS env (after `set "OPENAI_API_KEY=..."` in calling shell).

---

### 4b. SQLite `executescript` 不容错 ALTER TABLE(2026-07-13)
**Symptom**:`sqlite3.OperationalError: no such table: readings` 当 schema 里有 ALTER TABLE 时。
**Root cause**:`cursor.executescript()` 不像 `init_db()` 那样包 try/except,直接失败整个 script。
**Fix**:
- 数据库 init 必须用 Python 的 `init_db()`(已包 try/except),**不要** raw `sqlite3` CLI
- 或者在 schema 文件里加 `CREATE TABLE IF NOT EXISTS readings ...` + 用 try/except 包裹 ALTER
- 部署到 ECS 用 `python3 -c "import user_system; user_system.init_db()"` 而不是 `sqlite3 data.db < schema.sql`

### 5. PowerShell 5.x ASCII-only 才稳(2026-07-13)
**Symptom**: PowerShell 5.x 解析 `.ps1` 时,如果注释或字符串里有 emoji(✗ ℹ 等)或非 ASCII 中文,
parser 直接报"字符串缺少终止符: " ",整个脚本根本没跑。
**Root cause**: PowerShell 5.x 默认 GBK codepage,多字节字符边界错位,parser 在某一行提前终止。
**Fix**: **PowerShell 脚本全部 ASCII**。注释也用英文。
- 允许:变量名/字符串/注释**纯英文 + ASCII 符号**
- 不允许:emoji(✓ ✗ ℹ ⚠ ❌ 等)、中文注释、中文字符串
- 真要中文:用 PowerShell 7+(`pwsh`),或把中文存到独立 `.txt` 文件再 Read

### 6. PowerShell `Add-Content` 默认 GBK → UTF-8 文件被污染(2026-07-11)

**Symptom**: 给 UTF-8 文件 append 中文后,文件变成混合编码(GBK 字节 + UTF-8 字节),
后续读全乱码,emoji 变 `?`。

**Root cause**: PowerShell 5.x `Add-Content` 默认走系统 codepage(GBK),不感知文件原编码。

**Fix**: append 含中文/emoji 必用 Python:
```python
open('foo.md', 'a', encoding='utf-8').write('中文内容\n')
```
或显式 `Add-Content -Encoding UTF8`(PowerShell 7+) / `-Encoding UTF8` + BOM(PowerShell 5.x 不稳,**不推荐**)。

**适用范围**: 任何 .md / .yaml / .json / .tex 文件 append,**不仅 log.md**。

**真实案例**(本轮踩中): `knowledge/log.md` append w5 完工段后,Python `errors='replace'` 解码才能继续——> 后续所有 UTF-8 写也要小心。

---

### 6. Python 装饰器从下往上应用(2026-07-12 教训)

**Symptom**:重构 Flask 路由抽 helper 时,把 `@app.route(...)` 紧贴的下一个函数被错误地装饰。

**陷阱示例**:
```python
# 错误:@app.route 装饰了 _validate_question,而不是 reading_stream
@app.route("/reading_stream", methods=["POST"])
def _validate_question(...):  # ← 实际被装饰
    ...
def reading_stream(...):
    ...
```

**Root cause**:Python 装饰器在模块加载时**从下往上**应用,中间插入的 helper 函数会"偷走"装饰器。

**正确顺序**:
```python
# 1. 先写 helper(无装饰器)
def _validate_question(...): ...

# 2. 再写 @app.route + 主函数
@app.route("/reading_stream", methods=["POST"])
def reading_stream(...):
    ...
```

**强 gate(写完路由必校验)**:
```bash
python -c "import app; print([str(r) for r in app.app.url_map.iter_rules()])"
```

**或者用临时脚本**(`tmp/_check_routes.py`):用 ast 模块扫所有 `@app.route` 装饰的函数名是否对得上 `@app.route` 紧贴的下一行。

**真实案例**(7/12 23:30):重构 reading_stream 时,`_validate_question` 被装饰成 reading_stream 的视图函数,curl 测试发现 /reading_stream 路由名 → _validate_question() — 立刻发现 + 修复。

---

### Trap 7: edit tool writes Chinese as GBK into UTF-8 file(2026-07-13)

**Symptom**: After running `edit` tool on a `.md` file with Chinese content, the file becomes **mixed-encoding garbage** when viewed via PowerShell `Get-Content` or `bash cat`. But file bytes read via `[System.IO.File]::ReadAllBytes + Encoding.UTF8.GetString` are perfectly correct.

**Root cause**: `edit` tool's write path may not explicitly specify UTF-8 encoding on the underlying file stream. The file ON DISK is actually intact UTF-8 — **the "garbled" display is a viewer-side artifact** (PowerShell 5.x `[Console]::OutputEncoding` defaults to GBK).

**Diagnosis** (verify before fixing):
```powershell
$bytes = [System.IO.File]::ReadAllBytes('memory\2026-07-13.md')
$text = [System.Text.Encoding]::UTF8.GetString($bytes)
Write-Host ('Bytes: ' + $bytes.Length + ' / Chars: ' + $text.Length)
Write-Host $text.Substring($text.Length - 200)
```

If file shows perfect Chinese in the diagnostic output → **file is fine**, just the viewer is wrong.
If file shows actual garbage bytes (non-UTF8 sequences) → need to rewrite via Python or write tool.

**Prevention**:
- Before/after every `edit` to a Chinese-heavy file, run the diagnostic above
- If you see "garbled" output via `Get-Content`, **don't panic-rewrite** — first check whether it's a viewer issue
- If real corruption (file bytes are GBK), fix with:
  ```python
  content = open('foo.md', encoding='utf-8', errors='replace').read()
  open('foo.md', 'w', encoding='utf-8').write(content)
  ```

**Real case (2026-07-13 21:50)**: After editing `memory/2026-07-13.md` to add "21:50 - T11.1 handoff patch" section, `bash` showed `?? vs failure_taxonomy??` etc. Ran the diagnostic — file was 14269 bytes / 10482 chars, perfectly intact UTF-8. The "garbage" was just PowerShell console encoding. No fix needed.

**Anti-pattern**: If the user sees "garbled" Chinese and the agent immediately re-`write`s the file from the garbled output, **the agent just overwrote good UTF-8 with garbage**. Always diagnose first.

---

### Trap 8: Mock URL 设计 — 前端必须 fetch API,绝不让浏览器 redirect(2026-07-13)

**Symptom**: v2.0 Phase 7 Stripe 订阅 mock 实现,前端 JS 写
`window.location.href = "/api/v2/subscription/mock_confirm?session_id=xxx"`,
浏览器 GET 这个 URL → Flask 路由表里这个 endpoint 是 **POST only** → **404**。

**Root cause**: 把"假接口"设计成完整 URL 让浏览器跳转,但 API endpoint 默认 POST,
浏览器 GET 命中 → 路由 404。

**正确 mock 模式**(适用于所有第三方服务 mock:支付/邮件/短信/扫码):
```javascript
// WRONG: redirect 到 mock URL(浏览器 GET → 404)
window.location.href = mock_url

// RIGHT: fetch API(协议对齐)
const res = await fetch('/api/v2/subscription/mock_confirm', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({session_id: xxx})
})
const data = await res.json()
if (data.success) { /* 显示成功 UI */ }
```

**铁规**:
- ✅ Mock 路径必须和真路径**同 method + 同 body schema**
- ✅ 前端永远 `fetch()`,绝不 `window.location.href`
- ❌ 绝不让浏览器 redirect 到 `/api/...` 路径

**适用范围**: 任何 mock/stub 设计(支付网关 / SMTP / SMS / OAuth / QR 扫码回调)

**真实案例**(2026-07-13 22:15): v2.0 Phase 7 Stripe mock 第一次翻车就是这个,后改 fetch POST
立即通,本地 8/8 + ECS 6/6 全过。

**配套原则**(已写进 AGENT.md §"任何 API 集成默认用 mock 桩 + 真实 stub 模式"):
- dev 模式默认返回 mock 完整链路(无需外部凭据)
- 真接只需设环境变量 + 重启 + import 实际包
- **15 min 切换** = 标准动作

---

### Trap 9: Windows 写 PEM 文件默认 CRLF → cryptography 解析失败(2026-07-14)

**Symptom**: 把支付宝/微信/etc 私钥写到 `.pem` 文件后,`cryptography` / `OpenSSL` 报 `Could not deserialize key data` 或 `unexpected tag`。文件 cat 看着正常,base64 解码长度也对(比如 1218 字节 DER),但解析就是失败。

**Root cause**: PEM 标准 RFC 7468 要求 **LF only**(`\n`)。Windows 写文件默认 **CRLF**(`\r\n`),`\r` 被当作 base64 数据的一部分,解码后 DER 头错位 → ASN.1 解析失败。

**Fix**: 写 PEM 文件时强制 LF 行尾。
```python
content = content.replace('\r\n', '\n').replace('\r', '\n')
open('app_private_key.pem', 'w', encoding='utf-8', newline='').write(content)
# 或者写完 sed 转:sed -i 's/\r$//' app_private_key.pem
```

**Verification** (写完必查):
```python
data = open('key.pem', 'rb').read()
print('CRLF' if b'\r\n' in data else 'LF-only')
```

**适用范围**: 任何 `.pem` / `.key` / `.crt` / 私钥 / 证书文件 — **不只是 .sh**(Trap 4 只覆盖 .sh,这个补 PEM)。

**真实案例**(2026-07-14): 支付宝沙箱私钥写入 `.pem` 后 cryptography 报 `unexpected tag`,DER 前 16 字节看着对(`308204be 020100 300d...`),但 CRLF 里的 `\r` 污染 base64 → 转 LF 后立即通。

---

### Trap 10: 支付宝/微信/银行 私钥大多是 PKCS#8,不是 PKCS#1(2026-07-14)

**Symptom**: PEM 文件头是 `-----BEGIN RSA PRIVATE KEY-----`(PKCS#1 风格),但用 `cryptography` / `OpenSSL` 解析时格式不被识别。或者反过来:头是 `-----BEGIN PRIVATE KEY-----`,但代码用 PKCS#1 的 `RSA.importKey()` 解析失败。

**Root cause**: 主流支付平台(支付宝、微信支付、银联等)现在发的私钥都是 **PKCS#8**(`-----BEGIN PRIVATE KEY-----`),不是老的 PKCS#1(`-----BEGIN RSA PRIVATE KEY-----`)。但平台文档/示例常混用两种头,**沙箱后台展示的标题也可能跟实际内容不一致**(支付宝沙箱展示 PKCS#1 头,实际给的是 PKCS#8 内容)。

**识别方法**: 看 DER 头部字节:
- **PKCS#8**: `30 82 xx xx 02 01 00 30 0d 06 09 2a 86 48 86 f7 0d 01 01 01 ...`(有 AlgorithmIdentifier OID)
- **PKCS#1**: `30 82 xx xx 02 01 00 02 82 xx xx ...`(序列后直接进 modulus 整数)

**Fix**: 拿到平台私钥后,**不要相信显示的 PEM 头**,直接用 Python `cryptography.hazmat.primitives.serialization.load_pem_private_key()` 让它自动识别格式;或者检查 DER 头字节后改头。

**Python 加载代码**(同时支持 PKCS#1 / PKCS#8):
```python
from cryptography.hazmat.primitives import serialization
with open('app_private_key.pem', 'rb') as f:
    key = serialization.load_pem_private_key(f.read(), password=None)
```

**适用范围**: 任何第三方支付/银行/政务平台私钥加载场景。

---

### Trap 11: 私钥/敏感配置绝不能 push GitHub(2026-07-14)

**Symptom**: `tools/upload_phaseN.py` 推代码时,把 `.env.local` / `*.pem` / `*_private_key*` / `*.key` 也推到了 GitHub master,导致私钥泄露到公开仓库。

**Root cause**: 通用 GitHub upload 工具为了简单,会遍历整个项目目录,**没有敏感文件过滤**。`fortune-web-v2/` 下任何 `.pem` / `.key` / `.env*` 默认都被 git tracking → 推到 master = 公开。

**Fix**: upload 工具必须带**敏感词检测**(最低限度):
```python
SENSITIVE_PATTERNS = [
    'sk_live_', 'sk_test_', 'whsec_',         # Stripe
    '-----BEGIN RSA PRIVATE KEY-----',
    '-----BEGIN PRIVATE KEY-----',
    '-----BEGIN EC PRIVATE KEY-----',
    'APP_PRIVATE_KEY', 'SECRET_KEY', 'API_SECRET',
]
# 命中任一模式 → 跳过该文件 + warn
```

**部署原则**(强制):
- ✅ 代码 / 配置 schema / 文档 → GitHub
- ❌ `.env.local` / `*.pem` / `*_private_key*` / 任何含明文密钥的文件 → **永远不走 GitHub**
- ✅ 私钥部署到 ECS 用 `scp` 或 `cat > file <<EOF` 在 Workbench 手工写
- ✅ 上传工具加 `.gitignore` 检查 + 敏感词检测(双保险)

**真实案例**(2026-07-14): v2.0 Phase 8(支付宝)部署时,3 个代码文件推 GitHub,2 个私钥文件(`.env.local` + `app_private_key_sandbox.pem`)**绝不能推** — 手工在 ECS Workbench 写。

---

### Trap 12: 上传工具敏感词检测误杀(2026-07-14)

**Symptom**: `upload_phase8.py` 推 `subscriptions_routes.py` 时被敏感词检测**跳过**,但文件里**不含真密钥** — 只是注释里提到 `whsec_*` 字样描述 Stripe webhook 签名格式。

**Root cause**: 敏感词匹配只看**字符串包含**,不看**是不是真值**(注释 / 字符串字面量 / docstring 都会命中)。`whsec_*` 出现在注释里 ≠ 出现真密钥。

**Fix**: 敏感词检测要分级:
- **HIGH 风险**(sk_live_ + 32 字符 / 真 RSA 私钥 / 真 PEM body) → 直接 skip
- **LOW 风险**(whsec_ 字样在注释 / 文档示例 / docstring) → 不 skip,只 warn + 让用户确认

简单实现:
```python
def is_real_key(content, pattern):
    # 检查是否在字符串/赋值上下文,不在注释/docstring
    for line in content.split('\n'):
        if pattern in line:
            stripped = line.strip()
            if stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
                continue  # 注释跳过
            return True  # 真值
    return False
```

**预防**: 写上传工具时,敏感词检测**默认只 skip HIGH 风险 + 注释里全部 warn 不 skip**。宁可误放(让用户人工审核),不要误杀(用户没意识到文件没推成功)。

---

### Trap 13: `.env.local` 多行 PEM 难处理 → 拆出独立 .pem 文件 + path 引用(2026-07-13)

**Symptom**: 想把 PEM 私钥放 `.env.local`,用 `\n` 转义多行。结果:
1. Python `os.environ` 把 `\n` 当字面字符而非真换行
2. 支付宝 SDK 拿到假换行的私钥 → 签名错误
3. bash 解析 `.env.local` 时多行字符串炸

**Root cause**: `.env` 文件本来设计给单行 K=V,多行值(尤其是 PEM)需要 quote + 转义,跨语言/跨 shell 兼容性差。

**Fix**: **拆出独立 .pem 文件 + .env.local 只存路径**:
```ini
# .env.local -- 只存路径
TAIXUAN_ALIPAY_APP_PRIVATE_KEY_PATH=app_private_key_sandbox.pem

# 公钥可以留 .env.local(因为不长,几十字节)但要 multi-line quoted
TAIXUAN_ALIPAY_ALIPAY_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
... 实际多行内容 ...
-----END PUBLIC KEY-----
"
```

**代码加载**(用 path):
```python
def _load_private_key() -> str:
    key_path = os.environ.get("TAIXUAN_ALIPAY_APP_PRIVATE_KEY_PATH", "")
    if key_path and os.path.exists(key_path):
        with open(key_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return os.environ.get("TAIXUAN_ALIPAY_APP_PRIVATE_KEY", "")
```

**适用范围**: 任何 PEM 私钥 / 长证书 / 大段 base64 内容塞 `.env` 场景。

**真实案例**(2026-07-13): v2.0 Phase 8 支付宝私钥最初想塞 `.env.local`,试了 3 种转义方式都失败(单行 `\n`、multi-line quoted、base64 转码都翻车)→ 拆 `.pem` 文件 + path 引用,5 min 解决。
