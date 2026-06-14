# Document RAG MCP Server

MCP (Model Context Protocol) server for Document RAG system, allowing external AI agents to query documents.

## Features

- **search_documents**: Search documents by title
- **query_rag**: Ask questions using RAG
- **get_document**: Get document by ID
- **list_categories**: List all categories

## Installation

```bash
npm install
npm run build
```

## Usage

### Standalone

```bash
npm start
```

### In Kiro

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "document-rag": {
      "command": "node",
      "args": ["/path/to/mcp-server/dist/server.js"],
      "env": {
        "API_URL": "http://localhost:5000/api"
      }
    }
  }
}
```

### Docker

```bash
docker-compose up mcp-server
```

## MCP Tools

### search_documents

Search for documents by title.

```typescript
{
  query: string;      // Search term
  category?: string;  // Filter by category name
  limit?: number;     // Max results (default: 20)
}
```

### query_rag

Ask a question about documents using RAG.

```typescript
{
  question: string;   // Your question
  categoryId?: number; // Filter by category ID
}
```

Returns AI-generated answer with sources and confidence score.

### get_document

Get detailed information about a specific document.

```typescript
{
  documentId: number; // Document ID
}
```

### list_categories

List all available document categories. No parameters required.

## Example Queries

**Search documents:**
```json
{
  "name": "search_documents",
  "arguments": {
    "query": "order service",
    "limit": 5
  }
}
```

**Ask a question:**
```json
{
  "name": "query_rag",
  "arguments": {
    "question": "What are the changes in the order service?"
  }
}
```

**Get document:**
```json
{
  "name": "get_document",
  "arguments": {
    "documentId": 45
  }
}
```

## Environment Variables

- `API_URL` - Backend API URL (default: http://localhost:5000/api)

## Development

```bash
# Watch mode
npm run dev

# Build only
npm run build
```
