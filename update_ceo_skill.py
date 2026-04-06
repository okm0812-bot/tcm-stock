# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Read the file
with open('C:/Users/user/.qclaw/workspace/skills/ceo-unified-analysis/SKILL.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the version record section
old_section = """## 版本記錄

| 版本 | 日期 | 備註 |
|------|------|------|
| 1.0.0 | 2026/03/26 | 初始版本，整合12個金融技能 |
| 2.0.0 | 2026/03/27 | 升級版本，新增4個補強技能（對標、現金流、DCF，技術風險） |
| 3.0.0 | 2026/03/27 | 完整版本，新增11個深度優化技能（法人、進階技術、財務、總經、產業、回測、警示） |"""

new_section = """## 版本記錄

| 版本 | 日期 | 備註 |
|------|------|------|
| 1.0.0 | 2026/03/26 | 初始版本，整合12個金融技能 |
| 2.0.0 | 2026/03/27 | 升級版本，新增4個補強技能（對標、現金流、DCF，技術風險） |
| 3.0.0 | 2026/03/27 | 完整版本，新增11個深度優化技能（法人、進階技術、財務、總經、產業、回測、警示） |
| 3.1.0 | 2026/04/01 | 協調版本，整合27個技能為7大模組，建立自動路由和衝突解決機制 |"""

if old_section in content:
    content = content.replace(old_section, new_section)
    print("版本記錄已更新")
else:
    print("找不到版本記錄段落，嘗試其他方式...")
    # Try to find and append
    if "## 版本記錄" in content:
        idx = content.find("## 版本記錄")
        # Find the end of the table
        lines = content[idx:].split('\n')
        for i, line in enumerate(lines):
            if line.startswith("---") and i > 0:
                # Found the end of the table
                end_idx = idx + sum(len(l)+1 for l in lines[:i+1])
                before = content[:end_idx]
                after = content[end_idx:]
                content = before + new_section.split('\n')[-1] + '\n' + after
                print("版本記錄已更新（方式2）")
                break

# Write back
with open('C:/Users/user/.qclaw/workspace/skills/ceo-unified-analysis/SKILL.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("更新完成！")
