@echo off
title dkYield99 Setup Check
cd /d "%~dp0"
set "PY=%~dp0python\python.exe"

echo ============================================================
echo   dkYield99 - everything is already included (Python + libraries)
echo   No separate Python installation is required.
echo   (Safe to run multiple times.)
echo ============================================================
echo.

rem --- Bundled Python must be present ---
if not exist "%PY%" (
  echo [ERROR] Bundled Python was not found: python\python.exe
  echo         Please copy the WHOLE folder again, including the 'python' folder.
  echo.
  pause
  exit /b 1
)
for /f "delims=" %%v in ('"%PY%" --version') do echo   Bundled Python: %%v

rem --- Libraries are pre-installed; only reinstall if somehow missing ---
"%PY%" -c "import fastapi, uvicorn, pydantic" >nul 2>nul
if not errorlevel 1 (
  echo   [OK] Libraries are ready. Nothing to install.
  goto :ready
)
echo   Installing libraries into the bundled Python (first time only) ...
"%PY%" -m pip install --no-warn-script-location -r "server\requirements.txt"
if errorlevel 1 (
  echo   [ERROR] Library setup failed. Check your internet connection and run again.
  pause
  exit /b 1
)

:ready
echo.
echo   [OK] Ready. To play, double-click _start.bat.
echo.
choice /c YN /n /m "Run now? (Y=Yes / N=No): "
if errorlevel 2 goto :done
call "%~dp0_start.bat"
:done
