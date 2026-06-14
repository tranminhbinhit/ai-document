import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { Document, Category } from '../../models/models';

@Component({
  selector: 'app-documents',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="documents-container">
      <div class="header">
        <h2>📄 Documents</h2>
        <button (click)="refresh()" class="secondary">🔄 Refresh</button>
      </div>

      <div class="filters">
        <input 
          type="text" 
          [(ngModel)]="searchTerm"
          (ngModelChange)="onSearchChange()"
          placeholder="🔍 Search by title..."
          class="search-input"
        />
        <select [(ngModel)]="filterCategoryId" (change)="loadDocuments()" class="category-filter">
          <option [ngValue]="null">All Categories</option>
          <option *ngFor="let cat of categories" [ngValue]="cat.id">{{ cat.name }}</option>
        </select>
      </div>

      <div *ngIf="isLoading" class="loading">
        <div class="spinner"></div>
        <p>Loading documents...</p>
      </div>

      <div *ngIf="!isLoading && documents.length === 0" class="empty-state">
        <p>📭 No documents found</p>
        <p class="hint">Upload some documents to get started!</p>
      </div>

      <div *ngIf="!isLoading && documents.length > 0" class="documents-grid">
        <div *ngFor="let doc of documents" class="document-card">
          <div class="doc-header">
            <div class="doc-icon">{{ getFileIcon(doc.fileType) }}</div>
            <div class="doc-info">
              <h3 class="doc-title">{{ doc.title }}</h3>
              <p class="doc-filename">{{ doc.originalFileName }}</p>
            </div>
            <div class="doc-actions">
              <button (click)="editDocument(doc)" class="icon-btn" title="Edit">✏️</button>
              <button (click)="deleteDocument(doc)" class="icon-btn delete" title="Delete">🗑️</button>
            </div>
          </div>

          <div class="doc-details">
            <div class="detail">
              <span class="label">Category:</span>
              <span class="value">{{ doc.categoryName }}</span>
            </div>
            <div class="detail">
              <span class="label">Size:</span>
              <span class="value">{{ formatFileSize(doc.fileSize) }}</span>
            </div>
            <div class="detail">
              <span class="label">Status:</span>
              <span [class]="'badge ' + doc.status.toLowerCase()">{{ doc.status }}</span>
            </div>
            <div class="detail">
              <span class="label">Uploaded:</span>
              <span class="value">{{ formatDate(doc.uploadedAt) }}</span>
            </div>
          </div>

          <div *ngIf="doc.errorMessage" class="error-message">
            ⚠️ {{ doc.errorMessage }}
          </div>
        </div>
      </div>

      <div *ngIf="totalPages > 1" class="pagination">
        <button 
          (click)="previousPage()" 
          [disabled]="currentPage === 1"
          class="secondary"
        >
          ← Previous
        </button>
        <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
        <button 
          (click)="nextPage()" 
          [disabled]="currentPage === totalPages"
          class="secondary"
        >
          Next →
        </button>
      </div>

      <!-- Edit Modal -->
      <div *ngIf="editingDocument" class="modal-overlay" (click)="cancelEdit()">
        <div class="modal" (click)="$event.stopPropagation()">
          <h3>Edit Document</h3>
          <div class="form-group">
            <label>Title</label>
            <input type="text" [(ngModel)]="editTitle" />
          </div>
          <div class="form-group">
            <label>Category</label>
            <select [(ngModel)]="editCategoryId">
              <option *ngFor="let cat of categories" [ngValue]="cat.id">{{ cat.name }}</option>
            </select>
          </div>
          <div class="modal-actions">
            <button (click)="saveEdit()" class="primary">💾 Save</button>
            <button (click)="cancelEdit()" class="secondary">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .documents-container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 40px 20px;
    }

    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
    }

    .header h2 {
      margin: 0;
    }

    .filters {
      display: flex;
      gap: 12px;
      margin-bottom: 24px;
    }

    .search-input {
      flex: 1;
    }

    .category-filter {
      min-width: 200px;
    }

    .loading {
      text-align: center;
      padding: 60px 20px;
    }

    .spinner {
      width: 40px;
      height: 40px;
      border: 4px solid #f3f3f3;
      border-top: 4px solid #667eea;
      border-radius: 50%;
      animation: spin 1s linear infinite;
      margin: 0 auto 20px;
    }

    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }

    .empty-state {
      text-align: center;
      padding: 60px 20px;
      color: #999;
    }

    .empty-state .hint {
      font-size: 14px;
      margin-top: 8px;
    }

    .documents-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
      gap: 20px;
      margin-bottom: 24px;
    }

    .document-card {
      background: white;
      border-radius: 8px;
      padding: 20px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      transition: transform 0.2s, box-shadow 0.2s;
    }

    .document-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }

    .doc-header {
      display: flex;
      gap: 12px;
      margin-bottom: 16px;
      align-items: flex-start;
    }

    .doc-icon {
      font-size: 32px;
    }

    .doc-info {
      flex: 1;
      min-width: 0;
    }

    .doc-title {
      margin: 0 0 4px 0;
      font-size: 16px;
      font-weight: 600;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .doc-filename {
      margin: 0;
      font-size: 13px;
      color: #999;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .doc-actions {
      display: flex;
      gap: 4px;
    }

    .icon-btn {
      background: none;
      border: none;
      cursor: pointer;
      font-size: 18px;
      padding: 4px 8px;
      border-radius: 4px;
      transition: background 0.2s;
    }

    .icon-btn:hover {
      background: #f0f0f0;
    }

    .icon-btn.delete:hover {
      background: #fee;
    }

    .doc-details {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }

    .detail {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .detail .label {
      font-size: 12px;
      color: #999;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .detail .value {
      font-size: 14px;
      color: #333;
      font-weight: 500;
    }

    .badge {
      display: inline-block;
      padding: 4px 8px;
      border-radius: 12px;
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
    }

    .badge.pending {
      background: #fff3cd;
      color: #856404;
    }

    .badge.processing {
      background: #cce5ff;
      color: #004085;
    }

    .badge.completed {
      background: #d4edda;
      color: #155724;
    }

    .badge.failed {
      background: #f8d7da;
      color: #721c24;
    }

    .error-message {
      margin-top: 12px;
      padding: 8px 12px;
      background: #fff3cd;
      border-left: 3px solid #ffc107;
      font-size: 13px;
      border-radius: 4px;
    }

    .pagination {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 16px;
    }

    .page-info {
      font-weight: 600;
      color: #333;
    }

    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0,0,0,0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
    }

    .modal {
      background: white;
      padding: 24px;
      border-radius: 8px;
      width: 90%;
      max-width: 500px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }

    .modal h3 {
      margin-top: 0;
    }

    .form-group {
      margin-bottom: 16px;
    }

    .form-group label {
      display: block;
      margin-bottom: 8px;
      font-weight: 600;
    }

    .form-group input,
    .form-group select {
      width: 100%;
    }

    .modal-actions {
      display: flex;
      gap: 12px;
      justify-content: flex-end;
    }
  `]
})
export class DocumentsComponent implements OnInit {
  documents: Document[] = [];
  categories: Category[] = [];
  isLoading = false;
  searchTerm = '';
  filterCategoryId: number | null = null;
  currentPage = 1;
  pageSize = 20;
  totalCount = 0;
  totalPages = 0;
  searchTimeout: any;

  editingDocument: Document | null = null;
  editTitle = '';
  editCategoryId: number | null = null;

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadCategories();
    this.loadDocuments();
  }

  loadCategories() {
    this.apiService.getCategories().subscribe(cats => {
      this.categories = cats;
    });
  }

  loadDocuments() {
    this.isLoading = true;
    this.apiService.getDocuments(
      this.currentPage,
      this.pageSize,
      this.searchTerm || undefined,
      this.filterCategoryId || undefined
    ).subscribe({
      next: (result) => {
        this.documents = result.documents;
        this.totalCount = result.totalCount;
        this.totalPages = Math.ceil(this.totalCount / this.pageSize);
        this.isLoading = false;
      },
      error: () => {
        this.isLoading = false;
      }
    });
  }

  onSearchChange() {
    clearTimeout(this.searchTimeout);
    this.searchTimeout = setTimeout(() => {
      this.currentPage = 1;
      this.loadDocuments();
    }, 500);
  }

  previousPage() {
    if (this.currentPage > 1) {
      this.currentPage--;
      this.loadDocuments();
    }
  }

  nextPage() {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
      this.loadDocuments();
    }
  }

  refresh() {
    this.loadDocuments();
  }

  editDocument(doc: Document) {
    this.editingDocument = doc;
    this.editTitle = doc.title;
    this.editCategoryId = doc.categoryId;
  }

  saveEdit() {
    if (!this.editingDocument || !this.editCategoryId) return;

    this.apiService.updateDocument(
      this.editingDocument.id,
      this.editTitle,
      this.editCategoryId
    ).subscribe({
      next: () => {
        this.loadDocuments();
        this.cancelEdit();
      }
    });
  }

  cancelEdit() {
    this.editingDocument = null;
    this.editTitle = '';
    this.editCategoryId = null;
  }

  deleteDocument(doc: Document) {
    if (!confirm(`Delete "${doc.title}"?`)) return;

    this.apiService.deleteDocument(doc.id).subscribe({
      next: () => {
        this.loadDocuments();
      }
    });
  }

  getFileIcon(fileType: string): string {
    const icons: Record<string, string> = {
      pdf: '📕',
      docx: '📘',
      doc: '📘',
      xlsx: '📗',
      xls: '📗',
      pptx: '📙',
      ppt: '📙',
      html: '🌐',
      htm: '🌐',
      md: '📝',
      markdown: '📝',
      txt: '📄'
    };
    return icons[fileType.toLowerCase()] || '📄';
  }

  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  }

  formatDate(date: Date): string {
    return new Date(date).toLocaleDateString() + ' ' + new Date(date).toLocaleTimeString();
  }
}
