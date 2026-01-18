from flask import Flask, jsonify, request
from flask_cors import CORS
from openpyxl import load_workbook
import os
from datetime import datetime, timedelta

EXCEL_FILE = r"S:\Islamic Affairs\Zakat Section\Zakat Unit 2026\Corporate Affairs\Finance Unit\Account Statements\Account Statements Log.xlsx"
SHEET = "Sheet1"
CELL = "E3"

app = Flask(__name__)
CORS(app)

cache = {
    "value": None,
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

def get_total(sheet=SHEET, cell=CELL):
    now = datetime.now()
    
    if (cache["value"] is not None and 
        cache["timestamp"] and 
        now - cache["timestamp"] < timedelta(seconds=CACHE_DURATION) and
        not file_has_changed()):
        return cache["value"]
    
    try:
        wb = load_workbook(EXCEL_FILE, data_only=True)
        ws = wb[sheet]
        value = ws[cell].value or 0
        
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
    sheet = request.args.get("sheet", SHEET)
    cell = request.args.get("cell", CELL)
    
    result = get_total(sheet, cell)
    
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    
    return jsonify({"total": result})

@app.route("/health")
def health():
    file_exists = os.path.exists(EXCEL_FILE)
    return jsonify({
        "status": "healthy" if file_exists else "unhealthy",
        "file_exists": file_exists,
        "cache_active": cache["value"] is not None
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)