#!/bin/bash

# System check script
echo "======================================"
echo "Document RAG System - Health Check"
echo "======================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Docker
echo -n "Checking Docker... "
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓ Installed${NC}"
else
    echo -e "${RED}✗ Not installed${NC}"
    exit 1
fi

# Check Docker Compose
echo -n "Checking Docker Compose... "
if command -v docker-compose &> /dev/null; then
    echo -e "${GREEN}✓ Installed${NC}"
else
    echo -e "${RED}✗ Not installed${NC}"
    exit 1
fi

# Check .env file
echo -n "Checking .env file... "
if [ -f ".env" ]; then
    echo -e "${GREEN}✓ Exists${NC}"
    
    # Check for OpenAI key
    if grep -q "OPENAI_API_KEY=sk-" .env; then
        echo -e "  ${GREEN}✓ OpenAI API key configured${NC}"
    else
        echo -e "  ${YELLOW}⚠ OpenAI API key not configured${NC}"
        echo "  Please add your OpenAI API key to .env file"
    fi
else
    echo -e "${RED}✗ Not found${NC}"
    echo "  Run: cp .env.example .env"
    exit 1
fi

echo ""
echo "Checking running services..."
echo ""

# Check services
services=("sql-server" "qdrant" "redis" "backend" "indexer" "frontend" "mcp-server")
for service in "${services[@]}"; do
    container="rag-${service}"
    echo -n "  $service: "
    if docker ps --format '{{.Names}}' | grep -q "^${container}$"; then
        echo -e "${GREEN}✓ Running${NC}"
    else
        echo -e "${RED}✗ Not running${NC}"
    fi
done

echo ""
echo "Checking service endpoints..."
echo ""

# Check endpoints
check_endpoint() {
    url=$1
    name=$2
    
    echo -n "  $name: "
    if curl -s -o /dev/null -w "%{http_code}" "$url" | grep -q "200\|302"; then
        echo -e "${GREEN}✓ Accessible${NC}"
    else
        echo -e "${RED}✗ Not accessible${NC}"
    fi
}

check_endpoint "http://localhost:5000/api/categories" "Backend API"
check_endpoint "http://localhost:4200" "Frontend"
check_endpoint "http://localhost:6333/collections" "Qdrant"

echo ""
echo "======================================"
echo "Health Check Complete"
echo "======================================"
