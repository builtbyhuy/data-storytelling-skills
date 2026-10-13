#requires -Version 7.3
param(
 [string]$SourceDir='./source', [string]$BuildDir='./build', [string]$OutputDir='./generated',
 [string]$NodeExe='', [string]$NodeModules='', [string]$PythonExe='', [string]$PythonLauncher='', [string]$PresentationSkill=''
)
$ErrorActionPreference='Stop'
$profilePath=[Environment]::GetFolderPath('UserProfile')
$runtimeBase=Join-Path $profilePath '.cache/codex-runtimes/codex-primary-runtime/dependencies'
if(-not $NodeExe){$NodeExe=Join-Path $runtimeBase 'node/bin/node.exe'}
if(-not $NodeModules){$NodeModules=Join-Path $runtimeBase 'node/node_modules'}
if(-not $PythonExe){$PythonExe=Join-Path $runtimeBase 'python/python.exe'}
if(-not $PythonLauncher){$PythonLauncher=Join-Path $profilePath '.codex/workbenches/codex-local/Invoke-CodexPython.ps1'}
if(-not $PresentationSkill){
 $skillBase=Join-Path $profilePath '.codex/plugins/cache/openai-primary-runtime/presentations'
 $found=Get-ChildItem -LiteralPath $skillBase -Directory | Sort-Object LastWriteTime -Descending | Where-Object {Test-Path -LiteralPath (Join-Path $_.FullName 'skills/presentations/container_tools/artifact_tool_utils.mjs')} | Select-Object -First 1
 if($found){$PresentationSkill=Join-Path $found.FullName 'skills/presentations'}
}
foreach($file in @($NodeExe,$PythonExe,(Join-Path $PresentationSkill 'container_tools/artifact_tool_utils.mjs'))){if(-not (Test-Path -LiteralPath $file -PathType Leaf)){throw "Missing capability, supply the corresponding parameter: $file"}}
if(-not (Test-Path -LiteralPath (Join-Path $NodeModules '@oai/artifact-tool') -PathType Container)){throw 'Missing @oai/artifact-tool, supply -NodeModules for an available compatible runtime.'}
if(-not (Test-Path -LiteralPath $PythonLauncher -PathType Leaf)){$PythonLauncher=''}
$SourceDir=[IO.Path]::GetFullPath($SourceDir);$BuildDir=[IO.Path]::GetFullPath($BuildDir);$OutputDir=[IO.Path]::GetFullPath($OutputDir)
if(Test-Path -LiteralPath (Join-Path $OutputDir 'thu-nghiem-chuyen-can.pptx')){throw 'Use a fresh OutputDir. Delivered snapshots will not be overwritten.'}
New-Item -ItemType Directory -Path $BuildDir,$OutputDir -Force | Out-Null
$moduleLink=Join-Path $PSScriptRoot 'node_modules'
$createdLink=$false
if(Test-Path -LiteralPath $moduleLink){throw 'Existing node_modules entry: inspect it before running. The recipe will not replace or delete a pre-existing entry.'}
$savedModules=$env:RUNTIME_NODE_MODULES
try {
 New-Item -ItemType Junction -Path $moduleLink -Target $NodeModules | Out-Null
 $createdLink=$true
 $env:RUNTIME_NODE_MODULES=$NodeModules
 if($PythonLauncher){& $PythonLauncher -B (Join-Path $PSScriptRoot 'analyze.py') --source-dir $SourceDir --build-dir $BuildDir}
 else {& $PythonExe -X utf8 -B (Join-Path $PSScriptRoot 'analyze.py') --source-dir $SourceDir --build-dir $BuildDir}
 if($LASTEXITCODE -ne 0){throw 'Source analysis failed'}
 & $NodeExe (Join-Path $PSScriptRoot 'build.mjs') --build-dir $BuildDir --output-dir $OutputDir --presentation-skill $PresentationSkill --python-exe $PythonExe
 if($LASTEXITCODE -ne 0){throw 'Artifact build failed'}
 & (Join-Path $PSScriptRoot 'office-check.ps1') -OutputDir $OutputDir -BuildDir $BuildDir
 if($PythonLauncher){& $PythonLauncher -B (Join-Path $PSScriptRoot 'verify.py') --source-dir $SourceDir --build-dir $BuildDir --output-dir $OutputDir}
 else {& $PythonExe -X utf8 -B (Join-Path $PSScriptRoot 'verify.py') --source-dir $SourceDir --build-dir $BuildDir --output-dir $OutputDir}
 if($LASTEXITCODE -ne 0){throw 'Final verification failed'}
 Write-Output "Fresh deliverables: $OutputDir"
} finally {
 $env:RUNTIME_NODE_MODULES=$savedModules
 if($createdLink){
  $link=Get-Item -LiteralPath $moduleLink
  if($link.LinkType -ne 'Junction' -or [IO.Path]::GetFullPath($link.Target) -ne [IO.Path]::GetFullPath($NodeModules)){throw 'Unexpected dependency link target. Inspect manually.'}
  Remove-Item -LiteralPath $moduleLink -ErrorAction Stop
 }
}
