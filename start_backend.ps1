$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

if (-not (Test-Path "backend\.venv\Scripts\python.exe")) {
  Write-Host "Creating backend virtual environment..."
  python -m venv backend\.venv
}

Write-Host "Installing backend dependencies..."
backend\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt

Write-Host "Starting AngioSim API on http://127.0.0.1:8000"
Set-Location "$PSScriptRoot\backend"
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
