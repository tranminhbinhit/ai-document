import os
import pyodbc
import logging
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

def get_connection():
    """Get database connection"""
    conn_str = os.getenv('SQL_CONNECTION_STRING', '')
    
    # Parse connection string
    parts = dict(item.split('=', 1) for item in conn_str.split(';') if '=' in item)
    
    server = parts.get('Server', 'localhost').split(',')[0]
    database = parts.get('Database', 'DocumentRAG')
    user = parts.get('User Id', 'sa')
    password = parts.get('Password', '')
    
    # Build pyodbc connection string
    pyodbc_conn_str = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={user};'
        f'PWD={password};'
        f'TrustServerCertificate=yes;'
    )
    
    return pyodbc.connect(pyodbc_conn_str)

def get_document_info(document_id: int) -> Optional[Dict]:
    """Get document information from database"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT d.Id, d.Title, d.CategoryId, c.Name as CategoryName
            FROM Documents d
            JOIN Categories c ON d.CategoryId = c.Id
            WHERE d.Id = ?
        """, (document_id,))
        
        row = cursor.fetchone()
        if row:
            result = {
                'Id': row[0],
                'Title': row[1],
                'CategoryId': row[2],
                'CategoryName': row[3]
            }
        else:
            result = None
        conn.close()
        return result
    except Exception as e:
        logger.error(f"Error getting document info: {e}")
        return None

def update_document_status(document_id: int, status: int, error_message: Optional[str]):
    """Update document processing status"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if status == 2:  # Completed
            cursor.execute("""
                UPDATE Documents 
                SET Status = ?, ProcessedAt = ?, ErrorMessage = NULL
                WHERE Id = ?
            """, (status, datetime.utcnow(), document_id))
        else:
            cursor.execute("""
                UPDATE Documents 
                SET Status = ?, ErrorMessage = ?
                WHERE Id = ?
            """, (status, error_message, document_id))
        
        conn.commit()
        conn.close()
        logger.info(f"Document {document_id} status updated to {status}")
    except Exception as e:
        logger.error(f"Error updating document status: {e}")
        raise

def save_chunks(document_id: int, chunks: List[Dict]):
    """Save document chunks to database"""
    try:
        # Get document info first
        doc_info = get_document_info(document_id)
        if not doc_info:
            raise Exception("Document not found")
        
        conn = get_connection()
        cursor = conn.cursor()
        
        for chunk in chunks:
            cursor.execute("""
                INSERT INTO DocumentChunks 
                (DocumentId, ChunkIndex, Content, TokenCount, QdrantPointId, CreatedAt)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                document_id,
                chunk['chunk_index'],
                chunk['content'],
                chunk['token_count'],
                chunk['qdrant_point_id'],
                datetime.utcnow()
            ))
        
        conn.commit()
        conn.close()
        logger.info(f"Saved {len(chunks)} chunks for document {document_id}")
    except Exception as e:
        logger.error(f"Error saving chunks: {e}")
        raise
