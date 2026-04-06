$meta = Get-Content "$env:USERPROFILE\.qclaw\qclaw.json" -Raw | ConvertFrom-Json
$mjs = $meta.cli.openclawMjs
$env:ELECTRON_RUN_AS_NODE = "1"
node $mjs cron list 2>&1
