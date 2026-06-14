import tiktoken
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Count tokens in text"""
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except:
        # Fallback to rough estimation
        return len(text) // 4

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[Dict]:
    """
    Split text into overlapping chunks based on token count
    
    Args:
        text: Input text to chunk
        chunk_size: Target size of each chunk in tokens
        overlap: Number of tokens to overlap between chunks
        
    Returns:
        List of chunks with metadata
    """
    try:
        encoding = tiktoken.encoding_for_model("gpt-4")
        tokens = encoding.encode(text)
        
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(tokens):
            # Get chunk tokens
            end = start + chunk_size
            chunk_tokens = tokens[start:end]
            
            # Decode back to text
            chunk_text = encoding.decode(chunk_tokens)
            
            chunks.append({
                'chunk_index': chunk_index,
                'content': chunk_text,
                'token_count': len(chunk_tokens),
                'start_token': start,
                'end_token': end
            })
            
            # Move to next chunk with overlap
            start = end - overlap
            chunk_index += 1
            
            # Break if we've processed all tokens
            if end >= len(tokens):
                break
        
        logger.info(f"Split text into {len(chunks)} chunks (avg {sum(c['token_count'] for c in chunks) / len(chunks):.0f} tokens/chunk)")
        return chunks
        
    except Exception as e:
        logger.error(f"Error chunking text: {e}")
        raise
