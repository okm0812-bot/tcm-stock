# Download uv standalone Windows binary
$ErrorActionPreference = "Continue"
$outPath = "$env:USERPROFILE\.qclaw\uv.exe"
$url = "https://astral.sh/uv/install.ps1"

# Try direct uv download for Windows
$uvDirect = "https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-pc-windows-msvc.zip"
$client = New-Object System.Net.WebClient
try {
    $client.DownloadFile($uvDirect, "$env:TEMP\uv.zip")
    Expand-Archive -Path "$env:TEMP\uv.zip" -DestinationPath "$env:TEMP\uv-extracted" -Force
    Copy-Item "$env:TEMP\uv-extracted\uv.exe" -Destination "$env:USERPROFILE\.qclaw\uv.exe" -Force
    Write-Output "SUCCESS"
} catch {
    Write-Output "FAILED: $_"
}
