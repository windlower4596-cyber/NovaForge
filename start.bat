@echo off
echo ======================================================
echo           STARTING NOVAFORGE AI SERVICES
echo ======================================================

echo [1/3] Starting Standalone MCP Server on port 8001...
start "NovaForge MCP Server" cmd /k "python backend/mcp_server.py"

echo [2/3] Starting FastAPI Backend Server on port 8000...
start "NovaForge Backend" cmd /k "python backend/run.py"

echo [3/3] Starting Vite React Frontend on port 3000...
start "NovaForge Frontend" cmd /k "cd frontend && npm run dev -- --port 3000"

echo.
echo Services launched! Opening http://localhost:3000 in your browser in 5 seconds...
timeout /t 5 >nul
start http://localhost:3000
echo.
echo All servers are running. Close the spawned terminal windows to stop the services.
pause
