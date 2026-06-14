#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import fetch from 'node-fetch';

const API_URL = process.env.API_URL || 'http://localhost:5000/api';

interface SearchDocumentsArgs {
  query: string;
  category?: string;
  limit?: number;
}

interface QueryRAGArgs {
  question: string;
  categoryId?: number;
}

interface GetDocumentArgs {
  documentId: number;
}

// Create server instance
const server = new Server(
  {
    name: 'document-rag-mcp',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'search_documents',
        description: 'Search documents by title. Returns a list of documents matching the search query.',
        inputSchema: {
          type: 'object',
          properties: {
            query: {
              type: 'string',
              description: 'Search query for document titles',
            },
            category: {
              type: 'string',
              description: 'Optional category name to filter results',
            },
            limit: {
              type: 'number',
              description: 'Maximum number of results (default: 20)',
            },
          },
          required: ['query'],
        },
      },
      {
        name: 'query_rag',
        description: 'Ask a question about documents using RAG (Retrieval-Augmented Generation). The system will search relevant documents and provide an AI-generated answer with sources.',
        inputSchema: {
          type: 'object',
          properties: {
            question: {
              type: 'string',
              description: 'Question to ask about the documents',
            },
            categoryId: {
              type: 'number',
              description: 'Optional category ID to limit search scope',
            },
          },
          required: ['question'],
        },
      },
      {
        name: 'get_document',
        description: 'Get detailed information about a specific document by ID.',
        inputSchema: {
          type: 'object',
          properties: {
            documentId: {
              type: 'number',
              description: 'Document ID to retrieve',
            },
          },
          required: ['documentId'],
        },
      },
      {
        name: 'list_categories',
        description: 'List all available document categories.',
        inputSchema: {
          type: 'object',
          properties: {},
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'search_documents': {
        const typedArgs = (args || {}) as unknown as SearchDocumentsArgs;
        const { query, category, limit = 20 } = typedArgs;
        
        // Build query params
        const params = new URLSearchParams({
          page: '1',
          pageSize: limit.toString(),
          search: query,
        });

        if (category) {
          // First, get categories to find ID
          const categoriesResponse = await fetch(`${API_URL}/categories`);
          const categories: any = await categoriesResponse.json();
          const cat = categories.find((c: any) => 
            c.name.toLowerCase().includes(category.toLowerCase())
          );
          if (cat) {
            params.append('categoryId', cat.id.toString());
          }
        }

        const response = await fetch(`${API_URL}/documents?${params}`);
        const data: any = await response.json();

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(data, null, 2),
            },
          ],
        };
      }

      case 'query_rag': {
        const typedArgs = (args || {}) as unknown as QueryRAGArgs;
        const { question, categoryId } = typedArgs;

        const response = await fetch(`${API_URL}/chat/query`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: question,
            categoryId: categoryId || null,
          }),
        });

        const data: any = await response.json();

        // Format response with sources
        let result = `**Answer:**\n${data.message}\n\n`;
        
        if (data.sources && data.sources.length > 0) {
          result += `**Sources (${(data.confidenceScore * 100).toFixed(0)}% confidence):**\n`;
          data.sources.forEach((source: any, idx: number) => {
            result += `\n${idx + 1}. **${source.documentTitle}** (${(source.score * 100).toFixed(0)}% match)\n`;
            result += `   ${source.chunkContent.substring(0, 200)}...\n`;
          });
        }

        return {
          content: [
            {
              type: 'text',
              text: result,
            },
          ],
        };
      }

      case 'get_document': {
        const typedArgs = (args || {}) as unknown as GetDocumentArgs;
        const { documentId } = typedArgs;

        const response = await fetch(`${API_URL}/documents/${documentId}`);
        
        if (!response.ok) {
          throw new Error(`Document not found: ${documentId}`);
        }

        const data: any = await response.json();

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(data, null, 2),
            },
          ],
        };
      }

      case 'list_categories': {
        const response = await fetch(`${API_URL}/categories`);
        const data: any = await response.json();

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(data, null, 2),
            },
          ],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    return {
      content: [
        {
          type: 'text',
          text: `Error: ${errorMessage}`,
        },
      ],
      isError: true,
    };
  }
});

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  
  console.error('Document RAG MCP Server running on stdio');
}

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
