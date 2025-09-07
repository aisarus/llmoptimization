@echo off
setlocal
REM Vegan Recipe Builder Desktop launcher (Windows)
REM Put this file next to package.json

cd /d "%~dp0"
if not exist package.json (
  echo [x] Не найден package.json. Положи скрипт в корень проекта.
  pause
  exit /b 1
)

where node >nul 2>nul || (
  echo [x] Node.js не установлен или не в PATH: https://nodejs.org/
  pause
  exit /b 1
)

if not exist node_modules (
  echo [i] Устанавливаю зависимости...
  call npm install || exit /b 1
)

echo [>] Запускаю приложение...
call npm run dev
