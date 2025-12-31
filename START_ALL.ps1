# Court Summarizer - All-in-One Startup Script (PowerShell)
# Run: powershell -NoProfile -ExecutionPolicy Bypass -File "START_ALL.ps1"

Write-Host ""
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "Court Summarizer - Starting All Services" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

$rootDir = "C:\Users\LENOVO\Desktop\Court-Summarizer"
Set-Location $rootDir

Write-Host "[1/3] Starting FastAPI Server on port 8000..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootDir'; & '.\.venv\Scripts\Activate.ps1'; python -m uvicorn app_final5:app --host 0.0.0.0 --port 8000" -WindowStyle Normal

Start-Sleep -Seconds 3

Write-Host "[2/3] Starting Node API Server on port 5002..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootDir\db-connect'; `$env:PORT=5002; npm start" -WindowStyle Normal

Start-Sleep -Seconds 3

Write-Host "[3/3] Starting Frontend Vite Server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$rootDir\frontend'; npm run dev" -WindowStyle Normal

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ All services started successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Access the app at: http://localhost:5174" -ForegroundColor Yellow
Write-Host ""
Write-Host "Services:" -ForegroundColor Yellow
Write-Host "  - FastAPI:   http://localhost:8000" -ForegroundColor Gray
Write-Host "  - Node API:  http://localhost:5002" -ForegroundColor Gray
Write-Host "  - Frontend:  http://localhost:5174" -ForegroundColor Gray
Write-Host ""
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to exit this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
