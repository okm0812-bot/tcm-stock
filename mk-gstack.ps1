$parent = $env:USERPROFILE + "\.qclaw\workspace\skills"
$newDir = $parent + "\gstack-skills"
[System.IO.Directory]::CreateDirectory($newDir)
Write-Host "Created: $newDir"
