@echo off
title Zakat Dashboard - Online Mode
echo.
echo =================================
echo    ZAKAT COLLECTION DASHBOARD
echo    Starting in ONLINE MODE
echo =================================
echo.

REM Start Flask API
echo [1/3] Starting Flask server...
start "Zakat API Server" cmd /k "cd backend && python app.py"

REM Wait for Flask to start
timeout /t 5 /nobreak >nul

REM Start ngrok tunnel
echo [2/3] Creating secure public tunnel...
start "Ngrok Tunnel" cmd /k "C:\ngrok\ngrok.exe http 5000"

echo [3/3] Opening ngrok dashboard...
timeout /t 3 /nobreak >nul
start "" "http://127.0.0.1:4040"

echo.
echo =====================
echo    SETUP COMPLETE!
echo =====================
echo.
pause