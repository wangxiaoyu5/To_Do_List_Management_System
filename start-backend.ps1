# ========================================
# Backend Startup Script
# ========================================

Write-Host "`n=== Starting Todo App Backend ===" -ForegroundColor Cyan

# Configure Python PATH
$pythonPath = "D:\Python314"
$scriptsPath = "D:\Python314\Scripts"
$pathParts = $env:Path -split ';' | Where-Object { 
    $_ -notlike "*Python*" -and 
    $_ -notlike "*python*" -and 
    $_ -notlike "*WindowsApps*" 
}
$env:Path = "$pythonPath;$scriptsPath;$($pathParts -join ';')"

Write-Host "✅ Python PATH configured" -ForegroundColor Green

# Change to backend directory
cd backend

Write-Host "`n=== Starting Django server ===" -ForegroundColor Green
Write-Host "Server will run on: http://localhost:8000" -ForegroundColor Yellow
python manage.py runserver
