[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$InputImage,
    [string]$RuntimeRoot = "D:\AI\carpet-visualizer-runtime",
    [string]$OutputDir = "output",
    [double]$Scale = 2.0,
    [int]$Port = 8188,
    [switch]$KeepServer
)

$ErrorActionPreference = "Stop"
$comfyRoot = Join-Path $RuntimeRoot "ComfyUI"
$python = Join-Path $RuntimeRoot "venv\Scripts\python.exe"
$tempRoot = Join-Path $RuntimeRoot "tmp"
$logRoot = Join-Path $RuntimeRoot "logs"
New-Item -ItemType Directory -Force -Path $tempRoot, $logRoot | Out-Null
$env:TEMP = $tempRoot
$env:TMP = $tempRoot
$env:PIP_CACHE_DIR = Join-Path $RuntimeRoot "cache\pip"
$env:HF_HOME = Join-Path $RuntimeRoot "cache\huggingface"
$serverUrl = "http://127.0.0.1:$Port"
$startedHere = $false
$process = $null

try {
    try { Invoke-RestMethod -Uri "$serverUrl/system_stats" -TimeoutSec 2 | Out-Null }
    catch {
        $stdout = Join-Path $logRoot "comfyui-enhance.stdout.log"
        $stderr = Join-Path $logRoot "comfyui-enhance.stderr.log"
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

    & $python (Join-Path $PSScriptRoot "comfyui_upscale.py") $InputImage `
        --runtime-root $RuntimeRoot --output-dir $OutputDir --server $serverUrl --scale $Scale
    if ($LASTEXITCODE -ne 0) { throw "Enhancement client failed with exit code $LASTEXITCODE" }
}
finally {
    if ($startedHere -and -not $KeepServer -and $null -ne $process -and -not $process.HasExited) {
        Stop-Process -Id $process.Id
    }
}
