@echo off
REM Court Summarizer - All-in-One Startup Script
REM This script starts all 3 services in separate windows

echo.
echo ========================================
echo Court Summarizer - Starting All Services
echo ========================================
echo.

REM Change to project directory
cd /d C:\Users\LENOVO\Desktop\Court-Summarizer

REM Terminal 1: FastAPI Server (Port 8000)
echo [1/3] Starting FastAPI Server on port 8000...
start "FastAPI Server" cmd /k "& '.\.venv\Scripts\Activate.ps1'; python -m uvicorn app_final5:app --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak

REM Terminal 2: Node API Server (Port 5002)
echo [2/3] Starting Node API Server on port 5002...
start "Node API Server" cmd /k "cd db-connect && set PORT=5002 && npm start"

timeout /t 3 /nobreak

REM Terminal 3: Frontend Vite Server (Port 5174)
echo [3/3] Starting Frontend Vite Server...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo ✅ All services started successfully!
echo ========================================
echo.
echo Access the app at: http://localhost:5174
echo.
echo Services:
echo  - FastAPI:   http://localhost:8000
echo  - Node API:  http://localhost:5002
echo  - Frontend:  http://localhost:5174
echo.
echo Close this window to exit the startup script
echo (Individual service windows will remain open)
echo ========================================
echo.

pause
