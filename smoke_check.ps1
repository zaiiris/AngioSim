$ErrorActionPreference = "Stop"

$Api = "http://127.0.0.1:8000"

Write-Host "Checking API health..."
Invoke-RestMethod "$Api/api/health" | Out-Null

Write-Host "Checking demo auth..."
$loginBody = @{ email = "ziada@angiosim.local"; password = "demo" } | ConvertTo-Json
$user = Invoke-RestMethod "$Api/api/auth/login" -Method Post -ContentType "application/json" -Body $loginBody

Write-Host "Checking dashboard..."
Invoke-RestMethod "$Api/api/dashboard/summary?user_id=$($user.user.id)" | Out-Null

Write-Host "Checking lessons and leaderboard..."
Invoke-RestMethod "$Api/api/lessons" | Out-Null
Invoke-RestMethod "$Api/api/leaderboard" | Out-Null

Write-Host "Checking session + hardware event..."
$sessionBody = @{ user_id = $user.user.id; mode = "ord"; vessel_size = "6mm"; goal = "tech" } | ConvertTo-Json
$session = Invoke-RestMethod "$Api/api/sessions" -Method Post -ContentType "application/json" -Body $sessionBody
$hardwareBody = @{
  session_id = $session.session.id
  events = @(
    @{ sensor_name = "flow"; value = 1.42; unit = "L/min" },
    @{ sensor_name = "circulation"; value = 86; unit = "bpm" }
  )
} | ConvertTo-Json -Depth 4
Invoke-RestMethod "$Api/api/hardware/events" -Method Post -ContentType "application/json" -Body $hardwareBody | Out-Null

Write-Host "Smoke check passed."
