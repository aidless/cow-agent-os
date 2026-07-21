<#
TaiXuan validation pipeline v1.0.10 (PowerShell port)

Root: F:\test\2026-06-27-14-59-27\wx-miniprogram
Usage: PowerShell -ExecutionPolicy Bypass -File validate.ps1

v1.0.10 (2026-07-11):
  - Use Start-Process -WaitForExit for sub-process exit code (avoids PS & call race)
  - ASCII-only (avoids PS 5.x UTF-8 parse bug with non-BOM Chinese)
  - 5 steps 1:1 mirroring validate.bat v1.0.5
  - Replaces bat to kill cmd /c "XXX was unexpected at this time." false error
#>

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $ScriptDir

Write-Host ""
Write-Host "=== TaiXuan validation pipeline v1.0.10 ==="
Write-Host "=== Root:$(Get-Location) ==="
Write-Host ""

# Helper: run node script, return exit code, print stdout
function Run-Node {
    param([string]$Cmd, [switch]$NoStream)
    $p = Start-Process -FilePath 'node' -ArgumentList $Cmd -NoNewWindow -Wait -PassThru -RedirectStandardOutput "$env:TEMP\_validate_out.tmp" -RedirectStandardError "$env:TEMP\_validate_err.tmp"
    if (Test-Path "$env:TEMP\_validate_out.tmp") {
        Get-Content "$env:TEMP\_validate_out.tmp" | Write-Host
        Remove-Item "$env:TEMP\_validate_out.tmp" -Force
    }
    if (Test-Path "$env:TEMP\_validate_err.tmp") {
        Get-Content "$env:TEMP\_validate_err.tmp" | Write-Host
        Remove-Item "$env:TEMP\_validate_err.tmp" -Force
    }
    return $p.ExitCode
}

function Step1JsSyntax {
    Write-Host "[1/5] JS syntax check..."
    $jsOk = 0
    $jsBad = 0
    $jsDirs = @('utils', 'pages', 'components', 'tests')
    foreach ($dir in $jsDirs) {
        if (-not (Test-Path $dir)) { continue }
        Get-ChildItem -Path $dir -Recurse -Filter *.js | ForEach-Object {
            $p = Start-Process -FilePath 'node' -ArgumentList @('--check', $_.FullName) -NoNewWindow -Wait -PassThru
            if ($p.ExitCode -eq 0) { $jsOk++ } else { $jsBad++ }
        }
    }
    if (Test-Path 'app.js') {
        $p = Start-Process -FilePath 'node' -ArgumentList @('--check', 'app.js') -NoNewWindow -Wait -PassThru
        if ($p.ExitCode -eq 0) { $jsOk++ } else { $jsBad++ }
    }
    Write-Host "  JS check: $jsOk OK / $jsBad BAD"
    if ($jsBad -gt 0) {
        Write-Host "  X Step 1 BAD"
        return 1
    }
    Write-Host "  OK Step 1 PASS"
    return 0
}

function Step2JsonSyntax {
    Write-Host "[2/5] JSON syntax check..."
    $r = Run-Node 'tests\_validate-step2-json.js'
    if ($r -ne 0) { return 1 }
    Write-Host "  OK Step 2 PASS"
    return 0
}

function Step3Tests {
    Write-Host "[3/5] Tests..."
    $tests = @(
        @{ Cmd = "tests\run-lunar-test.js"; Label = "A accuracy" },
        @{ Cmd = "tests\test-solar-time.js"; Label = "C solar-time" },
        @{ Cmd = "tests\liupai-reader-test.js"; Label = "D 8-school + spec-vs-demo" },
        @{ Cmd = "tests\demo-typo-check.js"; Label = "F typo scan" },
        @{ Cmd = "tests\demo-readability-test.js"; Label = "G readability" },
        @{ Cmd = "tests\check-spec-coherence.js"; Label = "B2 spec coherence (specs/)" },
        @{ Cmd = "tests\lunar-lichun-test.js"; Label = "E lichun year switch" }
    )
    $testBad = 0
    foreach ($t in $tests) {
        Write-Host "  -- $($t.Label) --"
        $r = Run-Node $t.Cmd
        if ($r -ne 0) { $testBad++ }
    }
    if ($testBad -gt 0) {
        Write-Host "  X Step 3 BAD ($testBad tests failed)"
        return 1
    }
    Write-Host "  OK Step 3 PASS"
    return 0
}

function Step4Scanners {
    Write-Host "[4/5] Scanners..."
    $scanners = @(
        @{ Cmd = "tests\check-objective-language.js"; Label = "objective-language scanner" },
        @{ Cmd = "tests\audit-wxml-tone.js"; Label = "wxml-tone softener" }
    )
    $scanBad = 0
    foreach ($s in $scanners) {
        Write-Host "  -- $($s.Label) --"
        $r = Run-Node $s.Cmd
        if ($r -ne 0) { $scanBad++ }
    }
    if ($scanBad -gt 0) {
        Write-Host "  X Step 4 BAD"
        return 1
    }
    Write-Host "  OK Step 4 PASS"
    return 0
}

function Step5Bundle {
    Write-Host "[5/5] Bundle size..."
    $r = Run-Node 'tests\_validate-step5-bundle.js'
    return $r
}

$r = Step1JsSyntax; if ($r -ne 0) { Write-Host ""; Write-Host "=== Validation failed ==="; exit $r }
$r = Step2JsonSyntax; if ($r -ne 0) { Write-Host ""; Write-Host "=== Validation failed ==="; exit $r }
$r = Step3Tests; if ($r -ne 0) { Write-Host ""; Write-Host "=== Validation failed ==="; exit $r }
$r = Step4Scanners; if ($r -ne 0) { Write-Host ""; Write-Host "=== Validation failed ==="; exit $r }
$r = Step5Bundle; if ($r -ne 0) { Write-Host ""; Write-Host "=== Validation failed ==="; exit $r }

Write-Host ""
Write-Host "=== ALL PASS -- ready to ship ==="
exit 0