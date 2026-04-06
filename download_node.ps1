Add-Type -AssemblyName System.Net.Http
$uri = "https://nodejs.org/dist/v22.21.1/win-x64/node.exe"
$outPath = "C:\Users\user\.qclaw\workspace\node.exe"
try {
    $webClient = New-Object System.Net.WebClient
    $webClient.DownloadFile($uri, $outPath)
    $webClient.Dispose()
    Write-Output "SUCCESS"
    Write-Output "File size: $((Get-Item $outPath).Length)"
} catch {
    Write-Output "FAILED: $_"
}
