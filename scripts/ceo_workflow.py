# -*- coding: utf-8 -*-
"""
=================================================================
CEO 自動化工作流程 v1.0
功能：
1. 定時執行風險預警
2. 定時執行系統監控
3. 整合報告歸檔
4. 日誌記錄
=================================================================
"""

import os
import sys
from datetime import datetime

# 工作流程設定
WORKFLOW_STEPS = [
    ("system_check", "System Health Check"),
    ("risk_alert", "Risk Alert Analysis"),
    ("portfolio_check", "Portfolio Status Check"),
    ("report_archive", "Report Archiving"),
]

class CEOWorkflow:
    """CEO 工作流程管理"""
    
    def __init__(self):
        self.log = []
        self.start_time = datetime.now()
    
    def log_step(self, step_name, status, message=""):
        """記錄工作流程步驟"""
        self.log.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "step": step_name,
            "status": status,
            "message": message
        })
    
    def run_system_check(self):
        """執行系統檢查"""
        try:
            # 導入並執行監控
            sys.path.insert(0, "C:\\Users\\user\\.qclaw\\workspace\\scripts")
            from ceo_monitor import SystemMonitor
            
            monitor = SystemMonitor()
            metrics = monitor.generate_dashboard()
            
            self.log_step("System Check", "OK", f"Scripts: {metrics['script_count']}")
            return True
        except Exception as e:
            self.log_step("System Check", "FAIL", str(e))
            return False
    
    def run_risk_alert(self):
        """執行風險預警"""
        try:
            from risk_alert_v2 import run_full_alert_check, output_alerts
            
            # 測試數據
            market_data = {"twii_now": 32000, "twii_prev": 32500, "vix": 25}
            stock_prices = {"1101": 23.70, "2352": 23.30, "2409": 16.85, "6919": 95.0}
            
            alerts = run_full_alert_check(market_data, stock_prices)
            output_alerts(alerts, "workflow_risk_alert.txt")
            
            self.log_step("Risk Alert", "OK", f"Alerts: {len(alerts)}")
            return True
        except Exception as e:
            self.log_step("Risk Alert", "FAIL", str(e))
            return False
    
    def run_portfolio_check(self):
        """執行持股檢查"""
        try:
            # 簡化持股檢查
            portfolio = {
                "1101": {"shares": 19000, "avg": 34.56, "current": 23.70},
                "2352": {"shares": 5000, "avg": 51.33, "current": 23.30},
                "2409": {"shares": 9000, "avg": 16.20, "current": 16.85},
                "6919": {"shares": 300, "avg": 102.36, "current": 95.0},
            }
            
            total_value = sum(p["shares"] * p["current"] for p in portfolio.values())
            total_cost = sum(p["shares"] * p["avg"] for p in portfolio.values())
            pnl = (total_value - total_cost) / total_cost * 100
            
            self.log_step("Portfolio Check", "OK", f"PnL: {pnl:.2f}%")
            return True
        except Exception as e:
            self.log_step("Portfolio Check", "FAIL", str(e))
            return False
    
    def archive_reports(self):
        """歸檔報告"""
        try:
            import shutil
            from glob import glob
            
            # 建立歸檔目錄
            archive_dir = f"C:\\Users\\user\\.qclaw\\workspace\\archive\\{datetime.now().strftime('%Y%m%d')}"
            os.makedirs(archive_dir, exist_ok=True)
            
            # 移動舊報告
            workspace = "C:\\Users\\user\\.qclaw\\workspace"
            txt_files = glob(f"{workspace}\\*.txt")
            
            moved = 0
            for f in txt_files:
                if "workflow" in f or "test" in f:
                    shutil.move(f, archive_dir)
                    moved += 1
            
            self.log_step("Report Archive", "OK", f"Moved: {moved} files")
            return True
        except Exception as e:
            self.log_step("Report Archive", "FAIL", str(e))
            return False
    
    def run_full_workflow(self):
        """執行完整工作流程"""
        self.log_step("Workflow Start", "INFO", f"Time: {self.start_time.strftime('%H:%M:%S')}")
        
        # 執行各步驟
        self.run_system_check()
        self.run_risk_alert()
        self.run_portfolio_check()
        self.archive_reports()
        
        # 結束記錄
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        self.log_step("Workflow End", "INFO", f"Duration: {duration:.1f}s")
        
        return self.log
    
    def generate_workflow_report(self):
        """產生工作流程報告"""
        lines = []
        lines.append("="*60)
        lines.append("CEO Workflow Execution Report")
        lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
        lines.append("="*60)
        
        for entry in self.log:
            status_icon = "[OK]" if entry["status"] == "OK" else "[FAIL]" if entry["status"] == "FAIL" else "[INFO]"
            lines.append(f"{entry['time']} {status_icon} {entry['step']}")
            if entry["message"]:
                lines.append(f"           -> {entry['message']}")
        
        # 統計
        ok_count = sum(1 for e in self.log if e["status"] == "OK")
        fail_count = sum(1 for e in self.log if e["status"] == "FAIL")
        
        lines.append("-"*60)
        lines.append(f"Summary: {ok_count} OK, {fail_count} FAIL")
        
        return "\n".join(lines)

def main():
    """主程式"""
    workflow = CEOWorkflow()
    workflow.run_full_workflow()
    
    report = workflow.generate_workflow_report()
    
    # 儲存報告
    report_file = f"workflow_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"Workflow completed, report saved to {report_file}")

if __name__ == "__main__":
    main()
