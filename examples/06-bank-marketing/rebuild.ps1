#requires -Version 7.3
param(
  [Parameter(Mandatory)][string]$PythonLauncher,
  [Parameter(Mandatory)][string]$Node,
  [Parameter(Mandatory)][string]$Modules,
  [Parameter(Mandatory)][string]$Chrome,
  [Parameter(Mandatory)][string]$PopplerBin,
  [Parameter(Mandatory)][string]$Source,
  [Parameter(Mandatory)][string]$Out
)
$ErrorActionPreference = 'Stop'
& $PythonLauncher -B (Join-Path $PSScriptRoot 'build.py') --source $Source --out $Out
if ($LASTEXITCODE -ne 0) { throw 'Calculation or HTML build failed.' }
& $Node (Join-Path $PSScriptRoot 'render.mjs') --modules $Modules --chrome $Chrome --out $Out
if ($LASTEXITCODE -ne 0) { throw 'Browser/PDF render failed.' }
& $PythonLauncher -B (Join-Path $PSScriptRoot 'verify.py') --source $Source --out $Out --poppler-bin $PopplerBin
if ($LASTEXITCODE -ne 0) { throw 'Verification failed.' }
