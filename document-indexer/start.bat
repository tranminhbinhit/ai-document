@echo off
REM Quick start script for Document Indexer (Windows)

echo Starting Document Indexer Stack...

REM Check Docker
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo Docker not found. Please install Docker Desktop first.
    exit /b 1
)

REM Check .env file
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please edit .env file with your configuration
)

REM Create documents directory
if not exist documents (
    echo Creating documents directory...
    mkdir documents
)

REM Start stack
echo Starting Docker containers...
docker-compose up -d

REM Wait for SQL Server
echo Waiting for SQL Server to be ready...
timeout /t 10 /nobreak >nul

REM Check status
docker-compose ps

echo.
echo Stack is running!
echo.
echo Next steps:
echo   1. Copy documents to .\documents folder
echo   2. Check logs: docker-compose logs -f document-watcher
echo.
echo To stop: docker-compose down

pause
