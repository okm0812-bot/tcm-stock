# Try to find pip
$pipCmd = Get-Command pip -ErrorAction SilentlyContinue
$pip3Cmd = Get-Command pip3 -ErrorAction SilentlyContinue
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
$python3Cmd = Get-Command python3 -ErrorAction SilentlyContinue
Write-Output "pip: $($pipCmd.Source)"
Write-Output "pip3: $($pip3Cmd.Source)"
Write-Output "python: $($pythonCmd.Source)"
Write-Output "python3: $($python3Cmd.Source)"

# Try python -m pip
$pyExe = 'C:\Users\user\AppData\Local\Microsoft\WindowsApps\python.exe'
if (Test-Path $pyExe) {
    Write-Output "Found WindowsApps python"
    try {
        & $pyExe -m pip --version 2>&1
    } catch {
        Write-Output "pip module error: $_"
    }
}

# Search for any pip in common locations
$pipPaths = @(
    'C:\Python312\Scripts\pip.exe',
    'C:\Python311\Scripts\pip.exe',
    'C:\Python310\Scripts\pip.exe',
    'C:\Program Files\Python312\Scripts\pip.exe',
    'C:\Program Files\Python311\Scripts\pip.exe',
    'C:\Users\user\AppData\Local\Programs\Python\Python312\Scripts\pip.exe'
)
foreach ($p in $pipPaths) {
    if (Test-Path $p) {
        Write-Output "Found pip at: $p"
        & $p --version 2>&1
    }
}
