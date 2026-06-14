# Setup Guide - Document RAG System

## Trạng thái hiện tại

✅ **Đã hoàn thành:**
- Docker Compose configuration
- Database schema (SQL Server)
- Backend .NET 9 API (hoàn chỉnh)
  - Controllers: Categories, Documents, Chat
  - Services: RAG, Document, Qdrant
  - Database context và entities
- Python Indexer (hoàn chỉnh)
  - Worker với Redis queue
  - Document processors (PDF, DOCX, XLSX, PPTX, HTML, MD, TXT)
  - Chunking và embedding
- Infrastructure setup scripts

🚧 **Cần hoàn thiện:**
- Angular Frontend (cần generate components)
- MCP Server (cần implement)

## Bước 1: Prerequisites

Cài đặt:
- Docker Desktop
- Git
- Node.js 22 (nếu dev frontend locally)
- .NET 9 SDK (nếu dev backend locally)

## Bước 2: Clone và Setup

```bash
# Clone repository
git clone <repo-url>
cd <repo-name>

# Tạo .env file
cp .env.example .env

# Edit .env và thêm OpenAI API key
nano .env
```

Nội dung `.env`:
```env
SQL_SA_PASSWORD=YourStrong@Passw0rd123
OPENAI_API_KEY=sk-your-actual-openai-key-here
```

## Bước 3: Hoàn thiện Angular Frontend

### Option A: Dùng Angular CLI (Recommended)

```bash
cd frontend

# Install Angular CLI
npm install -g @angular/cli@19

# Create new Angular 19 project (hoặc dùng structure đã tạo)
# ng new document-rag-app --routing --style=css --skip-git

# Install dependencies
npm install

# Generate components
ng generate component app/app --standalone --inline-template=false
ng generate component pages/chat --standalone
ng generate component pages/upload --standalone
ng generate component pages/documents --standalone

# Generate services
ng generate service services/api
ng generate service services/chat
ng generate service services/document
ng generate service services/category

# Generate models
ng generate interface models/document
ng generate interface models/category
ng generate interface models/chat
```

### Option B: Copy từ template

Tạo các files sau trong `frontend/src/app/`:

**app.component.ts:**
```typescript
import { Component } from '@angular/core';
import { RouterOutlet, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink],
  template: `
    <div class="app-container">
      <nav class="navbar">
        <h1>Document RAG System</h1>
        <div class="nav-links">
          <a routerLink="/chat" routerLinkActive="active">Chat</a>
          <a routerLink="/upload" routerLinkActive="active">Upload</a>
          <a routerLink="/documents" routerLinkActive="active">Documents</a>
        </div>
      </nav>
      <router-outlet></router-outlet>
    </div>
  `,
  styles: [`
    .app-container { min-height: 100vh; }
    .navbar {
      background: #007bff;
      color: white;
      padding: 1rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .nav-links { display: flex; gap: 1rem; }
    .nav-links a {
      color: white;
      text-decoration: none;
      padding: 0.5rem 1rem;
      border-radius: 4px;
    }
    .nav-links a:hover { background: rgba(255,255,255,0.1); }
    .nav-links a.active { background: rgba(255,255,255,0.2); }
  `]
})
export class AppComponent {}
```

**app.routes.ts:**
```typescript
import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: '/chat', pathMatch: 'full' },
  { 
    path: 'chat', 
    loadComponent: () => import('./pages/chat/chat.component').then(m => m.ChatComponent)
  },
  { 
    path: 'upload', 
    loadComponent: () => import('./pages/upload/upload.component').then(m => m.UploadComponent)
  },
  { 
    path: 'documents', 
    loadComponent: () => import('./pages/documents/documents.component').then(m => m.DocumentsComponent)
  }
];
```

## Bước 4: Hoàn thiện MCP Server

```bash
cd mcp-server

# Initialize Node.js project
npm init -y

# Install dependencies
npm install @modelcontextprotocol/sdk express

# Install dev dependencies
npm install -D @types/node @types/express typescript ts-node

# Create tsconfig.json
npx tsc --init
```

Tạo `mcp-server/src/server.ts`:
```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const API_URL = process.env.API_URL || 'http://localhost:5000';

const server = new Server({
  name: 'document-rag-mcp',
  version: '1.0.0',
}, {
  capabilities: {
    tools: {},
  },
});

// Tool: search_documents
server.setRequestHandler('tools/list', async () => ({
  tools: [
    {
      name: 'search_documents',
      description: 'Search documents by title or content',
      inputSchema: {
        type: 'object',
        properties: {
          query: { type: 'string' },
          category: { type: 'string', optional: true },
          limit: { type: 'number', optional: true }
        },
        required: ['query']
      }
    },
    {
      name: 'query_rag',
      description: 'Ask question about documents using RAG',
      inputSchema: {
        type: 'object',
        properties: {
          question: { type: 'string' },
          categoryId: { type: 'number', optional: true }
        },
        required: ['question']
      }
    }
  ]
}));

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
```

## Bước 5: Build và Deploy

### Development Mode

```bash
# Terminal 1: Start infrastructure
docker-compose up sql-server qdrant redis

# Terminal 2: Backend
cd backend/DocumentRAG.API
dotnet run

# Terminal 3: Indexer
cd indexer
pip install -r requirements.txt
python worker.py

# Terminal 4: Frontend
cd frontend
npm start
```

### Production Mode (Docker Compose)

```bash
# Build và start tất cả services
docker-compose up --build -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Bước 6: Verify Installation

1. **Check services health:**
```bash
# Backend API
curl http://localhost:5000/api/categories

# Qdrant
curl http://localhost:6333/collections

# Frontend
curl http://localhost:4200
```

2. **Test upload:**
- Go to http://localhost:4200/upload
- Select a category
- Upload a test PDF/DOCX file
- Check logs: `docker-compose logs indexer`

3. **Test chat:**
- Go to http://localhost:4200/chat
- Ask a question about uploaded documents
- Should see response with sources

## Bước 7: Database Initialization

Database được tự động khởi tạo khi start SQL Server container.

Nếu cần reset database:
```bash
docker-compose down -v
docker-compose up sql-server -d
```

## Troubleshooting

### Angular build fails

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Backend không kết nối được database

```bash
# Wait for SQL Server (takes ~30-60s)
docker-compose logs -f sql-server

# Check connection
docker exec -it rag-sqlserver /opt/mssql-tools/bin/sqlcmd \
  -S localhost -U sa -P 'YourStrong@Passw0rd123' \
  -Q "SELECT name FROM sys.databases"
```

### Indexer không xử lý documents

```bash
# Check Redis queue
docker exec -it rag-redis redis-cli
> LLEN document_processing

# Check indexer logs
docker-compose logs -f indexer
```

### OpenAI API errors

- Verify API key trong `.env`
- Check quota: https://platform.openai.com/usage
- Check rate limits

## Next Steps

1. **Frontend Development:**
   - Implement chat UI
   - Implement upload UI với drag-drop
   - Implement documents list với search
   - Add loading states và error handling

2. **MCP Server:**
   - Complete tool implementations
   - Add authentication
   - Document MCP usage

3. **Testing:**
   - Add unit tests
   - Add integration tests
   - Load testing

4. **Production:**
   - Add monitoring (Prometheus/Grafana)
   - Add logging (ELK stack)
   - SSL/TLS certificates
   - Backup strategy

## Câu hỏi thường gặp

**Q: Tôi có thể dùng model khác thay OpenAI không?**
A: Có, bạn cần modify RAGService và embedder.py để support models khác (Azure OpenAI, Anthropic, local models, etc.)

**Q: Làm sao để scale hệ thống?**
A: 
- Multiple indexer workers
- Load balancer cho backend
- Qdrant cluster
- Redis Sentinel/Cluster

**Q: Chi phí ước tính?**
A: ~$5/month cho 1000 queries/day với OpenAI gpt-4o-mini

**Q: Có cần GPU không?**
A: Không, đang dùng OpenAI API. Nếu chuyển sang local models thì cần GPU.
