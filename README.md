# Zakat Collection Dashboard

A real-time dashboard that displays zakat collection totals from an Excel file with an elegant, modern interface.

![Dashboard Preview](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)

## 📋 Overview

This project provides a beautiful web-based dashboard that reads zakat collection data from a local Excel file and displays it in real-time. The dashboard automatically refreshes every 10 seconds to show the latest collection totals.

## ✨ Features

- 🎨 Modern, visually appealing dark blue interface
- 🔄 Auto-refresh every 10 seconds
- 💰 Real-time zakat collection total display
- 💾 Intelligent caching to reduce file reads
- 🎯 Simple one-click startup
- 📱 Responsive design (works on mobile/tablet)
- ⚡ Fast and lightweight
- 🕌 Clean, professional display for mosques and Islamic organizations

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Windows OS (for the .bat file)

### Installation

1. **Clone the repository:**
```bash
   git clone https://github.com/abubakurhassan/zakat-collection-dashboard.git
   cd zakat-collection-dashboard
```

2. **Install Python dependencies:**
```bash
   cd backend
   pip install -r requirements.txt
   cd ..
```

3. **Configure your Excel file:**
   
   Open `backend/app.py` and update the file path:
```python
   EXCEL_FILE = r"C:\path\to\your\zakat_collections.xlsx"
   SHEET = "Sheet1"  # Your sheet name
   CELL = "B2"       # The cell containing the total
```

4. **Run the dashboard:**
   
   Simply double-click `start webpage.bat`
   
   The Flask server will start and the dashboard will open in your browser automatically!

## 📁 Project Structure
```
zakat-collection-dashboard/
├── backend/
│   ├── app.py              # Flask API server
│   ├── requirements.txt    # Python dependencies
│   └── .gitignore         # Backend-specific ignores
├── frontend/
│   └── index.html         # Dashboard interface
├── start webpage.bat      # Startup script
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🔧 Configuration

### Changing the Excel Source

Edit `backend/app.py`:
```python
EXCEL_FILE = r"C:\your\path\to\zakat_collections.xlsx"  # Path to Excel file
SHEET = "Sheet1"                                          # Sheet name
CELL = "B2"                                               # Cell with total amount
```

### Changing Refresh Rate

Edit `frontend/index.html` (line ~285):
```javascript
setInterval(loadTotal, 10000);  // Change 10000 to desired milliseconds
```

### Changing Currency

Edit `frontend/index.html` to change from MVR to your currency:
```javascript
// Find this line and change MVR to your currency code
valueEl.innerHTML = `<span class="currency-symbol">USD</span>${formattedValue}`;
```

### Changing Colors

The dashboard uses a dark blue color scheme. To customize, edit the CSS in `frontend/index.html`:
```css
/* Main gradient colors */
background: linear-gradient(135deg, #3b82f6 0%, #1e3a8a 50%, #60a5fa 100%);
```

## 🎯 Usage

### Starting the Dashboard

**Option 1: Using the batch file (Recommended)**
- Double-click `start webpage.bat`
- Dashboard opens automatically in your browser

**Option 2: Manual start**
```bash
# Terminal 1: Start Flask server
cd backend
python app.py

# Terminal 2: Open the dashboard
# Just open frontend/index.html in your browser
```

### Stopping the Server

- Close the "Excel Dashboard API" command window, or
- Press `Ctrl+C` in the server window

### Using the Dashboard

- The dashboard displays the total zakat collection from your configured Excel cell
- Status indicator shows connection state (green = Live, red = Offline)
- Last update timestamp shows when data was last refreshed
- Values automatically update every 10 seconds
- Perfect for displaying on monitors, TVs, or tablets in your mosque or office

## 💡 Use Cases

- **Mosque Display**: Show live zakat collection totals on a TV/monitor
- **Office Monitoring**: Track collections in real-time for administrative purposes
- **Fundraising Events**: Display live donation totals during campaigns
- **Monthly Reports**: Keep staff updated on collection progress
- **Transparency**: Show the community current collection status

## 🔌 API Endpoints

The Flask backend provides these endpoints:

### `GET /total`
Returns the current zakat collection total from the Excel file.

**Response:**
```json
{
  "total": 12345.67
}
```

**Query Parameters:**
- `sheet` (optional): Override default sheet name
- `cell` (optional): Override default cell

**Example:**
```
http://127.0.0.1:5000/total?sheet=Collections&cell=D10
```

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "file_exists": true,
  "cache_active": true
}
```

## 🛠️ Development

### Backend (Flask)

The backend uses:
- **Flask**: Web framework
- **Flask-CORS**: Cross-origin resource sharing
- **openpyxl**: Excel file reading

### Frontend (HTML/JavaScript)

Pure HTML, CSS, and vanilla JavaScript - no frameworks required!

Features:
- Gradient animations
- Floating particle effects
- Glassmorphic design
- Responsive layout
- Professional typography

## 📝 Git Workflow
```bash
# Make changes to your code
git add .
git commit -m "Description of changes"
git push
```

**Note:** Your Excel file is automatically excluded from Git via `.gitignore` to protect sensitive collection data.

## ⚙️ Advanced Configuration

### Cache Settings

Modify cache duration in `backend/app.py`:
```python
CACHE_DURATION = 60  # seconds (default: 60)
```

### Network Access

To access from other devices on your network (e.g., display on a different computer or tablet):

1. Change in `backend/app.py`:
```python
   app.run(host="0.0.0.0", port=5000)  # Instead of 127.0.0.1
```

2. Find your computer's IP address:
```bash
   ipconfig  # Windows
```

3. Update `frontend/index.html`:
```javascript
   const res = await fetch("http://YOUR_IP:5000/total");
```

4. Access from other devices: `http://YOUR_IP/path/to/frontend/index.html`

### Kiosk Mode (For Dedicated Displays)

To run the dashboard in full-screen kiosk mode:
```batch
REM Add to start webpage.bat
start "" "chrome.exe" --kiosk --app="file:///%CD%\frontend\index.html"
```

## 🐛 Troubleshooting

### Dashboard shows "Connection Error"

- ✅ Make sure Flask server is running
- ✅ Check that the Excel file path is correct in `app.py`
- ✅ Verify the file exists and is not open in Excel
- ✅ Ensure the specified sheet and cell exist in your Excel file

### "Module not found" error
```bash
cd backend
pip install -r requirements.txt
```

### Excel file is locked

- Close Excel if the file is open
- Excel locks files when they're being edited
- The dashboard will show cached data until the file is available

### Port 5000 already in use

Change the port in `backend/app.py`:
```python
app.run(host="127.0.0.1", port=5001)  # Use different port
```

And update `frontend/index.html`:
```javascript
const res = await fetch("http://127.0.0.1:5001/total");
```

### Values not updating

- Check if the Excel file is being modified
- Verify the cache duration setting
- Ensure the cell reference is correct
- Check browser console for errors (F12)

## 🔒 Security Notes

- The dashboard is designed for **local network use only**
- Excel files containing sensitive data are excluded from Git
- CORS is enabled for local development
- For public deployment, additional security measures are required

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

Feel free to check the [issues page](https://github.com/abubakurhassan/zakat-collection-dashboard/issues).

## 👤 Author

**Your Name**
- GitHub: [@abubakurhassan](https://github.com/abubakurhassan)

## 🙏 Acknowledgments

- Flask framework for the backend API
- openpyxl library for Excel file handling
- Modern CSS gradient inspirations
- Islamic community for the inspiration

---

**Made with ❤️ for transparent zakat collection management**

*"The believer's shade on the Day of Resurrection will be his charity." - Al-Tirmidhi*