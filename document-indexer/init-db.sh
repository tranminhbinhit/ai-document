#!/bin/bash

# Wait for SQL Server to be ready
echo "Waiting for SQL Server to start..."
sleep 30

# Run initialization script
echo "Running database initialization..."
/opt/mssql-tools/bin/sqlcmd -S sqlserver -U sa -P YourStrong@Password123 -i /docker-entrypoint-initdb.d/init.sql

echo "Database initialization complete!"
