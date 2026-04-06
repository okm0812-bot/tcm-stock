# -*- coding: utf-8 -*-
"""
Error Logging System - scripts/error_log.py
Records calculation errors with timestamp, module, error, and corrected value.
"""
import os, csv, sys
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "error_log.csv")


def _ensure_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Module", "Error_Type", "Error_Message", "Corrected_Value", "Raw_Value"])


def log_error(module: str, error_type: str, message: str, corrected: str = "", raw: str = ""):
    """
    Log an error to the CSV error log.

    Args:
        module: Script/module name (e.g. "adjusted_price.py")
        error_type: Category (e.g. "DivisionByZero", "TypeError", "EncodingError")
        message: Human-readable error description
        corrected: The corrected/expected value
        raw: The raw/incorrect value that caused the error
    """
    _ensure_log()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, module, error_type, message, corrected, raw])
    print(f"  [ERROR LOGGED] {timestamp} | {module} | {error_type}")


def query_errors(module: str = None, limit: int = 20) -> list:
    """
    Query error history.

    Args:
        module: Filter by module name (None = all)
        limit: Max number of records to return

    Returns:
        List of dicts: [{timestamp, module, error_type, message, corrected, raw}]
    """
    _ensure_log()
    results = []
    try:
        with open(LOG_FILE, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if module and row["Module"] != module:
                    continue
                results.append(row)
    except FileNotFoundError:
        return []

    return results[-limit:]


def print_errors(module: str = None, limit: int = 20):
    """Print error log to console."""
    errors = query_errors(module, limit)
    if not errors:
        print("No errors found.")
        return

    print(f"\n{'='*80}")
    print(f"Error Log {f'(Module: {module})' if module else '(All)'}")
    print(f"{'='*80}")
    for e in errors:
        print(f"  [{e['Timestamp']}] {e['Module']} | {e['Error_Type']}")
        print(f"    Message: {e['Error_Message']}")
        print(f"    Raw: {e['Raw_Value']} | Corrected: {e['Corrected_Value']}")
        print()


def error_summary() -> dict:
    """Return summary stats by module and error type."""
    errors = query_errors(limit=99999)
    if not errors:
        return {"total": 0}

    by_module = {}
    by_type = {}
    for e in errors:
        by_module[e["Module"]] = by_module.get(e["Module"], 0) + 1
        by_type[e["Error_Type"]] = by_type.get(e["Error_Type"], 0) + 1

    return {"total": len(errors), "by_module": by_module, "by_type": by_type}


if __name__ == "__main__":
    import sys as _sys
    module_filter = _sys.argv[1] if len(_sys.argv) > 1 else None
    limit = int(_sys.argv[2]) if len(_sys.argv) > 2 else 20

    print(f"Error Log Query (module={module_filter}, limit={limit})")
    print_errors(module_filter, limit)

    summary = error_summary()
    print(f"\nTotal errors: {summary['total']}")
    if summary.get("by_module"):
        print("By module:")
        for m, c in summary["by_module"].items():
            print(f"  {m}: {c}")
    if summary.get("by_type"):
        print("By type:")
        for t, c in summary["by_type"].items():
            print(f"  {t}: {c}")
