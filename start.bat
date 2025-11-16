@echo off
echo ==========================================
echo   Polymarket Event Viewer - Quick Start
echo ==========================================
echo.

REM Перевірка наявності Python
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo [32m✓[0m Python знайдено
    echo.
    echo Встановлення залежностей...
    pip install -q -r requirements.txt
    echo.
    echo [32m→[0m Запуск сервера...
    echo.
    python proxy-server.py
    goto :end
)

REM Перевірка наявності Node.js
node --version >nul 2>&1
if %errorlevel% == 0 (
    echo [32m✓[0m Node.js знайдено
    echo.
    echo Встановлення залежностей...
    call npm install --silent
    echo.
    echo [32m→[0m Запуск сервера...
    echo.
    node proxy-server.js
    goto :end
)

echo [31m✗[0m Помилка: Не знайдено ні Python, ні Node.js
echo.
echo Будь ласка, встановіть один з них:
echo   - Python 3: https://www.python.org/downloads/
echo   - Node.js: https://nodejs.org/
pause
exit /b 1

:end
