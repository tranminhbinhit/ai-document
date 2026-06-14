export interface Category {
  id: number;
  name: string;
  description?: string;
  createdAt: Date;
}

export interface Document {
  id: number;
  title: string;
  originalFileName: string;
  fileType: string;
  fileSize: number;
  categoryId: number;
  categoryName: string;
  status: 'Pending' | 'Processing' | 'Completed' | 'Failed';
  uploadedAt: Date;
  processedAt?: Date;
  errorMessage?: string;
}

export interface DocumentList {
  documents: Document[];
  totalCount: number;
  page: number;
  pageSize: number;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  sources?: DocumentSource[];
  confidenceScore?: number;
  createdAt: Date;
}

export interface DocumentSource {
  documentId: number;
  documentTitle: string;
  chunkContent: string;
  score: number;
}

export interface ChatQueryRequest {
  sessionId?: string;
  message: string;
  categoryId?: number;
}

export interface ChatQueryResponse {
  sessionId: string;
  message: string;
  sources: DocumentSource[];
  confidenceScore: number;
  timestamp: Date;
}

export interface ChatSession {
  sessionId: string;
  createdAt: Date;
  messages: ChatMessage[];
}
