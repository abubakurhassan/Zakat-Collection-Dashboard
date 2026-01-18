from flask import Flask, jsonify, request
from flask_cors import CORS
from openpyxl import load_workbook
import os
from datetime import datetime, timedelta

# Excel file configuration
EXCEL_FILE = r"S:\Islamic Affairs\Zakat Section\Zakat Unit 2026\Corporate Affairs\IT Unit\Collection-Dashboard\test_data.xlsx"
SHEET = "Sheet1"

# Cell references for summary data
TOTAL_CELL = "B2"           # Total collections
TOTAL_EXPENSES_CELL = "B3"  # Total expenses

# Expense categories location (Option B structure)
EXPENSE_CATEGORIES_START_ROW = 6  # First category row
EXPENSE_CATEGORY_COL = "C"        # Column with category names
EXPENSE_AMOUNT_COL = "D"          # Column with amounts
NUM_CATEGORIES = 7                 # Number of expense categories

# Chart data location
CHART_START_ROW = 15       # Starting row for daily collection data
CHART_DATE_COL = "A"       # Column with dates
CHART_VALUE_COL = "B"      # Column with daily amounts

app = Flask(__name__)
CORS(app)

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
        ws = wb[SHEET]
        
        # Get totals
        total = ws[TOTAL_CELL].value or 0
        total_expenses = ws[TOTAL_EXPENSES_CELL].value or 0
        balance = total - total_expenses
        
        # Get expense categories
        expense_categories = []
        for i in range(NUM_CATEGORIES):
            row = EXPENSE_CATEGORIES_START_ROW + i
            category_name = ws[f"{EXPENSE_CATEGORY_COL}{row}"].value
            category_amount = ws[f"{EXPENSE_AMOUNT_COL}{row}"].value
            
            if category_name:  # Only add if category name exists
                expense_categories.append({
                    "name": str(category_name),
                    "amount": float(category_amount) if category_amount else 0
                })
        
        # Get chart data (daily collections)
        chart_labels = []
        chart_values = []
        
        row = CHART_START_ROW
        max_rows = 30  # Get last 30 days
        
        while row < CHART_START_ROW + max_rows:
            try:
                date_cell = ws[f"{CHART_DATE_COL}{row}"].value
                value_cell = ws[f"{CHART_VALUE_COL}{row}"].value
                
                # Stop if we hit an empty row
                if date_cell is None or date_cell == "":
                    break
                
                # Skip if value is not a number
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
        
        # If no chart data found, provide empty arrays
        if not chart_labels:
            chart_labels = []
            chart_values = []
        
        data = {
            "total": float(total),
            "expenses": float(total_expenses),
            "balance": float(balance),
            "expense_categories": expense_categories,
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
    except KeyError:
        return {"error": f"Sheet '{SHEET}' not found"}, 404
    except Exception as e:
        return {"error": f"Error reading Excel: {str(e)}"}, 500

@app.route("/dashboard")
def dashboard():
    """Get complete dashboard data"""
    result = get_dashboard_data()
    
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    
    return jsonify(result)

@app.route("/total")
def total():
    """Legacy endpoint for backward compatibility"""
    result = get_dashboard_data()
    
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    
    return jsonify({"total": result.get("total", 0)})

@app.route("/health")
def health():
    file_exists = os.path.exists(EXCEL_FILE)
    return jsonify({
        "status": "healthy" if file_exists else "unhealthy",
        "file_exists": file_exists,
        "cache_active": cache["data"] is not None
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)