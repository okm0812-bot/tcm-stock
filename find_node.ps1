$node = (Get-Command node -ErrorAction SilentlyContinue).Source
$npm = (Get-Command npm -ErrorAction SilentlyContinue).Source
$python = (Get-Command python -ErrorAction SilentlyContinue).Source
$pip = (Get-Command pip -ErrorAction SilentlyContinue).Source
Write-Output "node: $node"
Write-Output "npm: $npm"
Write-Output "python: $python"
Write-Output "pip: $pip"

if ($node) {
    & $node --version
}
if ($npm) {
    & $npm --version
}
