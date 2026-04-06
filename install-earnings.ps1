$meta = Get-Content "$env:USERPROFILE\.qclaw\qclaw.json" -Raw | ConvertFrom-Json
$mjs = $meta.cli.openclawMjs
$env:ELECTRON_RUN_AS_NODE = "1"
node $mjs skills install earnings-tracker 2>&1
