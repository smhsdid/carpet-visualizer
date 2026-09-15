[CmdletBinding()]
param(
    [string]$RuntimeRoot = "D:\AI\carpet-visualizer-runtime",
    [string]$PythonVersion = "3.13",
    [switch]$SkipModel
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$lock = Get-Content -Raw (Join-Path $projectRoot "config\runtime-lock.json") | ConvertFrom-Json
$comfyRoot = Join-Path $RuntimeRoot "ComfyUI"
$venvRoot = Join-Path $RuntimeRoot "venv"
$cacheRoot = Join-Path $RuntimeRoot "cache"
$tempRoot = Join-Path $RuntimeRoot "tmp"

New-Item -ItemType Directory -Force -Path $RuntimeRoot, $cacheRoot, (Join-Path $cacheRoot "pip"), (Join-Path $cacheRoot "huggingface"), $tempRoot | Out-Null
$env:TEMP = $tempRoot
$env:TMP = $tempRoot
$env:PIP_CACHE_DIR = Join-Path $cacheRoot "pip"
$env:HF_HOME = Join-Path $cacheRoot "huggingface"
$env:HF_HUB_CACHE = Join-Path $env:HF_HOME "hub"

if (-not (Test-Path -LiteralPath $comfyRoot)) {
    git clone $lock.comfyui.repository $comfyRoot
}
git -C $comfyRoot fetch origin $lock.comfyui.commit --depth 1
git -C $comfyRoot checkout --detach $lock.comfyui.commit

foreach ($node in $lock.custom_nodes) {
    $nodeRoot = Join-Path (Join-Path $comfyRoot "custom_nodes") $node.directory
    if (-not (Test-Path -LiteralPath $nodeRoot)) {
        git clone $node.repository $nodeRoot
    }
    git -C $nodeRoot fetch origin $node.commit --depth 1
    git -C $nodeRoot checkout --detach $node.commit
}

if (-not (Test-Path -LiteralPath (Join-Path $venvRoot "Scripts\python.exe"))) {
    py "-$PythonVersion" -m venv $venvRoot
}
$python = Join-Path $venvRoot "Scripts\python.exe"
& $python -m pip install --upgrade pip
& $python -m pip install $lock.pytorch.packages --extra-index-url $lock.pytorch.index_url
& $python -m pip install -r (Join-Path $comfyRoot "requirements.txt")

if (-not $SkipModel) {
    foreach ($model in $lock.models) {
        $modelPath = Join-Path $comfyRoot $model.relative_path
        $modelDir = Split-Path -Parent $modelPath
        $partialPath = "$modelPath.partial"
        New-Item -ItemType Directory -Force -Path $modelDir | Out-Null
        if (Test-Path -LiteralPath $modelPath) {
            $existingSize = (Get-Item -LiteralPath $modelPath).Length
            if ($existingSize -lt $model.size_bytes) {
                Move-Item -LiteralPath $modelPath -Destination $partialPath -Force
            } elseif ($existingSize -ne $model.size_bytes) {
                throw "Unexpected model size for $($model.id): $existingSize bytes"
            }
        }
        if (Test-Path -LiteralPath $modelPath) {
            $existingHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $modelPath).Hash.ToLowerInvariant()
            if ($existingHash -ne $model.sha256.ToLowerInvariant()) { throw "Existing model SHA256 mismatch for $($model.id): $existingHash" }
        }
        else {
            curl.exe -L --fail --continue-at - --output $partialPath $model.url
            if ($LASTEXITCODE -ne 0) { throw "Model download failed for $($model.id) with exit code $LASTEXITCODE" }
            $downloadedHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $partialPath).Hash.ToLowerInvariant()
            if ($downloadedHash -ne $model.sha256.ToLowerInvariant()) { throw "Downloaded model SHA256 mismatch for $($model.id): $downloadedHash" }
            Move-Item -LiteralPath $partialPath -Destination $modelPath
        }
    }
}

& $python (Join-Path $projectRoot "scripts\doctor.py") --runtime-root $RuntimeRoot
