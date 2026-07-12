@echo off
title FootGolf Project Manager

:menu
cls
echo ===================================
echo     FootGolf Project Manager
echo ===================================
echo 1. Start Project (Backend + Frontend)
echo 2. Stop Project
echo 3. Exit
echo ===================================
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" goto start
if "%choice%"=="2" goto stop
if "%choice%"=="3" goto exit
goto menu

:start
echo Starting Backend...
cd /d "%~dp0backend"
start "FootGolf-Backend" cmd /k ".\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo Starting Frontend...
cd /d "%~dp0frontend"
start "FootGolf-Frontend" cmd /k "npm run dev"

cd /d "%~dp0"
echo.
echo Project started!
timeout /t 2 >nul
goto menu

:stop
echo.
echo Stopping FootGolf processes...
taskkill /FI "WINDOWTITLE eq FootGolf-Backend*" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq FootGolf-Frontend*" /T /F >nul 2>&1
echo Project stopped!
timeout /t 2 >nul
goto menu

:exit
exit
