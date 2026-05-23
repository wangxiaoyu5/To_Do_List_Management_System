# ========================================
# Frontend Startup Script
# ========================================

Write-Host "`n=== Starting Todo App Frontend ===" -ForegroundColor Cyan

# Change to frontend directory
cd frontend

Write-Host "`n=== Starting Vite dev server ===" -ForegroundColor Green
Write-Host "Server will run on: http://localhost:5173" -ForegroundColor Yellow
npm run dev
