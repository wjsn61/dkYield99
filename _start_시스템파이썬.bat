@echo off
rem ============================================================
rem   내 PC 에 설치한 파이썬으로 게임을 켭니다.
rem
rem   폴더 안에 python\ 번들이 없을 때 쓰는 대체 실행 파일입니다.
rem   이 파일을 게임 폴더(_start.bat 옆)에 두고 더블클릭하세요.
rem ============================================================
title dk Lecture Server (system Python)
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] python 을 찾지 못했습니다.
  echo         python.org 에서 Python 3.10 이상을 설치하고,
  echo         설치 화면의 "Add python.exe to PATH" 를 꼭 체크하세요.
  echo.
  pause
  exit /b 1
)

for /f "delims=" %%v in ('python --version') do echo   Python: %%v

python -c "import fastapi, uvicorn, pydantic" >nul 2>nul
if errorlevel 1 (
  echo   처음 한 번만 - 라이브러리를 설치합니다 ...
  python -m pip install --no-warn-script-location -r "server\requirements.txt"
  if errorlevel 1 (
    echo [ERROR] 설치에 실패했습니다. 인터넷 연결을 확인하세요.
    pause
    exit /b 1
  )
)

echo ============================================================
echo   서버를 켭니다. 잠시 뒤 브라우저가 열립니다.
echo   (이 창을 닫지 마세요. 멈추려면 Ctrl + C)
echo ============================================================

rem  dkCity 는 8000, dkYield99 는 5000 을 씁니다 - run.py 가 알아서 정합니다
if exist "server\app\engine\process_engine.py" (
  start "" cmd /c "timeout /t 4 >nul & start http://127.0.0.1:5000"
) else (
  start "" cmd /c "timeout /t 4 >nul & start http://127.0.0.1:8000"
)

cd /d "%~dp0server"
python run.py

echo.
echo 서버가 멈췄습니다.
pause
