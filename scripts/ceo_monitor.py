# -*- coding: utf-8 -*-
"""
=================================================================
CEO 系統監控儀表板 v1.0
功能：
1. 監控腳本數量變化
2. 追蹤報告生成頻率
3. 檢查系統健康度
4. 產生監控摘要
=================================================================
"""

import os
import json
from datetime import datetime, timedelta

WORKSPACE = "C:\\Users\\user\\.qclaw\\workspace"
SCRIPTS_DIR = f"{WORKSPACE}\\scripts"

class SystemMonitor:
    """系統監控類別"""
    
    def __init__(self):
        self.check_time = datetime.now()
        self.metrics = {}
    
    def count_scripts(self):
        """統計腳本數量"""
        try:
            py_files = [f for f in os.listdir(SCRIPTS_DIR) if f.endswith('.py')]
            return len(py_files)
        except:
            return 0
    
    def count_reports(self):
        """統計報告檔案"""
        try:
            txt_files = [f for f in os.listdir(WORKSPACE) if f.endswith('.txt')]
            return len(txt_files)
        except:
            return 0
    
    def get_latest_reports(self, hours=24):
        """取得最近生成的報告"""
        try:
            cutoff = datetime.now() - timedelta(hours=hours)
            recent = []
            
            for f in os.listdir(WORKSPACE):
                if f.endswith('.txt'):
                    path = os.path.join(WORKSPACE, f)
                    mtime = datetime.fromtimestamp(os.path.getmtime(path))
                    if mtime > cutoff:
                        recent.append({
                            "name": f,
                            "time": mtime.strftime("%H:%M:%S")
                        })
            
            return sorted(recent, key=lambda x: x["time"], reverse=True)[:5]
        except:
            return []
    
    def check_module_health(self):
        """檢查模組健康度"""
        modules = {
            "risk_alert_v2.py": "風險預警",
            "unified_chips.py": "法人籌碼",
            "stock_filter.py": "選股自動化",
            "ceo_integrate.py": "CEO整合",
            "ceo_test_runner.py": "測試執行器",
        }
        
        health = {}
        for script, name in modules.items():
            path = os.path.join(SCRIPTS_DIR, script)
            health[name] = {
                "exists": os.path.exists(path),
                "size": os.path.getsize(path) if os.path.exists(path) else 0
            }
        
        return health
    
    def generate_dashboard(self):
        """產生監控儀表板"""
        self.metrics = {
            "check_time": self.check_time.strftime("%Y-%m-%d %H:%M:%S"),
            "script_count": self.count_scripts(),
            "report_count": self.count_reports(),
            "recent_reports": self.get_latest_reports(),
            "module_health": self.check_module_health(),
        }
        
        return self.metrics
    
    def format_dashboard(self, metrics):
        """格式化儀表板輸出（ASCII 版）"""
        lines = []
        lines.append("="*60)
        lines.append("CEO System Monitor Dashboard")
        lines.append(f"Check Time: {metrics['check_time']}")
        lines.append("="*60)
        
        lines.append(f"\n[System Statistics]")
        lines.append(f"  Python Scripts: {metrics['script_count']}")
        lines.append(f"  Report Files: {metrics['report_count']}")
        
        lines.append(f"\n[Recent Reports]")
        for report in metrics['recent_reports']:
            lines.append(f"  - {report['name']} ({report['time']})")
        
        lines.append(f"\n[Module Health]")
        for name, status in metrics['module_health'].items():
            icon = "[OK]" if status['exists'] else "[FAIL]"
            size_kb = status['size'] / 1024 if status['size'] else 0
            lines.append(f"  {icon} {name}: {size_kb:.1f} KB")
        
        lines.append(f"\n[System Status]")
        all_ok = all(s['exists'] for s in metrics['module_health'].values())
        if all_ok:
            lines.append("  [OK] All core modules operational")
        else:
            lines.append("  [WARNING] Some modules abnormal")
        
        return "\n".join(lines)

def main():
    """主程式"""
    monitor = SystemMonitor()
    metrics = monitor.generate_dashboard()
    output = monitor.format_dashboard(metrics)
    
    # 儲存監控數據
    data_file = f"monitor_data_{datetime.now().strftime('%Y%m%d')}.json"
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)
    
    # 儲存報告
    report_file = f"monitor_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(output)
    
    print(f"監控完成，報告已寫入 {report_file}")
    return metrics

if __name__ == "__main__":
    main()
