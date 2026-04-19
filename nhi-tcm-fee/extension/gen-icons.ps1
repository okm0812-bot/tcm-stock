Add-Type -AssemblyName System.Drawing
$dir = "$env:USERPROFILE\.qclaw\workspace-agent-2aae340b\extension"

function New-Icon {
    param([int]$size, [string]$path)
    $bmp = New-Object System.Drawing.Bitmap($size, $size)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = 'AntiAlias'
    $g.Clear([System.Drawing.Color]::FromArgb(33, 150, 243))
    $brush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
    $pad = [int]($size * 0.15)
    $s = $size - $pad * 2
    $g.FillEllipse($brush, $pad, $pad, $s, $s)
    $brush.Dispose()
    $g.Dispose()
    $bmp.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
    $bmp.Dispose()
}

New-Icon -size 16 -path "$dir\icon16.png"
New-Icon -size 48 -path "$dir\icon48.png"
New-Icon -size 128 -path "$dir\icon128.png"
Write-Output "Icons generated successfully"
