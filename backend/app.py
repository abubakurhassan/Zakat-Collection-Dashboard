from flask import Flask, jsonify, request
from flask_cors import CORS
from openpyxl import load_workbook
import os
from datetime import datetime, timedelta

# Use environment variable for file path, with fallback
EXCEL_FILE = os.environ.get('EXCEL_FILE', r"C:\path\to\your\file.xlsx")
SHEET = "Sheet1"
CELL = "B2"

app = Flask(__name__)
CORS(app)

# Simple cache
cache = {
    "value": None,
    "timestamp": None,
    "file_mtime": None
}
CACHE_DURATION = 60  # seconds

def file_has_changed():
    """Check if Excel file has been modified"""
    try:
        current_mtime = os.path.getmtime(EXCEL_FILE)
        return cache["file_mtime"] != current_mtime
    except OSError:
        return True

def get_total(sheet=SHEET, cell=CELL):
    """Read value from Excel with caching"""
    now = datetime.now()
    
    # Check if cache is valid
    if (cache["value"] is not None and 
        cache["timestamp"] and 
        now - cache["timestamp"] < timedelta(seconds=CACHE_DURATION) and
        not file_has_changed()):
        return cache["value"]
    
    # Read from Excel
    try:
        wb = load_workbook(EXCEL_FILE, data_only=True)
        ws = wb[sheet]
        value = ws[cell].value or 0
        
        # Update cache
        cache["value"] = value
        cache["timestamp"] = now
        cache["file_mtime"] = os.path.getmtime(EXCEL_FILE)
        
        return value
    except FileNotFoundError:
        return {"error": f"Excel file not found: {EXCEL_FILE}"}, 404
    except KeyError:
        return {"error": f"Sheet '{sheet}' not found"}, 404
    except Exception as e:
        return {"error": f"Error reading Excel: {str(e)}"}, 500

@app.route("/total")
def total():
    """Get total from Excel cell"""
    sheet = request.args.get("sheet", SHEET)
    cell = request.args.get("cell", CELL)
    
    result = get_total(sheet, cell)
    
    # Handle error responses
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    
    return jsonify({"total": result})

@app.route("/health")
def health():
    """Health check endpoint"""
    file_exists = os.path.exists(EXCEL_FILE)
    return jsonify({
        "status": "healthy" if file_exists else "unhealthy",
        "file_exists": file_exists,
        "cache_active": cache["value"] is not None
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)