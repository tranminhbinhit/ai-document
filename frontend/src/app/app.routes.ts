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
