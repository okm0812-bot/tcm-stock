# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

content = """

---

## A 帳戶代碼修正（2026-04-01 21:59）

### 修正內容
- A帳戶「永豐20年美公債」代碼應為 **00857B**（不是 00751B）
- 00751B 在 A帳戶不存在，A帳戶該欄位是 00857B

### A 帳戶正確代碼對照

| 代碼 | 名稱 | 帳戶 |
|------|------|------|
| 00687B | 國泰20年美債 | A帳戶 + B帳戶 |
| 00795B | 中信美國公債20年 | A帳戶 + B帳戶 |
| **00857B** | **永豐20年美公債** | **A帳戶** |
| 00853B | 統一美債20年（A）/ 統一美債10年Aa-A（B） | A帳戶 + B帳戶 |
| 00933B | 群益ESG投等債20+（A）/ 國泰10Y+金融債（B） | A帳戶 + B帳戶 |
| 00751B | 元大AAA至A公司債 | **B帳戶only** |

### 00857B 今日現價
- 今日收盤：23.71 元
- 昨收：23.81 元（用戶提供數據）
- 均價：25.08 元
- 損益：-5.15%（以23.81計算）
"""

with open('C:/Users/user/.qclaw/workspace/memory/2026-04-01.md', 'r', encoding='utf-8') as f:
    existing = f.read()

# 也修正腳本中的代碼
with open('C:/Users/user/.qclaw/workspace/memory/2026-04-01.md', 'w', encoding='utf-8') as f:
    f.write(existing + content)

print("記憶已更新：A帳戶 00751B → 00857B")
