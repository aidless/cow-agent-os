/**
 * tests/_validate-step2-json.js
 *
 * v1.0.4 · 2026-07-11
 * 验证流水线 Step 2 的独立 runner —— JSON 语法扫描
 * 排除目录:tmp/、.githooks/、.git/、node_modules/
 * 排除文件:{try{JSON.parse(d) (历史遗留的 0 字节怪文件)
 *
 * 用法:node tests/_validate-step2-json.js
 */
const fs = require('fs');
const path = require('path');

const SKIP_DIRS = new Set(['node_modules', 'tmp', '.githooks', '.git']);
const SKIP_FILES = new Set(['{try{JSON.parse(d)']);

function walk(dir) {
  const results = [];
  if (!fs.existsSync(dir)) return results;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (SKIP_DIRS.has(entry.name)) continue;
      results.push(...walk(p));
    } else if (path.extname(entry.name) === '.json' && !SKIP_FILES.has(entry.name)) {
      results.push(p);
    }
  }
  return results;
}

const files = walk('.');
let ok = 0;
let fail = 0;
const failures = [];
for (const f of files) {
  try {
    JSON.parse(fs.readFileSync(f, 'utf8'));
    ok++;
  } catch (e) {
    failures.push(`  ❌ ${f}: ${e.message}`);
    fail++;
  }
}
if (failures.length > 0) {
  console.log(failures.join('\n'));
}
console.log(`   JSON 检查: ${ok} OK / ${fail} FAIL (排除 tmp/、.githooks/、怪文件)`);
process.exit(fail > 0 ? 1 : 0);