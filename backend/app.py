from flask import Flask, jsonify, request
from flask_cors import CORS
from openpyxl import load_workbook
import os
from datetime import datetime, timedelta

# Excel file configuration
EXCEL_FILE = r"S:\Islamic Affairs\Zakat Section\Zakat Unit 2026\Corporate Affairs\Finance Unit\Zakat Fund Budget\Master Sheet\ZF Master Sheet (01 Jan 2026 - 31 Dec 2026).xlsx"  # UPDATE THIS PATH

# Sheet names
SUMMARY_SHEET = "Summary"
ACCOUNT_SHEET = "Account_Statement"
CHART_SHEET = "Collection"

# Summary sheet cell references
TOTAL_COLLECTIONS_CELL = "C4"
ROI_CELL = "C6"
TOTAL_EXPENSES_CELL = "C7"

# Beneficiary Distribution (C8:C14 = 7 categories)
BENEFICIARY_START_ROW = 8
BENEFICIARY_CATEGORY_COL = "B"  # Category names
BENEFICIARY_AMOUNT_COL = "C"    # Amounts
NUM_BENEFICIARY_CATEGORIES = 7

# Investment (C15)
INVESTMENT_ROW = 15
INVESTMENT_CATEGORY_COL = "B"
INVESTMENT_AMOUNT_COL = "C"

# Account Statement sheet
ACCOUNT_BALANCE_CELL = "H3"

# Chart data (in Collections sheet)
CHART_START_ROW = 4       # Adjust if different
CHART_DATE_COL = "B"
CHART_VALUE_COL = "E"

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

cache = {
    "data": None,
    "timestamp": None,
    "file_mtime": None
}
CACHE_DURATION = 60

def file_has_changed():
    try:
        current_mtime = os.path.getmtime(EXCEL_FILE)
        return cache["file_mtime"] != current_mtime
    except OSError:
        return True

def get_dashboard_data():
    now = datetime.now()
    
    # Check cache
    if (cache["data"] is not None and 
        cache["timestamp"] and 
        now - cache["timestamp"] < timedelta(seconds=CACHE_DURATION) and
        not file_has_changed()):
        return cache["data"]
    
    try:
        wb = load_workbook(EXCEL_FILE, data_only=True)
        
        # Get Summary sheet
        summary_ws = wb[SUMMARY_SHEET]
        
        # Get main metrics
        total_collections = summary_ws[TOTAL_COLLECTIONS_CELL].value or 0
        roi = summary_ws[ROI_CELL].value or 0
        total_expenses = summary_ws[TOTAL_EXPENSES_CELL].value or 0
        
        # Get Account Balance from Account Statement sheet
        account_ws = wb[ACCOUNT_SHEET]
        account_balance = account_ws[ACCOUNT_BALANCE_CELL].value or 0
        
        # Get Beneficiary Distribution categories (7 items)
        beneficiary_categories = []
        for i in range(NUM_BENEFICIARY_CATEGORIES):
            row = BENEFICIARY_START_ROW + i
            category_name = summary_ws[f"{BENEFICIARY_CATEGORY_COL}{row}"].value
            category_amount = summary_ws[f"{BENEFICIARY_AMOUNT_COL}{row}"].value
            
            if category_name:
                beneficiary_categories.append({
                    "name": str(category_name),
                    "amount": float(category_amount) if category_amount else 0
                })
        
        # Get Investment category (1 item)
        investment_name = summary_ws[f"{INVESTMENT_CATEGORY_COL}{INVESTMENT_ROW}"].value or "Zakat Investments"
        investment_amount = summary_ws[f"{INVESTMENT_AMOUNT_COL}{INVESTMENT_ROW}"].value or 0
        
        investment_category = {
            "name": str(investment_name),
            "amount": float(investment_amount)
        }
        
        # Get chart data (daily collections) from Summary sheet
        chart_ws = wb[CHART_SHEET]
        chart_labels = []
        chart_values = []
        
        row = CHART_START_ROW
        max_rows = 30
        
        while row < CHART_START_ROW + max_rows:
            try:
                date_cell = chart_ws[f"{CHART_DATE_COL}{row}"].value
                value_cell = chart_ws[f"{CHART_VALUE_COL}{row}"].value
                
                if date_cell is None or date_cell == "":
                    break
                
                if value_cell is None or value_cell == "" or isinstance(value_cell, str):
                    row += 1
                    continue
                
                # Format date
                if isinstance(date_cell, datetime):
                    date_str = date_cell.strftime("%b %d")
                else:
                    date_str = str(date_cell)
                
                chart_labels.append(date_str)
                chart_values.append(float(value_cell))
                    
            except (ValueError, TypeError) as e:
                print(f"Skipping row {row}: {e}")
            
            row += 1
        
        # Build response data
        data = {
            "total_collections": float(total_collections),
            "roi": float(roi),
            "total_expenses": float(total_expenses),
            "account_balance": float(account_balance),
            "beneficiary_distribution": beneficiary_categories,
            "investments": investment_category,
            "chart": {
                "labels": chart_labels,
                "values": chart_values
            }
        }
        
        # Update cache
        cache["data"] = data
        cache["timestamp"] = now
        cache["file_mtime"] = os.path.getmtime(EXCEL_FILE)
        
        return data
        
    except FileNotFoundError:
        return {"error": f"Excel file not found: {EXCEL_FILE}"}, 404
    except KeyError as e:
        return {"error": f"Sheet not found: {str(e)}"}, 404
    except Exception as e:
        return {"error": f"Error reading Excel: {str(e)}"}, 500

@app.route("/dashboard")
def dashboard():
    """Get complete dashboard data"""
    result = get_dashboard_data()
    
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    
    return jsonify(result)

@app.route("/health")
def health():
    file_exists = os.path.exists(EXCEL_FILE)
    return jsonify({
        "status": "healthy" if file_exists else "unhealthy",
        "file_exists": file_exists,
        "cache_active": cache["data"] is not None
    })

if __name__ == "__main__":
    print("="*50)
    print("Starting Zakat Dashboard API")
    print("Access locally at: http://127.0.0.1:5000/dashboard")
    print("="*50)
    app.run(host="0.0.0.0", port=5000, debug=True)