[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$SemanticMaster,
    [string]$RuntimeRoot = "D:\AI\carpet-visualizer-runtime",
    [string]$OutputDir = "output",
    [double]$Scale = 2.0
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $RuntimeRoot "venv\Scripts\python.exe"
$tempRoot = Join-Path $RuntimeRoot "tmp\carpet-visualizer"
New-Item -ItemType Directory -Force -Path $tempRoot | Out-Null
$texturedMaster = Join-Path $tempRoot (([System.IO.Path]::GetFileNameWithoutExtension($SemanticMaster)) + "-textured.png")

& $python (Join-Path $PSScriptRoot "apply_weave_texture.py") $SemanticMaster $texturedMaster `
    --product-texture (Join-Path $projectRoot "assets\material-library\jacquard-01\construction\product-scale-crop.jpg") `
    --macro-texture (Join-Path $projectRoot "assets\material-library\jacquard-01\construction\macro-detail.jpg") `
    --product-tile 120 --macro-tile 75 --product-strength 0.11 --macro-strength 0.035
if ($LASTEXITCODE -ne 0) { throw "Weave texture stage failed with exit code $LASTEXITCODE" }

& (Join-Path $PSScriptRoot "run-local-enhance.ps1") $texturedMaster `
    -RuntimeRoot $RuntimeRoot -OutputDir $OutputDir -Scale $Scale
if ($LASTEXITCODE -ne 0) { throw "GPU enhancement stage failed with exit code $LASTEXITCODE" }
