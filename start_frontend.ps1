$ErrorActionPreference = "Stop"

Set-Location "$PSScriptRoot\frontend\static"

Write-Host "Starting AngioSim frontend on http://127.0.0.1:8080"
..\..\backend\.venv\Scripts\python.exe -m http.server 8080 --bind 127.0.0.1
