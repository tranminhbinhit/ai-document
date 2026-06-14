#!/bin/bash

# Quick start script for Document Indexer

echo "🚀 Starting Document Indexer Stack..."

# Kiểm tra Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose first."
    exit 1
fi

# Tạo .env nếu chưa có
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration"
fi

# Tạo thư mục documents nếu chưa có
if [ ! -d ./documents ]; then
    echo "📁 Creating documents directory..."
    mkdir -p ./documents
fi

# Start stack
echo "🐳 Starting Docker containers..."
docker-compose up -d

# Wait for SQL Server
echo "⏳ Waiting for SQL Server to be ready..."
sleep 10

# Check health
if docker-compose ps | grep -q "Up"; then
    echo "✅ Stack is running!"
    echo ""
    echo "📊 Services:"
    docker-compose ps
    echo ""
    echo "📝 Next steps:"
    echo "  1. Copy documents to ./documents folder"
    echo "  2. Check logs: docker-compose logs -f document-watcher"
    echo "  3. Query database: docker exec -it document-indexer-db /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P YourStrong@Password123"
    echo ""
    echo "🛑 To stop: docker-compose down"
else
    echo "❌ Failed to start stack. Check logs:"
    docker-compose logs
    exit 1
fi
