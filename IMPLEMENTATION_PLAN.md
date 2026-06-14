# Implementation Plan - RAG Document System

## Tóm tắt Requirements

### Core Stack
- **Frontend**: Angular 19 + Node 22
- **Backend API**: .NET 9
- **Document Processor**: Python 3.12
- **Vector DB**: Qdrant (Docker)
- **Database**: SQL Server (Docker)
- **Storage**: Docker Volume
- **AI**: OpenAI (gpt-4o-mini + text-embedding-3-small)
- **MCP Server**: Để các repo khác kết nối và truy vấn tài liệu

### Key Features
- Chat với AI (hiển thị sources + confidence score)
- Upload tài liệu đa định dạng (PDF, DOCX, XLSX, PPTX, HTML, MD, TXT)
- Xử lý bất đồng bộ với queue
- Quản lý categories (tạo inline)
- Danh sách tài liệu với pagination (20/page) + search by title
- Xóa/sửa tài liệu
- Export chat history
- **MCP Server để external repos truy cập**

---

## Architecture Overview

```
                      ┌─────────────────────────┐
                      │   OpenAI API (External) │
                      │  - GPT-4o-mini (Chat)   │
                      │  - text-embedding-3-small│
                      └──────────▲──────────────┘
                                 │
                                 │ HTTPS
                                 │
┌────────────────────────────────┼─────────────────────────────┐
│                     Docker Compose                            │
├───────────────────────────────────────────────────────────────┤
│                                │                               │
│  ┌──────────────┐      ┌───────┴──────┐                      │
│  │   Angular    │──────│   .NET API   │                      │
│  │  Frontend    │ HTTP │  (Port 5000) │                      │
│  │  (Port 4200) │      │              │                      │
│  └──────────────┘      │  RAG Service │───────┐              │
│                        │  OpenAI Client│       │              │
│                        └───────┬───────┘       │              │
│                                │                │              │
│                                │                │              │
│  ┌─────────────┐       ┌──────▼────────┐  ┌───▼──────────┐  │
│  │ SQL Server  │◄──────│    Python     │  │   Qdrant     │  │
│  │  (Port 1433)│       │    Indexer    │─►│  Vector DB   │  │
│  │             │       │   (Worker)    │  │  (Port 6333) │  │
│  │ - Documents │       │               │  │              │  │
│  │ - Categories│       │ OpenAI Client │──┼──────────────┼──┘
│  │ - Chunks    │       └───────┬───────┘  │              │
│  │ - Chat Logs │               │          └──────────────┘
│  └─────────────┘         ┌─────▼──────┐                      │
│                          │   Redis    │                      │
│                          │   Queue    │                      │
│                          │ (Port 6379)│                      │
│                          └────────────┘                      │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │           MCP Server (Port 3000)                        │ │
│  │  - search_documents tool                               │ │
│  │  - query_rag tool (calls .NET API)                     │ │
│  │  - get_document tool                                   │ │
│  │  → External repos/agents connect here                  │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │      Docker Volume: document-storage                    │ │
│  │      - Uploaded files (PDF, DOCX, XLSX, etc.)          │ │
│  └────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────┘

Flow:
1. User uploads document → .NET API → Redis queue → Python Indexer
2. Python Indexer → Extract text → OpenAI embedding → Qdrant + SQL
3. User asks question → .NET API → Qdrant search → OpenAI chat → Response
4. External repo → MCP Server → .NET API → RAG response
```

---

## Project Structure

```
/
├── docker-compose.yml
├── .env
├── README.md
├── IMPLEMENTATION_PLAN.md
├── REQUIREMENTS_QUESTIONS.md
├── PLAN.md
│
├── frontend/                    # Angular 19
│   ├── Dockerfile
│   ├── package.json
│   ├── angular.json
│   ├── src/
│   │   ├── app/
│   │   │   ├── pages/
│   │   │   │   ├── chat/
│   │   │   │   ├── upload/
│   │   │   │   └── documents/
│   │   │   ├── services/
│   │   │   ├── models/
│   │   │   └── app.routes.ts
│   │   └── ...
│   └── ...
│
├── backend/                     # .NET 9 API
│   ├── Dockerfile
│   ├── DocumentRAG.sln
│   ├── DocumentRAG.API/
│   │   ├── Controllers/
│   │   ├── Services/
│   │   ├── Models/
│   │   ├── DTOs/
│   │   └── Program.cs
│   ├── DocumentRAG.Core/
│   └── DocumentRAG.Infrastructure/
│
├── indexer/                     # Python Document Processor
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── processors/
│   │   ├── pdf_processor.py
│   │   ├── docx_processor.py
│   │   ├── excel_processor.py
│   │   └── ...
│   ├── embedder.py
│   ├── chunker.py
│   └── worker.py
│
├── mcp-server/                  # MCP Server (Node.js/Python)
│   ├── Dockerfile
│   ├── package.json
│   ├── src/
│   │   ├── server.ts
│   │   ├── tools/
│   │   │   ├── search-documents.ts
│   │   │   ├── get-document.ts
│   │   │   └── query-rag.ts
│   │   └── ...
│   └── ...
│
└── scripts/
    └── init-db.sql              # SQL Server initialization
```

---

## Phase 1: Infrastructure Setup

### 1.1 Docker Compose Configuration

**Services:**
- `sql-server`: SQL Server 2022
- `qdrant`: Vector database
- `redis`: Message queue
- `backend`: .NET API
- `indexer`: Python worker
- `frontend`: Angular app
- `mcp-server`: MCP server
- `storage`: Named volume

### 1.2 Database Schema

```sql
-- Categories table
CREATE TABLE Categories (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(200) NOT NULL UNIQUE,
    Description NVARCHAR(500),
    CreatedAt DATETIME2 DEFAULT GETDATE()
);

-- Documents table
CREATE TABLE Documents (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Title NVARCHAR(500) NOT NULL,
    OriginalFileName NVARCHAR(500) NOT NULL,
    StorageFileName NVARCHAR(500) NOT NULL,
    FilePath NVARCHAR(1000) NOT NULL,
    FileSize BIGINT NOT NULL,
    FileType NVARCHAR(50) NOT NULL,
    CategoryId INT FOREIGN KEY REFERENCES Categories(Id),
    Status NVARCHAR(50) NOT NULL, -- Pending, Processing, Completed, Failed
    UploadedAt DATETIME2 DEFAULT GETDATE(),
    ProcessedAt DATETIME2 NULL,
    ErrorMessage NVARCHAR(MAX) NULL
);

-- Document Chunks (metadata only, vectors in Qdrant)
CREATE TABLE DocumentChunks (
    Id INT PRIMARY KEY IDENTITY(1,1),
    DocumentId INT FOREIGN KEY REFERENCES Documents(Id) ON DELETE CASCADE,
    ChunkIndex INT NOT NULL,
    Content NVARCHAR(MAX) NOT NULL,
    TokenCount INT NOT NULL,
    QdrantPointId NVARCHAR(100) NOT NULL, -- UUID in Qdrant
    CreatedAt DATETIME2 DEFAULT GETDATE()
);

-- Chat Sessions (for export)
CREATE TABLE ChatSessions (
    Id INT PRIMARY KEY IDENTITY(1,1),
    SessionId UNIQUEIDENTIFIER DEFAULT NEWID(),
    CreatedAt DATETIME2 DEFAULT GETDATE()
);

-- Chat Messages
CREATE TABLE ChatMessages (
    Id INT PRIMARY KEY IDENTITY(1,1),
    SessionId INT FOREIGN KEY REFERENCES ChatSessions(Id) ON DELETE CASCADE,
    Role NVARCHAR(20) NOT NULL, -- user, assistant
    Content NVARCHAR(MAX) NOT NULL,
    Sources NVARCHAR(MAX) NULL, -- JSON array of document IDs
    ConfidenceScore DECIMAL(5,4) NULL,
    CreatedAt DATETIME2 DEFAULT GETDATE()
);

-- Indexes
CREATE INDEX IX_Documents_CategoryId ON Documents(CategoryId);
CREATE INDEX IX_Documents_Status ON Documents(Status);
CREATE INDEX IX_DocumentChunks_DocumentId ON DocumentChunks(DocumentId);
CREATE INDEX IX_ChatMessages_SessionId ON ChatMessages(SessionId);
```

---

## Phase 2: Backend API (.NET 9)

### 2.1 Controllers

**DocumentController**
- `POST /api/documents/upload` - Upload file + enqueue processing
- `GET /api/documents` - List with pagination & search
- `GET /api/documents/{id}` - Get document details
- `DELETE /api/documents/{id}` - Delete document
- `PUT /api/documents/{id}` - Update document metadata

**CategoryController**
- `GET /api/categories` - List all categories
- `POST /api/categories` - Create new category
- `PUT /api/categories/{id}` - Update category
- `DELETE /api/categories/{id}` - Delete category

**ChatController**
- `POST /api/chat/query` - RAG query
- `POST /api/chat/sessions` - Create session
- `GET /api/chat/sessions/{id}` - Get session messages
- `GET /api/chat/sessions/{id}/export` - Export to JSON/CSV

### 2.2 Services

**DocumentService**
- Save file to storage
- Create database record
- Enqueue processing job (Redis)

**RAGService**
- Query Qdrant for relevant chunks
- Construct prompt with context
- Call OpenAI API
- Calculate confidence score

**QdrantService**
- Search vectors
- Get chunks by document ID

---

## Phase 3: Python Indexer

### 3.1 Document Processors

**Supported formats:**
- PDF: `PyPDF2` or `pdfplumber`
- DOCX: `python-docx`
- XLSX: `openpyxl`
- PPTX: `python-pptx`
- HTML: `BeautifulSoup4`
- Markdown: `markdown`
- TXT: built-in

### 3.2 Processing Pipeline

1. **Worker** listens to Redis queue
2. **Processor** extracts text from document
3. **Chunker** splits text (500 tokens, 50 overlap)
4. **Embedder** generates vectors (OpenAI)
5. **Store** in Qdrant + SQL metadata
6. **Update** document status

### 3.3 Key Libraries

```python
# requirements.txt
redis==5.0.0
pymssql==2.2.0
qdrant-client==1.7.0
openai==1.10.0
PyPDF2==3.0.0
python-docx==1.1.0
openpyxl==3.1.2
python-pptx==0.6.23
beautifulsoup4==4.12.0
markdown==3.5.0
tiktoken==0.5.0
```

---

## Phase 4: Frontend (Angular 19)

### 4.1 Pages

**1. Chat Page (`/chat`)**
- Input box với auto-resize
- Message list (user/assistant)
- Source documents chip/tag
- Confidence score badge
- Export button

**2. Upload Page (`/upload`)**
- File drag-drop zone
- Category dropdown với "Create New" option
- Inline input khi chọn "Create New"
- Progress bar/status
- Success/error notifications

**3. Documents Page (`/documents`)**
- Search input (by title)
- Category filter dropdown
- Document cards/table
- Pagination (20 items/page)
- Edit/Delete actions

### 4.2 Services

- `ApiService` - HTTP client wrapper
- `ChatService` - Chat state management
- `DocumentService` - Document CRUD
- `CategoryService` - Category management

### 4.3 Models/Interfaces

```typescript
interface Document {
  id: number;
  title: string;
  fileName: string;
  fileType: string;
  fileSize: number;
  categoryId: number;
  categoryName: string;
  status: string;
  uploadedAt: Date;
}

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  sources?: DocumentSource[];
  confidenceScore?: number;
  timestamp: Date;
}

interface DocumentSource {
  documentId: number;
  documentTitle: string;
  chunkContent: string;
}
```

---

## Phase 5: MCP Server

### 5.1 Purpose
Expose tài liệu qua Model Context Protocol để các repo/agents khác có thể:
- Search documents
- Query RAG system
- Get document content

### 5.2 MCP Tools

**search_documents**
```typescript
{
  name: "search_documents",
  description: "Search documents by title or content",
  inputSchema: {
    query: "string",
    category?: "string",
    limit?: "number"
  }
}
```

**query_rag**
```typescript
{
  name: "query_rag",
  description: "Ask question about documents using RAG",
  inputSchema: {
    question: "string",
    category?: "string"
  }
}
```

**get_document**
```typescript
{
  name: "get_document",
  description: "Get document by ID",
  inputSchema: {
    documentId: "number"
  }
}
```

### 5.3 Implementation Options

**Option A: Node.js/TypeScript MCP Server**
- Use `@modelcontextprotocol/sdk`
- Connect to .NET API backend
- Lightweight và dễ maintain

**Option B: Python MCP Server**
- Direct access to Qdrant + SQL
- Share code với indexer
- Better performance

**Recommend: Option A** (easier integration)

---

## Docker Compose Configuration

```yaml
version: '3.8'

services:
  sql-server:
    image: mcr.microsoft.com/mssql/server:2022-latest
    environment:
      - ACCEPT_EULA=Y
      - SA_PASSWORD=${SQL_SA_PASSWORD}
    ports:
      - "1433:1433"
    volumes:
      - sql-data:/var/opt/mssql
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init.sql

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant-data:/qdrant/storage

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    ports:
      - "5000:80"
    environment:
      - ConnectionStrings__DefaultConnection=${SQL_CONNECTION_STRING}
      - Qdrant__Url=http://qdrant:6333
      - Redis__Host=redis:6379
      - OpenAI__ApiKey=${OPENAI_API_KEY}
      - Storage__Path=/app/storage
    volumes:
      - document-storage:/app/storage
    depends_on:
      - sql-server
      - qdrant
      - redis

  indexer:
    build: ./indexer
    environment:
      - SQL_CONNECTION_STRING=${SQL_CONNECTION_STRING}
      - QDRANT_URL=http://qdrant:6333
      - REDIS_HOST=redis
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - STORAGE_PATH=/app/storage
    volumes:
      - document-storage:/app/storage
    depends_on:
      - sql-server
      - qdrant
      - redis

  frontend:
    build: ./frontend
    ports:
      - "4200:80"
    environment:
      - API_URL=http://backend:80

  mcp-server:
    build: ./mcp-server
    ports:
      - "3000:3000"
    environment:
      - API_URL=http://backend:80
      - MCP_PORT=3000
    depends_on:
      - backend

volumes:
  sql-data:
  qdrant-data:
  document-storage:
```

---

## Environment Variables (.env)

```env
# SQL Server
SQL_SA_PASSWORD=YourStrong@Passw0rd
SQL_CONNECTION_STRING=Server=sql-server,1433;Database=DocumentRAG;User Id=sa;Password=YourStrong@Passw0rd;TrustServerCertificate=True

# OpenAI
OPENAI_API_KEY=sk-...

# Application
CHUNK_SIZE=500
CHUNK_OVERLAP=50
EMBEDDING_MODEL=text-embedding-3-small
CHAT_MODEL=gpt-4o-mini
RETRIEVAL_TOP_K=3
```

---

## Implementation Steps

### Step 1: Setup Infrastructure (1 day)
1. Create `docker-compose.yml`
2. Create `.env` template
3. Create `init-db.sql` script
4. Test docker compose up

### Step 2: Backend API (3-4 days)
1. Create .NET solution structure
2. Implement database models & EF Core
3. Implement controllers & services
4. Add Redis queue integration
5. Add Qdrant client
6. Add OpenAI client
7. Test APIs với Postman/Swagger

### Step 3: Python Indexer (3-4 days)
1. Setup project structure
2. Implement document processors
3. Implement chunking logic
4. Implement embedding generation
5. Implement Redis worker
6. Implement Qdrant storage
7. Test với sample documents

### Step 4: Frontend (5-6 days)
1. Create Angular project
2. Setup routing & layout
3. Implement Chat page
4. Implement Upload page
5. Implement Documents page
6. Connect to API
7. Polish UI/UX

### Step 5: MCP Server (2-3 days)
1. Setup MCP server project
2. Implement MCP tools
3. Connect to backend API
4. Test với MCP client
5. Document usage

### Step 6: Integration & Testing (2-3 days)
1. End-to-end testing
2. Docker compose testing
3. Performance optimization
4. Documentation
5. README với setup instructions

---

## Total Estimated Time: 16-21 days

---

## Success Criteria

✅ User có thể upload documents qua web UI  
✅ Documents được xử lý bất đồng bộ và lưu vào vector DB  
✅ User có thể chat và nhận câu trả lời từ RAG  
✅ Hiển thị source documents và confidence score  
✅ User có thể quản lý categories  
✅ User có thể search, edit, delete documents  
✅ User có thể export chat history  
✅ MCP server hoạt động, external repos có thể query  
✅ Toàn bộ chạy trên Docker Compose  

---

## Next Steps

1. Xác nhận implementation plan này
2. Bắt đầu với Step 1: Infrastructure setup
3. Iterate qua từng phase

Bạn có muốn điều chỉnh gì không? Hoặc tôi bắt đầu implementation ngay?
