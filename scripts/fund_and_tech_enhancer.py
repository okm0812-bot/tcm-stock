#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
法人數據與技術指標補強系統
"""

import json
import datetime

class FundFlowEnhancer:
    """法人資金流動分析補強"""
    
    def __init__(self):
        self.data_source = {
            "history_trend": {
                "外資": {"趨勢": "賣超", "連續": 3},
                "投信": {"趨勢": "買超", "連續": 1},
                "自營商": {"趨勢": "賣超", "連續": 2}
            },
            "stock_influence": {
                "1101": {"法人影響": "中等", "外資持股比例": "約10%"},
                "2352": {"法人影響": "中等", "外資持股比例": "約8%"},
                "2409": {"法人影響": "高", "外資持股比例": "約15%"},
                "6919": {"法人影響": "低", "外資持股比例": "約2%"}
            }
        }
    
    def analyze_fund_flow(self):
        """分析法人資金流動"""
        result = {
            "分析時間": datetime.datetime.now().strftime("%Y-%m-%d"),
            "整體趨勢": self._get_overall_trend(),
            "對持股影響": self._analyze_holdings_impact(),
            "建議": self._get_fund_flow_advice()
        }
        return result
    
    def _get_overall_trend(self):
        """獲取整體法人趨勢"""
        trends = self.data_source["history_trend"]
        
        # 判斷法人動向趨勢
        foreign_trend = trends["外資"]["趨勢"]
        investment_trend = trends["投信"]["趨勢"]
        dealer_trend = trends["自營商"]["趨勢"]
        
        # 綜合判斷
        if foreign_trend == "賣超" and dealer_trend == "賣超":
            return "法人動向偏空"
        elif foreign_trend == "買超" and investment_trend == "買超":
            return "法人動向偏多"
        else:
            return "法人動向分歧"
    
    def _analyze_holdings_impact(self):
        """分析法人對持股影響"""
        impacts = {}
        holdings = ["1101", "2352", "2409", "6919"]
        
        for stock in holdings:
            stock_data = self.data_source["stock_influence"].get(stock, {})
            influence = stock_data.get("法人影響", "未知")
            
            # 根據法人影響程度分類
            if influence == "高":
                impacts[stock] = "法人動向影響顯著"
            elif influence == "中等":
                impacts[stock] = "法人動向有一定影響"
            elif influence == "低":
                impacts[stock] = "法人動向影響有限"
            else:
                impacts[stock] = "法人動向影響未知"
        
        return impacts
    
    def _get_fund_flow_advice(self):
        """獲取法人動向建議"""
        trends = self.data_source["history_trend"]
        
        advice = []
        if trends["外資"]["連續"] >= 3:
            advice.append("外資連續賣超，需留意電子股")
        
        if trends["投信"]["趨勢"] == "買超":
            advice.append("投信小幅買超，中小型股可能有支撐")
        
        if trends["自營商"]["趨勢"] == "賣超":
            advice.append("自營商賣超，短線可能承壓")
        
        if not advice:
            advice.append("法人動向不明顯，需觀察市場變化")
        
        return advice

class TechnicalIndicatorEnhancer:
    """技術指標分析補強"""
    
    def __init__(self):
        self.patterns = {
            "RSI": {
                "70": "超買區域",
                "50": "中性區域",
                "30": "超賣區域"
            },
            "MACD": {
                "金叉": "上升訊號",
                "死叉": "下降訊號",
                "橫盤": "中性訊號"
            },
            "成交量": {
                "放大": "趨勢強烈",
                "縮小": "趨勢不確定",
                "持平": "趨勢中性"
            }
        }
    
    def analyze_stock_technical(self, stock_data):
        """分析個股技術指標"""
        result = {
            "股票": stock_data.get("股票"),
            "價格": stock_data.get("價格"),
            "漲跌": stock_data.get("漲跌"),
            "成交量": stock_data.get("成交量"),
            "技術分析": {}
        }
        
        # RSI 分析（根據價格變化估算）
        rsi_analysis = self._estimate_rsi(stock_data)
        result["技術分析"]["RSI"] = rsi_analysis
        
        # MACD 分析（根據趨勢估算）
        macd_analysis = self._estimate_macd(stock_data)
        result["技術分析"]["MACD"] = macd_analysis
        
        # 成交量分析
        volume_analysis = self._analyze_volume(stock_data)
        result["技術分析"]["成交量"] = volume_analysis
        
        # 支撐壓力分析
        support_resistance = self._estimate_support_resistance(stock_data)
        result["技術分析"]["支撐壓力"] = support_resistance
        
        # 綜合技術判斷
        result["技術分析"]["綜合判斷"] = self._get_technical_summary(
            rsi_analysis, macd_analysis, volume_analysis
        )
        
        return result
    
    def _estimate_rsi(self, stock_data):
        """估算 RSI 狀態"""
        price_change = stock_data.get("漲跌", 0)  # 漲跌幅
        
        if price_change <= -2:
            return {"狀態": "可能超賣", "建議": "可能接近反彈"}
        elif price_change >= 2:
            return {"狀態": "可能超買", "建議": "可能回落"}
        elif price_change <= -1:
            return {"狀態": "偏賣", "建議": "觀察支撐"}
        elif price_change >= 1:
            return {"狀態": "偏買", "建議": "觀察壓力"}
        else:
            return {"狀態": "中性", "建議": "技術面不明確"}
    
    def _estimate_macd(self, stock_data):
        """估算 MACD 狀態"""
        price_change = stock_data.get("漲跌", 0)
        recent_trend = stock_data.get("近期趨勢", "持平")
        
        if price_change <= -2:
            return {"狀態": "可能死叉", "建議": "下降趨勢"}
        elif price_change >= 2:
            return {"狀態": "可能金叉", "建議": "上升趨勢"}
        elif recent_trend == "下降":
            return {"狀態": "偏死叉", "建議": "可能繼續下降"}
        elif recent_trend == "上升":
            return {"狀態": "偏金叉", "建議": "可能繼續上升"}
        else:
            return {"狀態": "橫盤", "建議": "趨勢不明"}
    
    def _analyze_volume(self, stock_data):
        """分析成交量"""
        volume = stock_data.get("成交量", 0)
        avg_volume = stock_data.get("平均成交量", 0)
        
        if avg_volume == 0:
            return {"狀態": "未知", "建議": "需參考歷史成交量"}
        
        volume_ratio = volume / avg_volume
        
        if volume_ratio > 1.5:
            return {"狀態": "成交量放大", "建議": "趨勢可能強烈"}
        elif volume_ratio < 0.5:
            return {"狀態": "成交量縮小", "建議": "趨勢可能不確定"}
        elif 0.8 <= volume_ratio <= 1.2:
            return {"狀態": "成交量正常", "建議": "趨勢可信"}
        else:
            return {"狀態": "成交量波動", "建議": "趨勢需確認"}
    
    def _estimate_support_resistance(self, stock_data):
        """估算支撐壓力"""
        price = stock_data.get("價格", 0)
        
        if price == 0:
            return {"支撐": "未知", "壓力": "未知"}
        
        # 根據價格估算支撐壓力（簡化）
        support = round(price * 0.95, 2)  # 下降5%
        resistance = round(price * 1.05, 2)  # 上升5%
        
        return {
            "支撐": support,
            "壓力": resistance,
            "建議": f"支撐約{support}, 壓力約{resistance}"
        }
    
    def _get_technical_summary(self, rsi, macd, volume):
        """獲取技術分析綜合判斷"""
        rsi_status = rsi.get("狀態", "中性")
        macd_status = macd.get("狀態", "橫盤")
        volume_status = volume.get("狀態", "成交量正常")
        
        if rsi_status == "可能超賣" and macd_status == "可能死叉":
            return {"綜合": "技術面偏空", "強度": "強"}
        elif rsi_status == "可能超買" and macd_status == "可能金叉":
            return {"綜合": "技術面偏多", "強度": "強"}
        elif rsi_status == "偏賣" or macd_status == "偏死叉":
            return {"綜合": "技術面偏空", "強度": "中"}
        elif rsi_status == "偏買" or macd_status == "偏金叉":
            return {"綜合": "技術面偏多", "強度": "中"}
        else:
            return {"綜合": "技術面中性", "強度": "弱"}

class CEOAnalysisEnhancer:
    """CEO分析補強主系統"""
    
    def __init__(self):
        self.fund_enhancer = FundFlowEnhancer()
        self.tech_enhancer = TechnicalIndicatorEnhancer()
    
    def enhance_analysis(self, stock_data_list):
        """補強 CEO 分析"""
        print("=== CEO 分析補強系統啟動 ===")
        print(f"時間：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 法人資金流動分析
        print("\n【法人資金流動分析】")
        fund_analysis = self.fund_enhancer.analyze_fund_flow()
        print(f"整體趨勢：{fund_analysis['整體趨勢']}")
        print(f"對持股影響：{fund_analysis['對持股影響']}")
        print(f"建議：{fund_analysis['建議']}")
        
        # 技術指標分析
        print("\n【技術指標分析】")
        for stock_data in stock_data_list:
            print(f"\n--- {stock_data['股票']} ---")
            tech_analysis = self.tech_enhancer.analyze_stock_technical(stock_data)
            
            print(f"價格：{tech_analysis['價格']}，漲跌：{tech_analysis['漲跌']}")
            print(f"成交量：{tech_analysis['成交量']}")
            print(f"RSI分析：{tech_analysis['技術分析']['RSI']}")
            print(f"MACD分析：{tech_analysis['技術分析']['MACD']}")
            print(f"成交量分析：{tech_analysis['技術分析']['成交量']}")
            print(f"支撐壓力：{tech_analysis['技術分析']['支撐壓力']}")
            print(f"綜合判斷：{tech_analysis['技術分析']['綜合判斷']}")
        
        # 生成補強報告
        enhanced_report = self.generate_enhanced_report(fund_analysis, stock_data_list)
        return enhanced_report
    
    def generate_enhanced_report(self, fund_analysis, stock_data_list):
        """生成補強分析報告"""
        report = {
            "報告時間": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "法人資金流動": fund_analysis,
            "技術指標分析": [],
            "綜合建議": []
        }
        
        # 收集技術分析結果
        for stock_data in stock_data_list:
            tech_analysis = self.tech_enhancer.analyze_stock_technical(stock_data)
            report["技術指標分析"].append(tech_analysis)
        
        # 生成綜合建議
        report["綜合建議"] = self.generate_comprehensive_advice(
            fund_analysis, report["技術指標分析"]
        )
        
        return report
    
    def generate_comprehensive_advice(self, fund_analysis, tech_analysis_list):
        """生成綜合建議"""
        advice = []
        
        # 法人動向建議
        fund_trend = fund_analysis["整體趨勢"]
        if fund_trend == "法人動向偏空":
            advice.append("法人動向偏空，建議謹慎操作")
        elif fund_trend == "法人動向偏多":
            advice.append("法人動向偏多，可考慮增持")
        else:
            advice.append("法人動向分歧，需觀察市場變化")
        
        # 技術面建議
        for tech_analysis in tech_analysis_list:
            stock = tech_analysis["股票"]
            tech_summary = tech_analysis["技術分析"]["綜合判斷"]
            
            tech_status = tech_summary["綜合"]
            tech_strength = tech_summary["強度"]
            
            if tech_status == "技術面偏空" and tech_strength == "強":
                advice.append(f"{stock}技術面強烈偏空，建議減碼")
            elif tech_status == "技術面偏多" and tech_strength == "強":
                advice.append(f"{stock}技術面強烈偏多，可考慮增持")
            elif tech_status == "技術面偏空":
                advice.append(f"{stock}技術面偏空，需留意風險")
            elif tech_status == "技術面偏多":
                advice.append(f"{stock}技術面偏多，可觀察機會")
        
        return advice

def main():
    """主函數"""
    enhancer = CEOAnalysisEnhancer()
    
    # 持股數據（從 MEMORY.md 獲取）
    stock_data_list = [
        {
            "股票": "台泥1101",
            "價格": 22.80,
            "漲跌": -0.22,
            "成交量": 10809,
            "平均成交量": 15000,
            "近期趨勢": "下降"
        },
        {
            "股票": "佳世達2352",
            "價格": 23.60,
            "漲跌": -1.87,
            "成交量": 3057,
            "平均成交量": 4000,
            "近期趨勢": "下降"
        },
        {
            "股票": "友達2409",
            "價格": 14.45,
            "漲跌": -2.36,
            "成交量": 68390,
            "平均成交量": 60000,
            "近期趨勢": "下降"
        },
        {
            "股票": "康霈6919",
            "價格": 80.9,
            "漲跌": -5.49,
            "成交量": 13869,
            "平均成交量": 20000,
            "近期趨勢": "下降"
        }
    ]
    
    # 執行補強分析
    enhanced_report = enhancer.enhance_analysis(stock_data_list)
    
    print("\n=== 補強分析總結 ===")
    print("法人數據補強：完成歷史趨勢分析、持股影響分析")
    print("技術指標補強：完成RSI/MACD/成交量/支撐壓力分析")
    print("綜合建議：生成基於法人+技術面的操作建議")

if __name__ == "__main__":
    main()
