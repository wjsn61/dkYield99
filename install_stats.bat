@echo off
chcp 65001 >nul
title dkYield99 Statistics Lab Setup
cd /d "%~dp0"
set "PY=%~dp0python\python.exe"

echo ============================================================
echo   dkYield99 - Statistics Lab setup
echo.
echo   This is OPTIONAL. The game runs fine without it.
echo   You need this for:
echo     - lab\w12_chart.py            (drawing charts)
echo     - VS Code cell run (# %%%%)     Shift+Enter
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

rem --- Already installed? (both are needed, so check both) ---
"%PY%" -c "import matplotlib, ipykernel" >nul 2>nul
if not errorlevel 1 (
  echo   [OK] Statistics libraries are already installed.
  goto :verify
)

rem --- pip may be missing in an embeddable Python build ---
"%PY%" -m pip --version >nul 2>nul
if errorlevel 1 (
  if exist "wheels\get-pip.py" (
    echo   Bootstrapping pip from the bundled wheels folder ...
    "%PY%" "wheels\get-pip.py" --no-index --find-links "wheels" >nul
  ) else (
    echo   Bootstrapping pip from the internet ...
    "%PY%" -m ensurepip --default-pip >nul 2>nul
  )
)

rem --- Offline first: install from bundled wheels if the teacher shipped them ---
if exist "wheels\*.whl" (
  echo   Installing from bundled wheels ^(no internet needed^) ...
  "%PY%" -m pip install --no-index --find-links "wheels" --only-binary=:all: ^
      -r "server\requirements-stats.txt"
) else (
  echo   Installing from the internet ^(this may take a few minutes^) ...
  "%PY%" -m pip install --no-warn-script-location --only-binary=:all: ^
      -r "server\requirements-stats.txt"
)

if errorlevel 1 (
  echo.
  echo   [ERROR] Setup failed.
  echo           - Check your internet connection, or
  echo           - Ask your instructor for the 'wheels' folder ^(offline install^).
  echo.
  pause
  exit /b 1
)

:verify
echo.
echo   Checking that charts can actually be drawn ...
"%PY%" -c "import os,sys; os.environ.setdefault('MPLCONFIGDIR', r'%~dp0lab\.mplcache'); import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as p; p.figure(); p.plot([1,2],[1,2]); p.close(); print('   [OK] matplotlib works.')"
if errorlevel 1 (
  echo   [ERROR] matplotlib is installed but cannot draw. Tell your instructor.
  pause
  exit /b 1
)

"%PY%" -c "import pandas; print('   [OK] pandas works.')" 2>nul
if errorlevel 1 echo    [--] pandas not installed ^(optional - the lab still works^)

"%PY%" -c "import ipykernel; print('   [OK] VS Code cell run (# %%%%) is available.')" 2>nul
if errorlevel 1 echo    [--] ipykernel not installed ^(optional - plain 'python file.py' still works^)

echo.
echo ============================================================
echo   [OK] Ready.
echo.
echo   Next:  open a terminal in the 'lab' folder and run
echo            python w12_chart.py
echo   Charts are saved to  lab\figures\
echo.
echo   Tip: in VS Code, put  # %%%%  above a block and press
echo        Shift+Enter to run just that block.
echo        The file stays a normal .py - see docs\TOOLS.md
echo ============================================================
echo.
pause
