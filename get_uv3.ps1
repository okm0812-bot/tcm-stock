$ErrorActionPreference = "Continue"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# Try direct download using System.Net.Http
$handler = New-Object System.Net.Http.HttpClientHandler
$client = New-Object System.Net.Http.HttpClient($handler)
$client.Timeout = New-Object System.TimeSpan(0, 0, 30)

$uvUrl = "https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-pc-windows-msvc.zip"
$dest = "C:\Users\user\.qclaw\workspace\uv.zip"

try {
    $content = $client.GetByteArrayAsync($uvUrl).Result
    [System.IO.File]::WriteAllBytes($dest, $content)
    Write-Output "Downloaded: $($content.Length) bytes"
    Expand-Archive -Path $dest -DestinationPath "C:\Users\user\.qclaw\workspace\uv-extracted" -Force
    Write-Output "Extracted successfully"
} catch {
    Write-Output "FAILED: $_"
}
