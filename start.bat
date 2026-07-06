@echo off
echo ==========================================
echo  🚀 STARTING NOVAFORGE AI PLATFORM
echo ==========================================

echo.
echo [1/2] Launching Backend Server...
cd backend
start cmd /k "title NovaForge Backend Engine && python run.py"

echo.
echo [2/2] Launching Frontend UI...
cd ..\frontend
start cmd /k "title NovaForge Frontend UI && npm run dev"

echo.
echo 🌐 Opening your dashboard in the browser...
timeout /t 3 >nul
start http://localhost:5173

echo ==========================================
echo  🎉 Done! All systems are cleanly running.
echo ==========================================
pause