@echo off
title dkYield99 Stop
echo ============================================================
echo   Stopping dkYield99 server (port 5000)...
echo ============================================================

set FOUND=0
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
  taskkill /F /PID %%a >nul 2>nul
  echo   Killed PID %%a
  set FOUND=1
)

if "%FOUND%"=="0" (
  echo   No server is running on port 5000.
) else (
  echo   Done - port 5000 is now free.
)
echo ============================================================
timeout /t 2 >nul
