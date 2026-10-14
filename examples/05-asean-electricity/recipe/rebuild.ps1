param(
    [string]$PythonLauncher = (Join-Path $env:USERPROFILE '.codex/workbenches/codex-local/Invoke-CodexPython.ps1'),
    [string]$NodeExe = (Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'),
    [string]$ModuleDir = (Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules'),
    [string]$Browser = (Join-Path $env:ProgramFiles 'Google/Chrome/Application/chrome.exe'),
    [string]$OutputDir = (Join-Path $PSScriptRoot '../rebuilt')
)
$ErrorActionPreference = 'Stop'
if ($PSVersionTable.PSVersion -lt [version]'7.3') { throw 'Requires PowerShell 7.3 or later.' }
foreach ($runtimePath in @($PythonLauncher,$NodeExe,$ModuleDir,$Browser)) {
    if (-not (Test-Path -LiteralPath $runtimePath)) { throw "Existing runtime not found: $runtimePath. Pass the corresponding parameter; this recipe does not download dependencies." }
}
$sourceDir = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../source')).Path
& $PythonLauncher (Join-Path $PSScriptRoot 'analyze_build.py') --source $sourceDir --out $OutputDir
if ($LASTEXITCODE -ne 0) { throw 'Source calculation / HTML build failed.' }
& $NodeExe (Join-Path $PSScriptRoot 'export_web.mjs') --input (Join-Path $OutputDir 'energy-editorial.vi.html') --out (Join-Path $OutputDir 'previews') --module-dir $ModuleDir --browser $Browser --widths '1280,390,360' --min-essential 16 --pdf (Join-Path ([IO.Path]::GetFullPath($OutputDir)) 'energy-editorial.vi.pdf')
if ($LASTEXITCODE -ne 0) { throw 'Browser export or declared display checks failed; inspect previews/browser-export.json.' }
& $PythonLauncher (Join-Path $PSScriptRoot 'verify_outputs.py') --source $sourceDir --out $OutputDir --receipt (Join-Path $OutputDir 'previews/browser-export.json')
if ($LASTEXITCODE -ne 0) { throw 'Independent calculations / output object checks failed.' }
Write-Output "Rebuilt offline outputs: $([IO.Path]::GetFullPath($OutputDir))"
