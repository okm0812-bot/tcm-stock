$baseDir = $env:USERPROFILE + "\.qclaw\workspace\skills\stock-analysis"
uv run "$baseDir\scripts\analyze_stock.py" 2352.TW 2>&1
