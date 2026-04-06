# OpenClaw Auto-Updater Script
# Run via Windows Task Scheduler daily at 4:00 AM
# Logs output to update-log.txt

$ErrorActionPreference = "Continue"
$logPath = "$env:USERPROFILE\.qclaw\workspace\logs\update-log.txt"
$date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Ensure log directory exists
$logDir = Split-Path $logPath
if (!(Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

# Header
"$date --- OpenClaw Auto-Update Start ---" | Tee-Object -FilePath $logPath -Append

# 1. Update OpenClaw itself (via npm if available)
$npmUpdate = npx clawhub@latest update --all 2>&1
$npmUpdate | Tee-Object -FilePath $logPath -Append

# 2. Show result
if ($LASTEXITCODE -eq 0) {
    "$date --- Update completed successfully ---" | Tee-Object -FilePath $logPath -Append
} else {
    "$date --- Update completed with warnings ---" | Tee-Object -FilePath $logPath -Append
}

# Keep only last 7 days of log entries (simple trim)
$lines = Get-Content $logPath
if ($lines.Count -gt 1000) {
    $lines | Select-Object -Last 500 | Set-Content $logPath
}
