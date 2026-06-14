#!/bin/bash

# Entrypoint script for SQL Server with auto database initialization

# Start SQL Server in background
/opt/mssql/bin/launchpad &

# Wait for SQL Server to start
echo "Waiting for SQL Server to start..."
sleep 30

# Check if database already exists
echo "Checking if DocumentRAG database exists..."
DB_EXISTS=$(/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$SA_PASSWORD" -C -h -1 -Q "SELECT COUNT(*) FROM sys.databases WHERE name = 'DocumentRAG'" 2>/dev/null | tr -d ' ')

if [ "$DB_EXISTS" -eq "0" ] || [ -z "$DB_EXISTS" ]; then
    echo "Database does not exist. Initializing database..."
    /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$SA_PASSWORD" -C -i /docker-entrypoint-initdb.d/init-db.sql
    
    if [ $? -eq 0 ]; then
        echo "Database initialized successfully!"
    else
        echo "Database initialization failed!"
        exit 1
    fi
else
    echo "Database already exists. Skipping initialization."
fi

# Keep SQL Server running in foreground
wait