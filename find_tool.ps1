$whisper = Get-Command whisper -ErrorAction SilentlyContinue
$pip = Get-Command pip -ErrorAction SilentlyContinue
$python = Get-Command python -ErrorAction SilentlyContinue
$node = Get-Command node -ErrorAction SilentlyContinue
Write-Output "whisper: $($whisper.Source)"
Write-Output "pip: $($pip.Source)"
Write-Output "python: $($python.Source)"
Write-Output "node: $($node.Source)"

if ($python) {
    & $python --version 2>&1
}
