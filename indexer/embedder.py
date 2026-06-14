import os
import logging
from typing import List
from openai import OpenAI

logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'text-embedding-3-small')

def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for a list of texts"""
    try:
        logger.info(f"Generating embeddings for {len(texts)} texts")
        
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=texts
        )
        
        embeddings = [item.embedding for item in response.data]
        logger.info(f"Generated {len(embeddings)} embeddings")
        
        return embeddings
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        raise
