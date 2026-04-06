# -*- coding: utf-8 -*-
import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

# Read MEMORY.md
with open('C:/Users/user/.qclaw/workspace/MEMORY.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Check for the wrong numbers
patterns_to_fix = [
    (r'00795B.*?387,?786.*?\n', '00795B 中信美國公債20年 已被修正\n'),
    (r'中信美國公債20年.*?387,?786', '中信美國公債20年 已修正'),  
    (r'中信美國公債20年.*?虧損.*?-193', ''),  # Remove old wrong entry
]

# Simply search and print what we found
print("Searching for 00795B in MEMORY.md...")
if '00795B' in content:
    print("Found 00795B in MEMORY.md")
    # Find the line
    for line in content.split('\n'):
        if '00795B' in line or '中信' in line:
            print(f"Line: {line[:200]}")
else:
    print("00795B not found in MEMORY.md")

print("\nSearching for wrong values...")

# Check for old wrong values from portfolio B
wrong_values = ['1,587,460', '1,587460', '1,778,444', '1,963,550', '2,183,268']
for v in wrong_values:
    if v in content:
        print(f"Found wrong value: {v}")
        # Count occurrences
        count = content.count(v)
        print(f"  Appears {count} time(s)")
