import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Category, Document, DocumentList, ChatQueryRequest, ChatQueryResponse, ChatSession } from '../models/models';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) {}

  // Categories
  getCategories(): Observable<Category[]> {
    return this.http.get<Category[]>(`${this.apiUrl}/categories`);
  }

  createCategory(name: string, description?: string): Observable<Category> {
    return this.http.post<Category>(`${this.apiUrl}/categories`, { name, description });
  }

  deleteCategory(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/categories/${id}`);
  }

  // Documents
  uploadDocument(file: File, categoryId: number): Observable<Document> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('categoryId', categoryId.toString());
    return this.http.post<Document>(`${this.apiUrl}/documents/upload`, formData);
  }

  getDocuments(page: number = 1, pageSize: number = 20, search?: string, categoryId?: number): Observable<DocumentList> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('pageSize', pageSize.toString());
    
    if (search) params = params.set('search', search);
    if (categoryId) params = params.set('categoryId', categoryId.toString());

    return this.http.get<DocumentList>(`${this.apiUrl}/documents`, { params });
  }

  getDocument(id: number): Observable<Document> {
    return this.http.get<Document>(`${this.apiUrl}/documents/${id}`);
  }

  updateDocument(id: number, title: string, categoryId: number): Observable<Document> {
    return this.http.put<Document>(`${this.apiUrl}/documents/${id}`, { title, categoryId });
  }

  deleteDocument(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/documents/${id}`);
  }

  // Chat
  chatQuery(request: ChatQueryRequest): Observable<ChatQueryResponse> {
    return this.http.post<ChatQueryResponse>(`${this.apiUrl}/chat/query`, request);
  }

  createChatSession(): Observable<ChatSession> {
    return this.http.post<ChatSession>(`${this.apiUrl}/chat/sessions`, {});
  }

  getChatSession(sessionId: string): Observable<ChatSession> {
    return this.http.get<ChatSession>(`${this.apiUrl}/chat/sessions/${sessionId}`);
  }

  exportChat(sessionId: string, format: 'json' | 'csv'): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/chat/sessions/${sessionId}/export?format=${format}`, {
      responseType: 'blob'
    });
  }
}
