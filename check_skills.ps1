$result = & 'C:\Program Files\QClaw\resources\openclaw\config\skills\qclaw-openclaw\scripts\openclaw-win.cmd' skills list 2>&1
$result | Select-String -Pattern "openai-whisper" -Context 0,2
