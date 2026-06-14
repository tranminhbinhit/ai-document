import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { Category } from '../../models/models';

@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="upload-container">
      <div class="card">
        <h2>📤 Upload Document</h2>
        
        <div class="form-group">
          <label>Category *</label>
          <div class="category-input">
            <select 
              [(ngModel)]="selectedCategoryId" 
              (change)="onCategoryChange()"
              [disabled]="isUploading"
            >
              <option [ngValue]="null">Select a category...</option>
              <option *ngFor="let cat of categories" [ngValue]="cat.id">
                {{ cat.name }}
              </option>
              <option value="new">➕ Create New Category</option>
            </select>

            <div *ngIf="showNewCategoryInput" class="new-category-input">
              <input 
                type="text" 
                [(ngModel)]="newCategoryName"
                placeholder="Enter new category name"
                (keydown.enter)="createCategory()"
              />
              <button (click)="createCategory()" class="primary" [disabled]="!newCategoryName.trim()">
                ✓ Create
              </button>
              <button (click)="cancelNewCategory()" class="secondary">✕</button>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label>File *</label>
          <div 
            class="file-drop-zone"
            [class.drag-over]="isDragging"
            [class.disabled]="!selectedCategoryId || isUploading"
            (dragover)="onDragOver($event)"
            (dragleave)="onDragLeave($event)"
            (drop)="onDrop($event)"
            (click)="fileInput.click()"
          >
            <input 
              #fileInput
              type="file"
              (change)="onFileSelected($event)"
              [disabled]="!selectedCategoryId || isUploading"
              accept=".pdf,.docx,.doc,.xlsx,.xls,.pptx,.ppt,.html,.htm,.md,.markdown,.txt"
              style="display: none"
            />

            <div *ngIf="!selectedFile" class="drop-zone-content">
              <div class="icon">📁</div>
              <p><strong>Click to browse</strong> or drag and drop</p>
              <p class="hint">PDF, DOCX, XLSX, PPTX, HTML, MD, TXT</p>
            </div>

            <div *ngIf="selectedFile" class="selected-file">
              <div class="file-icon">📄</div>
              <div class="file-info">
                <div class="file-name">{{ selectedFile.name }}</div>
                <div class="file-size">{{ formatFileSize(selectedFile.size) }}</div>
              </div>
              <button 
                *ngIf="!isUploading" 
                (click)="removeFile($event)" 
                class="remove-btn"
              >
                ✕
              </button>
            </div>
          </div>
        </div>

        <div *ngIf="isUploading" class="progress-bar">
          <div class="progress-fill"></div>
          <span class="progress-text">Uploading and processing...</span>
        </div>

        <div *ngIf="uploadSuccess" class="alert success">
          ✓ Document uploaded successfully! Processing in background...
        </div>

        <div *ngIf="uploadError" class="alert error">
          ✕ {{ uploadError }}
        </div>

        <div class="actions">
          <button 
            (click)="upload()" 
            [disabled]="!selectedFile || !selectedCategoryId || isUploading"
            class="primary"
          >
            {{ isUploading ? '⏳ Uploading...' : '📤 Upload Document' }}
          </button>
        </div>
      </div>

      <div class="card info">
        <h3>ℹ️ Supported Formats</h3>
        <ul>
          <li><strong>PDF</strong> - Portable Document Format</li>
          <li><strong>DOCX/DOC</strong> - Microsoft Word</li>
          <li><strong>XLSX/XLS</strong> - Microsoft Excel</li>
          <li><strong>PPTX/PPT</strong> - Microsoft PowerPoint</li>
          <li><strong>HTML</strong> - Web pages</li>
          <li><strong>MD</strong> - Markdown</li>
          <li><strong>TXT</strong> - Plain text</li>
        </ul>
        <p class="note">Files will be processed asynchronously and indexed for RAG queries.</p>
      </div>
    </div>
  `,
  styles: [`
    .upload-container {
      max-width: 800px;
      margin: 0 auto;
      padding: 40px 20px;
    }

    .card h2 {
      margin-top: 0;
    }

    .form-group {
      margin-bottom: 24px;
    }

    .form-group label {
      display: block;
      margin-bottom: 8px;
      font-weight: 600;
      color: #333;
    }

    .category-input select {
      width: 100%;
    }

    .new-category-input {
      display: flex;
      gap: 8px;
      margin-top: 12px;
    }

    .new-category-input input {
      flex: 1;
    }

    .file-drop-zone {
      border: 2px dashed #ddd;
      border-radius: 8px;
      padding: 40px;
      text-align: center;
      cursor: pointer;
      transition: all 0.3s;
      background: #fafafa;
    }

    .file-drop-zone:hover:not(.disabled) {
      border-color: #667eea;
      background: #f0f0ff;
    }

    .file-drop-zone.drag-over {
      border-color: #667eea;
      background: #e8ebff;
    }

    .file-drop-zone.disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    .drop-zone-content .icon {
      font-size: 48px;
      margin-bottom: 16px;
    }

    .drop-zone-content p {
      margin: 8px 0;
      color: #666;
    }

    .drop-zone-content .hint {
      font-size: 13px;
      color: #999;
    }

    .selected-file {
      display: flex;
      align-items: center;
      gap: 16px;
      padding: 16px;
      background: white;
      border-radius: 8px;
    }

    .file-icon {
      font-size: 32px;
    }

    .file-info {
      flex: 1;
      text-align: left;
    }

    .file-name {
      font-weight: 600;
      color: #333;
      margin-bottom: 4px;
    }

    .file-size {
      font-size: 13px;
      color: #999;
    }

    .remove-btn {
      background: #dc3545;
      color: white;
      border: none;
      border-radius: 50%;
      width: 30px;
      height: 30px;
      cursor: pointer;
      font-size: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .remove-btn:hover {
      background: #c82333;
    }

    .progress-bar {
      position: relative;
      height: 40px;
      background: #f0f0f0;
      border-radius: 8px;
      overflow: hidden;
      margin-bottom: 16px;
    }

    .progress-fill {
      height: 100%;
      background: linear-gradient(90deg, #667eea, #764ba2);
      animation: progress 2s infinite;
    }

    .progress-text {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      color: #333;
      font-weight: 600;
    }

    @keyframes progress {
      0% { width: 0%; }
      50% { width: 100%; }
      100% { width: 0%; }
    }

    .alert {
      padding: 12px 16px;
      border-radius: 8px;
      margin-bottom: 16px;
    }

    .alert.success {
      background: #d4edda;
      color: #155724;
      border: 1px solid #c3e6cb;
    }

    .alert.error {
      background: #f8d7da;
      color: #721c24;
      border: 1px solid #f5c6cb;
    }

    .actions {
      display: flex;
      justify-content: flex-end;
    }

    .info {
      margin-top: 24px;
    }

    .info h3 {
      margin-top: 0;
    }

    .info ul {
      margin: 16px 0;
      padding-left: 20px;
    }

    .info li {
      margin-bottom: 8px;
    }

    .note {
      font-size: 13px;
      color: #666;
      font-style: italic;
    }
  `]
})
export class UploadComponent implements OnInit {
  categories: Category[] = [];
  selectedCategoryId: number | null = null;
  selectedFile: File | null = null;
  isDragging = false;
  isUploading = false;
  uploadSuccess = false;
  uploadError: string | null = null;
  showNewCategoryInput = false;
  newCategoryName = '';

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadCategories();
  }

  loadCategories() {
    this.apiService.getCategories().subscribe(cats => {
      this.categories = cats;
    });
  }

  onCategoryChange() {
    if ((this.selectedCategoryId as any) === 'new') {
      this.showNewCategoryInput = true;
      this.selectedCategoryId = null;
    } else {
      this.showNewCategoryInput = false;
    }
  }

  createCategory() {
    if (!this.newCategoryName.trim()) return;

    this.apiService.createCategory(this.newCategoryName).subscribe({
      next: (category) => {
        this.categories.push(category);
        this.selectedCategoryId = category.id;
        this.showNewCategoryInput = false;
        this.newCategoryName = '';
      },
      error: (error) => {
        this.uploadError = 'Failed to create category: ' + (error.error?.message || error.message);
      }
    });
  }

  cancelNewCategory() {
    this.showNewCategoryInput = false;
    this.newCategoryName = '';
    this.selectedCategoryId = null;
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
      this.uploadSuccess = false;
      this.uploadError = null;
    }
  }

  onDragOver(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    if (!this.selectedCategoryId || this.isUploading) return;
    this.isDragging = true;
  }

  onDragLeave(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = false;
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = false;

    if (!this.selectedCategoryId || this.isUploading) return;

    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      this.selectedFile = files[0];
      this.uploadSuccess = false;
      this.uploadError = null;
    }
  }

  removeFile(event: Event) {
    event.stopPropagation();
    this.selectedFile = null;
    this.uploadSuccess = false;
    this.uploadError = null;
  }

  upload() {
    if (!this.selectedFile || !this.selectedCategoryId) return;

    this.isUploading = true;
    this.uploadSuccess = false;
    this.uploadError = null;

    this.apiService.uploadDocument(this.selectedFile, this.selectedCategoryId).subscribe({
      next: () => {
        this.uploadSuccess = true;
        this.isUploading = false;
        this.selectedFile = null;
        setTimeout(() => this.uploadSuccess = false, 5000);
      },
      error: (error) => {
        this.uploadError = error.error?.message || 'Upload failed';
        this.isUploading = false;
      }
    });
  }

  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  }
}
