# Quick Start Guide

## Prerequisites

- Docker Desktop installed and running
- OpenAI API key

## 🚀 5-Minute Setup

### Step 1: Clone & Configure

```bash
# Clone repository
git clone <your-repo-url>
cd document-rag-system

# Create environment file
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```env
SQL_SA_PASSWORD=YourStrong@Passw0rd123
OPENAI_API_KEY=sk-your-actual-openai-key-here
```

### Step 2: Start Everything

```bash
# Build and start all services
docker-compose up --build -d

# Wait for services to initialize (~60 seconds)
sleep 60

# Check status
docker-compose ps
```

You should see 7 services running:
- ✅ rag-sqlserver
- ✅ rag-qdrant
- ✅ rag-redis
- ✅ rag-backend
- ✅ rag-indexer
- ✅ rag-frontend
- ✅ rag-mcp-server

### Step 3: Access the Application

Open your browser:

- **Frontend**: http://localhost:4200
- **API Swagger**: http://localhost:5000/swagger
- **Qdrant Dashboard**: http://localhost:6333/dashboard

## 📝 First Use

### 1. Upload a Document

1. Go to http://localhost:4200/upload
2. Select a category (or create new)
3. Click or drag a file (PDF, DOCX, etc.)
4. Click "Upload Document"

The document will be processed in the background (~10-30 seconds).

### 2. Check Processing Status

1. Go to http://localhost:4200/documents
2. Find your document
3. Wait for status to change from "Processing" → "Completed"

### 3. Ask a Question

1. Go to http://localhost:4200/chat
2. Type a question about your document
3. Press Enter or click Send
4. See the AI response with sources!

## 🔍 Verify Installation

### Check Backend API

```bash
# Test categories endpoint
curl http://localhost:5000/api/categories

# Should return JSON with default categories
```

### Check Database

```bash
# Connect to SQL Server
docker exec -it rag-sqlserver /opt/mssql-tools/bin/sqlcmd \
  -S localhost -U sa -P 'YourStrong@Passw0rd123' \
  -Q "SELECT name FROM sys.databases"

# Should show DocumentRAG database
```

### Check Qdrant

```bash
# Check collections
curl http://localhost:6333/collections

# Should return documents collection
```

### Check Logs

```bash
# Backend logs
docker-compose logs -f backend

# Indexer logs
docker-compose logs -f indexer

# All logs
docker-compose logs -f
```

## 🐛 Troubleshooting

### Services not starting

```bash
# Stop all services
docker-compose down

# Remove volumes (fresh start)
docker-compose down -v

# Start again
docker-compose up --build -d
```

### Backend can't connect to database

```bash
# Check SQL Server is ready
docker-compose logs sql-server | grep "SQL Server is now ready"

# Restart backend after SQL is ready
docker-compose restart backend
```

### Document not processing

```bash
# Check indexer logs
docker-compose logs indexer

# Check Redis queue
docker exec -it rag-redis redis-cli
> LLEN document_processing
> LPOP document_processing
```

### OpenAI API errors

1. Verify API key in `.env` is correct
2. Check OpenAI quota: https://platform.openai.com/usage
3. Check backend logs: `docker-compose logs backend`

### Frontend not loading

```bash
# Check nginx logs
docker-compose logs frontend

# Rebuild frontend
docker-compose up --build frontend
```

## 🛑 Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (delete all data)
docker-compose down -v
```

## 📊 Monitor Resources

```bash
# View resource usage
docker stats

# View service status
docker-compose ps
```

## 🔧 Development Mode

If you want to run services locally for development:

### Backend

```bash
cd backend/DocumentRAG.API
dotnet run
```

### Frontend

```bash
cd frontend
npm install
npm start
```

### Indexer

```bash
cd indexer
pip install -r requirements.txt
python worker.py
```

## 📚 Test Data

Create a test document to try the system:

**test-document.md:**
```markdown
# Order Service Documentation

## Version 2.3 Changes

- Added bulk order creation endpoint
- New PENDING_PAYMENT status
- Email field now required

## Breaking Changes

1. Old /orders endpoint deprecated
2. Authentication required
3. Payment integration changed to PayPal
```

Save this and upload via the UI!

## 🎯 Next Steps

1. **Upload more documents** - Add your technical docs, PDFs, etc.
2. **Try different queries** - Ask questions about your documents
3. **Export chat history** - Save conversations as JSON/CSV
4. **Configure MCP** - Allow external tools to query your docs
5. **Customize categories** - Organize documents your way

## 💡 Tips

- **Chunking**: Documents are split into 500-token chunks with 50-token overlap
- **Retrieval**: Top 3 most relevant chunks are used for each query
- **Confidence**: Score shows how relevant the sources are
- **Processing time**: Varies by file size (10s - 2min typical)
- **Cost**: ~$0.00017 per query with OpenAI

## 📖 More Documentation

- `README.md` - Project overview
- `IMPLEMENTATION_PLAN.md` - Technical details
- `RAG_FLOW_DETAIL.md` - How RAG works
- `SETUP_GUIDE.md` - Complete setup instructions
- `PROJECT_STATUS.md` - Current status

## 🆘 Need Help?

1. Check logs: `docker-compose logs <service-name>`
2. Review `SETUP_GUIDE.md` Troubleshooting section
3. Verify environment variables in `.env`
4. Ensure Docker has enough resources (4GB+ RAM)

## ✅ Success Checklist

- [ ] All 7 Docker services running
- [ ] Can access frontend at http://localhost:4200
- [ ] Can access Swagger at http://localhost:5000/swagger
- [ ] Default categories visible
- [ ] Document uploaded successfully
- [ ] Document status changed to "Completed"
- [ ] Chat returns answer with sources
- [ ] Qdrant shows vectors in dashboard

---

**Ready to go!** 🎉

Your Document RAG system is now running. Upload documents and start asking questions!
