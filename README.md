# 📚 Document RAG System

> Hệ thống RAG (Retrieval-Augmented Generation) cho phép upload, index và truy vấn tài liệu bằng AI.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-compose-blue.svg)](docker-compose.yml)
[![.NET](https://img.shields.io/badge/.NET-9.0-purple.svg)](backend/)
[![Angular](https://img.shields.io/badge/Angular-19-red.svg)](frontend/)
[![Python](https://img.shields.io/badge/Python-3.12-yellow.svg)](indexer/)

**[Quick Start](QUICK_START.md)** | **[Documentation](docs/INDEX.md)** | **[Deployment](DEPLOYMENT.md)** | **[Contributing](CONTRIBUTING.md)**

## Tech Stack

- **Frontend**: Angular 19 + Node 22
- **Backend API**: .NET 9
- **Document Processor**: Python 3.12
- **Vector DB**: Qdrant
- **Database**: SQL Server 2022
- **Message Queue**: Redis
- **AI**: OpenAI (GPT-4o-mini + text-embedding-3-small)
- **MCP Server**: Node.js
- **Deployment**: Docker Compose

## Features

✅ Upload tài liệu đa định dạng (PDF, DOCX, XLSX, PPTX, HTML, MD, TXT)  
✅ Xử lý bất đồng bộ với queue  
✅ RAG chat với AI (hiển thị sources + confidence score)  
✅ Quản lý categories  
✅ Search và pagination documents  
✅ Edit/Delete documents  
✅ Export chat history (JSON/CSV)  
✅ MCP Server để external repos kết nối  

## Quick Start

### Prerequisites

- Docker & Docker Compose
- OpenAI API key

### Setup

1. **Clone repository**

```bash
git clone <repo-url>
cd <repo-name>
```

2. **Create .env file**

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
SQL_SA_PASSWORD=YourStrong@Passw0rd123
OPENAI_API_KEY=sk-your-openai-api-key-here
```

3. **Start services**

```bash
docker-compose up --build
```

Wait for all services to start (takes ~2-3 minutes first time).

4. **Access the application**

- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:5000
- **Swagger**: http://localhost:5000/swagger
- **MCP Server**: http://localhost:3000
- **Qdrant UI**: http://localhost:6333/dashboard

## Architecture

```
┌─────────────────────────┐
│  OpenAI API (External)  │
│  - GPT-4o-mini          │
│  - Embedding Model      │
└──────────▲──────────────┘
           │ HTTPS
           │
┌──────────┼──────────────────────────────┐
│  Docker Compose                          │
│          │                               │
│  ┌───────┴───────┐     ┌──────────────┐ │
│  │  .NET API     │────►│   Qdrant     │ │
│  │  (RAG Service)│     │  Vector DB   │ │
│  └───────┬───────┘     └──────────────┘ │
│          │                               │
│  ┌───────▼───────┐     ┌──────────────┐ │
│  │  SQL Server   │     │    Redis     │ │
│  │  (Metadata)   │     │    Queue     │ │
│  └───────────────┘     └──────┬───────┘ │
│                                │         │
│  ┌─────────────────────────────▼──────┐ │
│  │  Python Indexer (Worker)          │ │
│  │  - Extract text                    │ │
│  │  - Generate embeddings             │ │
│  │  - Store vectors                   │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │  Angular Frontend (Port 4200)      │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │  MCP Server (Port 3000)            │ │
│  └────────────────────────────────────┘ │
└──────────────────────────────────────────┘
```

## Project Structure

```
/
├── docker-compose.yml          # Docker orchestration
├── .env                         # Environment variables
├── scripts/
│   └── init-db.sql             # Database initialization
│
├── backend/                     # .NET 9 API
│   ├── DocumentRAG.API/
│   ├── DocumentRAG.Core/
│   └── DocumentRAG.Infrastructure/
│
├── indexer/                     # Python document processor
│   ├── worker.py
│   ├── processors/
│   └── requirements.txt
│
├── frontend/                    # Angular 19 app
│   ├── src/
│   └── package.json
│
└── mcp-server/                  # MCP server (coming soon)
    └── src/
```

## Development

### Backend (.NET)

```bash
cd backend/DocumentRAG.API
dotnet run
```

### Frontend (Angular)

```bash
cd frontend
npm install
npm start
```

Navigate to http://localhost:4200

### Python Indexer

```bash
cd indexer
pip install -r requirements.txt
python worker.py
```

## API Endpoints

### Categories

- `GET /api/categories` - List all categories
- `POST /api/categories` - Create category
- `PUT /api/categories/{id}` - Update category
- `DELETE /api/categories/{id}` - Delete category

### Documents

- `POST /api/documents/upload` - Upload document
- `GET /api/documents` - List documents (pagination, search)
- `GET /api/documents/{id}` - Get document by ID
- `PUT /api/documents/{id}` - Update document
- `DELETE /api/documents/{id}` - Delete document

### Chat

- `POST /api/chat/query` - RAG query
- `POST /api/chat/sessions` - Create chat session
- `GET /api/chat/sessions/{id}` - Get session with messages
- `GET /api/chat/sessions/{id}/export?format=json|csv` - Export chat

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `SQL_SA_PASSWORD` | SQL Server SA password | Required |
| `CHUNK_SIZE` | Token chunk size | 500 |
| `CHUNK_OVERLAP` | Overlap between chunks | 50 |
| `RETRIEVAL_TOP_K` | Number of chunks to retrieve | 3 |

### Supported File Types

- **PDF**: `.pdf`
- **Word**: `.docx`, `.doc`
- **Excel**: `.xlsx`, `.xls`
- **PowerPoint**: `.pptx`, `.ppt`
- **HTML**: `.html`, `.htm`
- **Markdown**: `.md`, `.markdown`
- **Text**: `.txt`

## Troubleshooting

### Services not starting

Check logs:
```bash
docker-compose logs -f <service-name>
```

### Database connection failed

Wait for SQL Server to initialize (takes ~30s first time):
```bash
docker-compose logs -f sql-server
```

### OpenAI API errors

Verify API key in `.env` file and check quota.

### No documents found in chat

1. Check document status: should be "Completed"
2. Check Qdrant has vectors: http://localhost:6333/dashboard
3. Check logs: `docker-compose logs indexer`

## Cost Estimation

Per query:
- Embedding: ~$0.00002
- Chat: ~$0.00015
- **Total**: ~$0.00017/query

1000 queries/day ≈ $5/month

## Contributing

See [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for detailed architecture.

## License

MIT
