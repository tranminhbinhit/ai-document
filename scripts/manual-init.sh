#!/bin/bash

# Manual database initialization script
# Use this if automatic initialization fails

echo "Waiting for SQL Server to be ready..."
sleep 30

echo "Running initialization script..."

docker exec -i rag-sqlserver /opt/mssql-tools/bin/sqlcmd \
  -S localhost \
  -U sa \
  -P "${SQL_SA_PASSWORD}" \
  -i /docker-entrypoint-initdb.d/init-db.sql

echo "Database initialized successfully!"
