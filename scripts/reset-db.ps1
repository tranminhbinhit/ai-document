#!/usr/bin/env pwsh
# Reset database script for Windows

Write-Host "Resetting DocumentRAG database..." -ForegroundColor Green

# Load environment variables
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if ($_ -match "^([^=]+)=(.*)$") {
            [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
        }
    }
}

$sqlPassword = $env:SQL_SA_PASSWORD
if (-not $sqlPassword) {
    $sqlPassword = "YourStrong@Passw0rd123"
}

Write-Host "Using SQL SA Password: $sqlPassword" -ForegroundColor Yellow

# Wait for SQL Server to be ready
Write-Host "Checking if SQL Server is ready..." -ForegroundColor Yellow
$maxAttempts = 30
$attempt = 0

do {
    $attempt++
    Write-Host "Attempt $attempt/$maxAttempts..." -ForegroundColor Cyan
    
    try {
        $result = docker exec rag-sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$sqlPassword" -C -Q "SELECT 1" -h -1 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "SQL Server is ready!" -ForegroundColor Green
            break
        }
    }
    catch {
        Write-Host "SQL Server not ready yet..." -ForegroundColor Yellow
    }
    
    if ($attempt -lt $maxAttempts) {
        Start-Sleep -Seconds 2
    }
} while ($attempt -lt $maxAttempts)

if ($attempt -eq $maxAttempts) {
    Write-Host "SQL Server failed to become ready!" -ForegroundColor Red
    exit 1
}

# Run the reset script
Write-Host "Running database reset script..." -ForegroundColor Yellow
docker exec -i rag-sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$sqlPassword" -C -i /docker-entrypoint-initdb.d/reset-db.sql

if ($LASTEXITCODE -eq 0) {
    Write-Host "Database reset completed successfully!" -ForegroundColor Green
} else {
    Write-Host "Database reset failed!" -ForegroundColor Red
    exit 1
}