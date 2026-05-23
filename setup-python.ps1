# ========================================
# Python PATH Setup Script
# ========================================
# Run this script to configure Python PATH
# or add this content to your PowerShell profile manually

Write-Host "`n=== Configuring Python PATH ===" -ForegroundColor Cyan

$pythonPath = "D:\Python314"
$scriptsPath = "D:\Python314\Scripts"

# Remove existing Python paths and WindowsApps
$pathParts = $env:Path -split ';' | Where-Object { 
    $_ -notlike "*Python*" -and 
    $_ -notlike "*python*" -and 
    $_ -notlike "*WindowsApps*" 
}

# Add our Python paths at the BEGINNING
$env:Path = "$pythonPath;$scriptsPath;$($pathParts -join ';')"

Write-Host "✅ Python PATH configured: $pythonPath" -ForegroundColor Green
Write-Host "✅ Scripts PATH: $scriptsPath" -ForegroundColor Green

# Test
Write-Host "`nTesting Python..." -ForegroundColor Yellow
python --version
pip --version

Write-Host "`n=== Setup Complete! ===" -ForegroundColor Green
Write-Host "Tip: To make this permanent, manually add the above code to:"
Write-Host "     $PROFILE"
