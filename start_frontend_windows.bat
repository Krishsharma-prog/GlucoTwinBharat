@echo off
setlocal
cd /d "%~dp0frontend"
if not exist node_modules\vite\bin\vite.js (
  echo Installing frontend dependencies. An internet connection is required for the first run.
  npm install
  if errorlevel 1 (
    pause
    exit /b 1
  )
)
npm run dev
