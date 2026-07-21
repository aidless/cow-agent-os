#requires -Version 5.1
# _record_install.ps1 —— 主动安装 skill 的幂等记录脚本
# 用法: .\installed\_record_install.ps1 -SkillName "arxiv-tracker" -Reason "TMLR 论文每日抓取" -SourceUrl "https://..."

param(
    [Parameter(Mandatory=$true)] [string]$SkillName,
    [string]$Reason = "",
    [string]$SourceUrl = "",
    [string]$SourcePath = ""
)

$ErrorActionPreference = 'Stop'

# 验证 skill name (跟 cc-switch 命名规则一致)
if ($SkillName -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]*$') {
    Write-Host "ERROR: Skill name '$SkillName' contains invalid characters" -ForegroundColor Red
    exit 1
}

# 检查 cc-switch 是否真有这个 skill (1273 active 之一)
$CcSwitch = "$env:USERPROFILE\.cc-switch\skills\$SkillName"
$Claude   = "$env:USERPROFILE\.claude\skills\$SkillName"

if (-not (Test-Path $CcSwitch)) {
    Write-Host "WARNING: $SkillName not in cc-switch. Still recording but you may want to install it first." -ForegroundColor Yellow
}

$Today = Get-Date -Format 'yyyy-MM-dd'
$InstalledDir = Join-Path $PSScriptRoot ''
$RecordFile   = Join-Path $InstalledDir "$SkillName.md"

# 幂等: 如果已存在, 仅更新 Reasons/Urls(append), 不重置 install 日期
if (Test-Path $RecordFile) {
    $OldContent = Get-Content $RecordFile -Raw
    $AppendLine = "`n- $(Get-Date -Format 'yyyy-MM-dd HH:mm') 追加记录: $Reason"
    $NewContent = $OldContent.TrimEnd() + $AppendLine
    Set-Content -LiteralPath $RecordFile -Value $NewContent -Encoding UTF8
    Write-Host "Updated: $RecordFile" -ForegroundColor Green
} else {
    $Content = @"
# $SkillName

- **首次记录日**: $Today
- **来源 URL**: $(if ($SourceUrl)  { $SourceUrl }  else { '(未填)' })
- **来源路径**: $(if ($SourcePath) { $SourcePath } else { '(未填)' })
- **为什么装**: $Reason
- **symlink 路径**: $Claude → $CcSwitch
- **卸载步骤**: 
  1. ``rm $Claude``
  2. ``rm $RecordFile``

## 使用记录
- $Today 首次安装
"@
    Set-Content -LiteralPath $RecordFile -Value $Content -Encoding UTF8
    Write-Host "Created: $RecordFile" -ForegroundColor Green
}

# 列出当前所有主动安装的 skill
Write-Host "`n=== 当前 installed/ 目录 ===" -ForegroundColor Cyan
Get-ChildItem $InstalledDir -Filter "*.md" | Where-Object { $_.Name -ne "README.md" } | Select-Object Name, Length | Format-Table -AutoSize