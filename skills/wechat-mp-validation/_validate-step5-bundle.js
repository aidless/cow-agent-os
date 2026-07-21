/**
 * tests/_validate-step5-bundle.js
 *
 * v1.0.4 · 2026-07-11
 * 验证流水线 Step 5 的独立 runner —— 主包体积检查
 * 红线:< 2MB = PASS,否则 FAIL
 *
 * 用法:node tests/_validate-step5-bundle.js
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const SCAN_DIRS = ['utils', 'pages', 'components', 'assets'];
const RED_LINE_KB = 2048;

let total = 0;
function walk(dir) {
  for (const f of fs.readdirSync(dir)) {
    const fp = path.join(dir, f);
    const s = fs.statSync(fp);
    if (s.isDirectory()) {
      walk(fp);
    } else {
      total += s.size;
    }
  }
}

for (const d of SCAN_DIRS) {
  const dp = path.join(ROOT, d);
  if (fs.existsSync(dp)) walk(dp);
}

const kb = (total / 1024).toFixed(0);
const pass = total / 1024 < RED_LINE_KB;
const icon = pass ? '✅' : '❌';
console.log(`   主包: ${kb}K ${icon} ${pass ? 'PASS < 2MB' : `FAIL ${kb}K > ${RED_LINE_KB}K 红线`}`);
process.exit(pass ? 0 : 1);