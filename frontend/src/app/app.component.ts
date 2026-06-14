import { Component } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <div class="app-container">
      <nav class="navbar">
        <h1>📚 Document RAG System</h1>
        <div class="nav-links">
          <a routerLink="/chat" routerLinkActive="active">💬 Chat</a>
          <a routerLink="/upload" routerLinkActive="active">📤 Upload</a>
          <a routerLink="/documents" routerLinkActive="active">📄 Documents</a>
        </div>
      </nav>
      <main>
        <router-outlet></router-outlet>
      </main>
    </div>
  `,
  styles: [`
    .app-container {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }
    .navbar {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 1rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .navbar h1 {
      margin: 0;
      font-size: 1.5rem;
    }
    .nav-links {
      display: flex;
      gap: 0.5rem;
    }
    .nav-links a {
      color: white;
      text-decoration: none;
      padding: 0.6rem 1.2rem;
      border-radius: 6px;
      transition: all 0.3s;
      font-weight: 500;
    }
    .nav-links a:hover {
      background: rgba(255,255,255,0.15);
    }
    .nav-links a.active {
      background: rgba(255,255,255,0.25);
      box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    main {
      flex: 1;
      background: #f5f7fa;
    }
  `]
})
export class AppComponent {}
