@echo off
title dkYield99 Server
cd /d "%~dp0"
set "PY=%~dp0python\python.exe"

rem --- If a server is already running on port 5000, just open the browser ---
netstat -ano | findstr ":5000" | findstr "LISTENING" >nul 2>nul
if not errorlevel 1 (
  echo dkYield99 server is already running on port 5000.
  echo Opening http://127.0.0.1:5000 in your browser...
  start "" http://127.0.0.1:5000
  ping -n 3 127.0.0.1 >nul 2>nul
  exit /b 0
)

rem --- Bundled Python ships inside the 'python' folder - no install needed ---
if not exist "%PY%" (
  echo [ERROR] Bundled Python was not found: python\python.exe
  echo         Please copy the WHOLE folder again, including the 'python' folder.
  echo.
  pause
  exit /b 1
)

rem --- Libraries are pre-installed in the bundle; self-heal only if missing ---
"%PY%" -c "import fastapi, uvicorn" >nul 2>nul
if errorlevel 1 (
  echo First-run setup: installing libraries into the bundled Python ...
  "%PY%" -m pip install --no-warn-script-location -r "server\requirements.txt"
)

echo ============================================================
echo   Starting dkYield99 - Chemical Process Tycoon
echo   The browser will open at http://127.0.0.1:5000
echo   (Keep this window open. Press Ctrl + C to stop.)
echo ============================================================
start "" cmd /c "timeout /t 3 >nul & start http://127.0.0.1:5000"
cd /d "%~dp0server"
"%PY%" run.py
echo.
echo Server stopped.
pause
