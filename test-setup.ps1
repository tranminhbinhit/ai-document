#!/usr/bin/env pwsh
# Test setup script

Write-Host "Testing DocumentRAG Setup" -ForegroundColor Green
Write-Host "=========================" -ForegroundColor Green

# Stop existing containers
Write-Host "1. Stopping existing containers..." -ForegroundColor Yellow
docker-compose down -v

# Build and start with clean state
Write-Host "2. Building and starting containers..." -ForegroundColor Yellow
docker-compose up --build -d

# Wait a bit for initialization
Write-Host "3. Waiting for services to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Check service status
Write-Host "4. Checking service status..." -ForegroundColor Yellow
docker-compose ps

# Test SQL Server and database
Write-Host "5. Testing database connection..." -ForegroundColor Yellow
docker exec rag-sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "${env:SQL_SA_PASSWORD}" -C -Q "SELECT name FROM sys.databases WHERE name = 'DocumentRAG'"

# Check if DocumentChunks table exists
Write-Host "6. Checking DocumentChunks table..." -ForegroundColor Yellow
docker exec rag-sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "${env:SQL_SA_PASSWORD}" -C -Q "USE DocumentRAG; SELECT COUNT(*) as TableExists FROM sys.tables WHERE name = 'DocumentChunks'"

Write-Host "7. Testing API endpoints..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

try {
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/categories" -Method GET
    Write-Host "✅ Backend API is responding" -ForegroundColor Green
    Write-Host "Categories count: $($response.Length)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Backend API failed: $($_.Exception.Message)" -ForegroundColor Red
}

try {
    $response = Invoke-RestMethod -Uri "http://localhost:6333/collections" -Method GET
    Write-Host "✅ Qdrant is responding" -ForegroundColor Green
} catch {
    Write-Host "❌ Qdrant failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "Setup test completed!" -ForegroundColor Green