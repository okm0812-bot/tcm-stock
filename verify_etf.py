# -*- coding: utf-8 -*-
# ETF 市值驗證

etfs = [
    {"name": "00687B 國泰20年美債", "shares": 11000, "cost": 31.22, "price": 28.57},
    {"name": "00795B 中信美國公債20年", "shares": 14000, "cost": 29.89, "price": 27.71},
    {"name": "永豐20年美公債", "shares": 5000, "cost": 25.08, "price": 24.03},
    {"name": "統一美債20年", "shares": 5000, "cost": 14.96, "price": 13.89},
    {"name": "00933B 國泰10Y+金融債", "shares": 2000, "cost": 16.67, "price": 15.96},
]

print("=" * 60)
print("ETF 市值驗證")
print("=" * 60)

total_value = 0
total_cost = 0

for e in etfs:
    value = e["shares"] * e["price"]
    cost = e["shares"] * e["cost"]
    loss = cost - value
    total_value += value
    total_cost += cost
    
    print(f"{e['name']}")
    print(f"  {e['shares']:,} 股 × {e['price']:.2f} = {value:,.0f} 元")
    print(f"  成本: {e['shares']:,} × {e['cost']:.2f} = {cost:,.0f}")
    print(f"  虧損: {loss:,.0f} ({(loss/cost*100):.1f}%)")
    print()

print("-" * 60)
print(f"總市值: {total_value:,.0f} 元")
print(f"總成本: {total_cost:,.0f} 元")
print(f"總虧損: {total_cost - total_value:,.0f} 元 ({((total_cost-total_value)/total_cost*100):.1f}%)")
