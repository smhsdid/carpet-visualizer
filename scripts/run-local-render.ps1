[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$InputImage,
    [string]$RuntimeRoot = "D:\AI\carpet-visualizer-runtime",
    [string]$OutputDir = "output",
    [int]$Port = 8188,
    [int]$Seed = 5060001,
    [int]$Steps = 14,
    [double]$Denoise = 0.28,
    [int]$MaxSide = 1024,
    [switch]$KeepServer
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$comfyRoot = Join-Path $RuntimeRoot "ComfyUI"
$python = Join-Path $RuntimeRoot "venv\Scripts\python.exe"
$tempRoot = Join-Path $RuntimeRoot "tmp"
$logRoot = Join-Path $RuntimeRoot "logs"
New-Item -ItemType Directory -Force -Path $tempRoot, $logRoot | Out-Null
$env:TEMP = $tempRoot
$env:TMP = $tempRoot
$env:PIP_CACHE_DIR = Join-Path $RuntimeRoot "cache\pip"
$env:HF_HOME = Join-Path $RuntimeRoot "cache\huggingface"

if (-not (Test-Path -LiteralPath $python)) { throw "Runtime missing. Run scripts\install-local-backend.ps1 first." }
$serverUrl = "http://127.0.0.1:$Port"
$startedHere = $false
$process = $null

try {
    try { Invoke-RestMethod -Uri "$serverUrl/system_stats" -TimeoutSec 2 | Out-Null }
    catch {
        $stdout = Join-Path $logRoot "comfyui.stdout.log"
        $stderr = Join-Path $logRoot "comfyui.stderr.log"
        $arguments = @(
            (Join-Path $comfyRoot "main.py"), "--listen", "127.0.0.1", "--port", "$Port",
            "--lowvram", "--disable-auto-launch"
        )
        $process = Start-Process -FilePath $python -ArgumentList $arguments -WorkingDirectory $comfyRoot `
            -RedirectStandardOutput $stdout -RedirectStandardError $stderr -WindowStyle Hidden -PassThru
        $startedHere = $true
        $ready = $false
        for ($attempt = 0; $attempt -lt 120; $attempt++) {
            if ($process.HasExited) { throw "ComfyUI exited early. See $stderr" }
            try {
                Invoke-RestMethod -Uri "$serverUrl/system_stats" -TimeoutSec 2 | Out-Null
                $ready = $true
                break
            } catch { Start-Sleep -Seconds 1 }
        }
        if (-not $ready) { throw "ComfyUI did not become ready. See $stderr" }
    }

    & $python (Join-Path $PSScriptRoot "comfyui_client.py") $InputImage `
        --runtime-root $RuntimeRoot --output-dir $OutputDir --server $serverUrl `
        --seed $Seed --steps $Steps --denoise $Denoise --max-side $MaxSide
    if ($LASTEXITCODE -ne 0) { throw "Render client failed with exit code $LASTEXITCODE" }
}
finally {
    if ($startedHere -and -not $KeepServer -and $null -ne $process -and -not $process.HasExited) {
        Stop-Process -Id $process.Id
    }
}
