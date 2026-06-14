import os
import logging
from typing import List, Dict
from .pdf_processor import extract_text_from_pdf
from .docx_processor import extract_text_from_docx
from .excel_processor import extract_text_from_excel
from .pptx_processor import extract_text_from_pptx
from .html_processor import extract_text_from_html
from .markdown_processor import extract_text_from_markdown
from .txt_processor import extract_text_from_txt
from chunker import chunk_text
from database import get_document_info

logger = logging.getLogger(__name__)

PROCESSORS = {
    'pdf': extract_text_from_pdf,
    'docx': extract_text_from_docx,
    'doc': extract_text_from_docx,
    'xlsx': extract_text_from_excel,
    'xls': extract_text_from_excel,
    'pptx': extract_text_from_pptx,
    'ppt': extract_text_from_pptx,
    'html': extract_text_from_html,
    'htm': extract_text_from_html,
    'md': extract_text_from_markdown,
    'markdown': extract_text_from_markdown,
    'txt': extract_text_from_txt,
}

def process_document(file_path: str, file_type: str, chunk_size: int, overlap: int) -> List[Dict]:
    """
    Process a document: extract text and chunk it
    
    Returns:
        List of chunks with metadata
    """
    try:
        # Get processor for file type
        processor = PROCESSORS.get(file_type.lower())
        if not processor:
            raise Exception(f"Unsupported file type: {file_type}")
        
        logger.info(f"Processing {file_type} file: {file_path}")
        
        # Extract text
        text = processor(file_path)
        
        if not text or len(text.strip()) == 0:
            raise Exception("No text extracted from document")
        
        logger.info(f"Extracted {len(text)} characters")
        
        # Chunk text
        chunks = chunk_text(text, chunk_size, overlap)
        
        # Get document info from database
        # Extract document_id from file_path if possible
        doc_id = extract_document_id(file_path)
        if doc_id:
            doc_info = get_document_info(doc_id)
            if doc_info:
                for chunk in chunks:
                    chunk['document_title'] = doc_info['Title']
                    chunk['category_id'] = doc_info['CategoryId']
                    chunk['category_name'] = doc_info['CategoryName']
        
        return chunks
        
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        raise

def extract_document_id(file_path: str) -> int:
    """Extract document ID from file path (if stored in filename)"""
    # This is a simple implementation - adjust based on your naming convention
    try:
        # Assuming the worker receives document_id separately
        return None
    except:
        return None
