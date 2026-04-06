$meta = Get-Content "$env:USERPROFILE\.qclaw\qclaw.json" -Raw | ConvertFrom-Json
$mjs = $meta.cli.openclawMjs
$env:ELECTRON_RUN_AS_NODE = "1"
node $mjs skills install macro-monitor 2>&1
