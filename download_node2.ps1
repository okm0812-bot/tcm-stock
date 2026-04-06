try {
    Start-BitsTransfer -Source "https://nodejs.org/dist/v22.21.1/win-x64/node.exe" -Destination "C:\Users\user\.qclaw\workspace\node.exe" -ErrorAction Stop
    Write-Output "SUCCESS"
    Write-Output "Size: $((Get-Item 'C:\Users\user\.qclaw\workspace\node.exe').Length)"
} catch {
    Write-Output "FAILED: $_"
}
