import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { ChatMessage, Category } from '../../models/models';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="chat-container">
      <div class="chat-header">
        <h2>💬 Chat with Documents</h2>
        <div class="controls">
          <select [(ngModel)]="selectedCategoryId" class="category-filter">
            <option [ngValue]="null">All Categories</option>
            <option *ngFor="let cat of categories" [ngValue]="cat.id">{{ cat.name }}</option>
          </select>
          <button (click)="exportChat()" [disabled]="messages.length === 0" class="secondary">
            📥 Export
          </button>
          <button (click)="newSession()" class="secondary">🔄 New Chat</button>
        </div>
      </div>

      <div class="messages-container" #messagesContainer>
        <div *ngIf="messages.length === 0" class="empty-state">
          <p>👋 Start by asking a question about your documents!</p>
        </div>

        <div *ngFor="let msg of messages" [class]="'message ' + msg.role">
          <div class="message-content">
            <div class="message-text">{{ msg.content }}</div>
            
            <div *ngIf="msg.sources && msg.sources.length > 0" class="sources">
              <div class="sources-header">
                📚 Sources ({{ (msg.confidenceScore! * 100).toFixed(0) }}% confidence)
              </div>
              <div *ngFor="let source of msg.sources" class="source-item">
                <span class="source-title">{{ source.documentTitle }}</span>
                <span class="source-score">{{ (source.score * 100).toFixed(0) }}%</span>
              </div>
            </div>
          </div>
        </div>

        <div *ngIf="isLoading" class="message assistant">
          <div class="message-content loading">
            <div class="typing-indicator">
              <span></span><span></span><span></span>
            </div>
          </div>
        </div>
      </div>

      <div class="input-container">
        <textarea 
          [(ngModel)]="userInput"
          (keydown.enter)="onEnterPress($event)"
          placeholder="Ask a question about your documents..."
          [disabled]="isLoading"
          rows="3"
        ></textarea>
        <button 
          (click)="sendMessage()" 
          [disabled]="!userInput.trim() || isLoading"
          class="primary"
        >
          {{ isLoading ? '⏳ Thinking...' : '📤 Send' }}
        </button>
      </div>
    </div>
  `,
  styles: [`
    .chat-container {
      display: flex;
      flex-direction: column;
      height: calc(100vh - 80px);
      max-width: 1000px;
      margin: 0 auto;
      padding: 20px;
    }

    .chat-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }

    .chat-header h2 {
      margin: 0;
    }

    .controls {
      display: flex;
      gap: 10px;
    }

    .category-filter {
      min-width: 150px;
    }

    .messages-container {
      flex: 1;
      overflow-y: auto;
      background: white;
      border-radius: 8px;
      padding: 20px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      margin-bottom: 20px;
    }

    .empty-state {
      text-align: center;
      padding: 60px 20px;
      color: #999;
      font-size: 18px;
    }

    .message {
      margin-bottom: 20px;
      display: flex;
    }

    .message.user {
      justify-content: flex-end;
    }

    .message.assistant {
      justify-content: flex-start;
    }

    .message-content {
      max-width: 80%;
      padding: 12px 16px;
      border-radius: 12px;
    }

    .message.user .message-content {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
    }

    .message.assistant .message-content {
      background: #f0f0f0;
      color: #333;
    }

    .message-text {
      white-space: pre-wrap;
      line-height: 1.5;
    }

    .sources {
      margin-top: 12px;
      padding-top: 12px;
      border-top: 1px solid rgba(0,0,0,0.1);
    }

    .sources-header {
      font-weight: 600;
      margin-bottom: 8px;
      font-size: 13px;
    }

    .source-item {
      display: flex;
      justify-content: space-between;
      padding: 6px 8px;
      background: white;
      border-radius: 4px;
      margin-bottom: 4px;
      font-size: 13px;
    }

    .source-title {
      font-weight: 500;
    }

    .source-score {
      color: #667eea;
      font-weight: 600;
    }

    .loading {
      background: #f0f0f0 !important;
    }

    .typing-indicator {
      display: flex;
      gap: 4px;
    }

    .typing-indicator span {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #999;
      animation: typing 1.4s infinite;
    }

    .typing-indicator span:nth-child(2) {
      animation-delay: 0.2s;
    }

    .typing-indicator span:nth-child(3) {
      animation-delay: 0.4s;
    }

    @keyframes typing {
      0%, 60%, 100% { transform: translateY(0); }
      30% { transform: translateY(-10px); }
    }

    .input-container {
      display: flex;
      gap: 10px;
      background: white;
      padding: 16px;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    .input-container textarea {
      flex: 1;
      resize: none;
      font-family: inherit;
    }

    .input-container button {
      align-self: flex-end;
    }
  `]
})
export class ChatComponent implements OnInit {
  messages: ChatMessage[] = [];
  userInput = '';
  isLoading = false;
  sessionId: string | null = null;
  categories: Category[] = [];
  selectedCategoryId: number | null = null;

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadCategories();
    this.createSession();
  }

  loadCategories() {
    this.apiService.getCategories().subscribe(cats => {
      this.categories = cats;
    });
  }

  createSession() {
    this.apiService.createChatSession().subscribe(session => {
      this.sessionId = session.sessionId;
    });
  }

  sendMessage() {
    if (!this.userInput.trim() || this.isLoading) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: this.userInput,
      createdAt: new Date()
    };

    this.messages.push(userMessage);
    const query = this.userInput;
    this.userInput = '';
    this.isLoading = true;

    this.apiService.chatQuery({
      sessionId: this.sessionId || undefined,
      message: query,
      categoryId: this.selectedCategoryId || undefined
    }).subscribe({
      next: (response) => {
        const assistantMessage: ChatMessage = {
          role: 'assistant',
          content: response.message,
          sources: response.sources,
          confidenceScore: response.confidenceScore,
          createdAt: new Date(response.timestamp)
        };
        this.messages.push(assistantMessage);
        this.sessionId = response.sessionId;
        this.isLoading = false;
      },
      error: (error) => {
        const errorMessage: ChatMessage = {
          role: 'assistant',
          content: '❌ Error: ' + (error.error?.message || 'Failed to get response'),
          createdAt: new Date()
        };
        this.messages.push(errorMessage);
        this.isLoading = false;
      }
    });
  }

  onEnterPress(event: Event) {
    const keyboardEvent = event as KeyboardEvent;
    if (keyboardEvent.key === 'Enter' && !keyboardEvent.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }

  newSession() {
    this.messages = [];
    this.createSession();
  }

  exportChat() {
    if (!this.sessionId) return;

    this.apiService.exportChat(this.sessionId, 'json').subscribe(blob => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `chat-${this.sessionId}.json`;
      a.click();
      window.URL.revokeObjectURL(url);
    });
  }
}
