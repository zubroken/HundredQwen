param()

$Port = 9010
$HostAddress = "127.0.0.1"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BaseUrl = "http://${HostAddress}:$Port"
$HealthUrl = "$BaseUrl/api/config/llm/status"

function Test-HundredQwenHealth {
    try {
        $response = Invoke-WebRequest -Uri $HealthUrl -UseBasicParsing -TimeoutSec 2
        return $response.StatusCode -eq 200
    }
    catch {
        return $false
    }
}

if (Test-HundredQwenHealth) {
    Write-Host "HundredQwen is already running: $BaseUrl"
    Start-Process $BaseUrl
    exit 0
}

$listener = Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue |
    Select-Object -First 1
if ($listener) {
    Write-Error "Port $Port is in use by PID $($listener.OwningProcess), not HundredQwen. Stop that process and try again."
    exit 1
}

$pythonCommand = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCommand) {
    Write-Error "Python was not found. Activate the project Python environment and try again."
    exit 1
}

Write-Host "Starting HundredQwen: $BaseUrl"
$process = Start-Process -FilePath $pythonCommand.Source `
    -ArgumentList "main.py --host $HostAddress --port $Port" `
    -WorkingDirectory $ProjectRoot `
    -WindowStyle Hidden `
    -PassThru

for ($attempt = 1; $attempt -le 15; $attempt++) {
    Start-Sleep -Seconds 1
    if (Test-HundredQwenHealth) {
        Write-Host "HundredQwen started: $BaseUrl"
        Start-Process $BaseUrl
        exit 0
    }
}

if (-not $process.HasExited) {
    Stop-Process -Id $process.Id -Force
}
Write-Error "HundredQwen did not start within 15 seconds. Run python main.py --host $HostAddress --port $Port from the project directory to inspect the error."
exit 1
