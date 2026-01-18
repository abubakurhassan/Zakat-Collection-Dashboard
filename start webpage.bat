@echo off
title Excel Dashboard
color 0A
echo ========================================
echo    Excel Dashboard Server
echo ========================================
echo.
echo Starting Flask API...
echo.
echo Dashboard will open in 3 seconds...
echo.

REM Wait a moment
timeout /t 3 /nobreak >nul

REM Open browser
start "" "frontend\index.html"

echo Browser opened!
echo.
echo Server is running at http://127.0.0.1:5000
echo Dashboard should be open in your browser
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start Flask in this window
cd backend
python app.py