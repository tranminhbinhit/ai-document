#!/bin/bash

# Custom entrypoint for SQL Server with automatic database initialization

# Start SQL Server in background
echo "Starting SQL Server..."
/opt/mssql/bin/launchpad &
SQL_PID=$!

# Function to check if SQL Server is ready
wait_for_sql() {
    echo "Waiting for SQL Server to be ready..."
    local counter=0
    while ! /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$SA_PASSWORD" -C -Q "SELECT 1" > /dev/null 2>&1; do
        counter=$((counter + 1))
        if [ $counter -gt 60 ]; then
            echo "SQL Server failed to start within 60 attempts"
            exit 1
        fi
        echo "Attempt $counter: SQL Server not ready yet, waiting..."
        sleep 2
    done
    echo "SQL Server is ready!"
}

# Wait for SQL Server to be ready
wait_for_sql

# Check if database already exists
echo "Checking if DocumentRAG database exists..."
DB_EXISTS=$(/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$SA_PASSWORD" -C -h -1 -Q "SELECT COUNT(*) FROM sys.databases WHERE name = 'DocumentRAG'" 2>/dev/null | tr -d ' \r\n')

if [ "$DB_EXISTS" != "1" ]; then
    echo "Database does not exist or check failed. Running initialization..."
    
    # Run initialization script
    if [ -f "/docker-entrypoint-initdb.d/init-db.sql" ]; then
        echo "Running init-db.sql..."
        /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$SA_PASSWORD" -C -i /docker-entrypoint-initdb.d/init-db.sql
        
        if [ $? -eq 0 ]; then
            echo "Database initialization completed successfully!"
        else
            echo "Database initialization failed!"
            exit 1
        fi
    else
        echo "Warning: init-db.sql not found!"
    fi
else
    echo "Database DocumentRAG already exists. Skipping initialization."
fi

echo "SQL Server initialization completed. Server is ready for connections."

# Keep SQL Server running in foreground
wait $SQL_PID