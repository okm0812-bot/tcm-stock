$ErrorActionPreference = "Continue"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$uvUrl = "https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-pc-windows-msvc.zip"
$zipPath = "$env:TEMP\uv.zip"
$extractPath = "$env:TEMP\uv-extracted"
$destPath = "$env:USERPROFILE\.qclaw\uv.exe"

try {
    Invoke-WebRequest -Uri $uvUrl -OutFile $zipPath -TimeoutSec 30 -UseBasicParsing
    Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force
    Copy-Item "$extractPath\uv.exe" -Destination $destPath -Force
    Write-Output "SUCCESS: uv installed to $destPath"
} catch {
    Write-Output "FAILED: $_"
}
