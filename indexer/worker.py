import os
import json
import time
import logging
import redis
import uuid
from typing import Optional
from processors.document_processor import process_document
from embedder import generate_embeddings
from database import update_document_status, save_chunks
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Environment variables
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
REDIS_QUEUE = os.getenv('REDIS_QUEUE', 'document_processing')
QDRANT_URL = os.getenv('QDRANT_URL', 'http://localhost:6333')
QDRANT_COLLECTION = os.getenv('QDRANT_COLLECTION', 'documents')
CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', '500'))
CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', '50'))

def initialize_qdrant():
    """Initialize Qdrant collection if not exists"""
    try:
        client = QdrantClient(url=QDRANT_URL)
        
        collections = client.get_collections().collections
        collection_names = [col.name for col in collections]
        
        if QDRANT_COLLECTION not in collection_names:
            logger.info(f"Creating Qdrant collection: {QDRANT_COLLECTION}")
            client.create_collection(
                collection_name=QDRANT_COLLECTION,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
            )
            logger.info("Collection created successfully")
        else:
            logger.info(f"Collection {QDRANT_COLLECTION} already exists")
            
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Qdrant: {e}")
        raise

def process_job(job_data: dict, qdrant_client: QdrantClient) -> bool:
    """Process a document processing job"""
    document_id = job_data.get('document_id')
    file_path = job_data.get('file_path')
    file_type = job_data.get('file_type')
    
    logger.info(f"Processing document {document_id}: {file_path}")
    
    # Status enum: 0=Pending, 1=Processing, 2=Completed, 3=Failed
    try:
        # Update status to Processing
        update_document_status(document_id, 1, None)
        
        # Step 1: Extract text and chunk
        logger.info(f"Extracting text from {file_type} file")
        chunks = process_document(file_path, file_type, CHUNK_SIZE, CHUNK_OVERLAP)
        
        if not chunks:
            raise Exception("No text extracted from document")
        
        logger.info(f"Extracted {len(chunks)} chunks")
        
        # Step 2: Generate embeddings
        logger.info("Generating embeddings")
        embeddings = generate_embeddings([chunk['content'] for chunk in chunks])
        
        # Step 3: Store in Qdrant
        logger.info("Storing vectors in Qdrant")
        points = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            # Generate UUID for point ID (Qdrant requires UUID or unsigned int)
            point_id = str(uuid.uuid4())
            chunk['qdrant_point_id'] = point_id
            
            points.append(PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    'document_id': document_id,
                    'chunk_index': i,
                    'content': chunk['content'],
                    'token_count': chunk['token_count'],
                    'document_title': chunk.get('document_title', ''),
                    'category_id': chunk.get('category_id', 0),
                    'category_name': chunk.get('category_name', '')
                }
            ))
        
        qdrant_client.upsert(
            collection_name=QDRANT_COLLECTION,
            points=points
        )
        
        # Step 4: Save chunk metadata to SQL
        logger.info("Saving chunk metadata to database")
        save_chunks(document_id, chunks)
        
        # Step 5: Update document status to Completed
        update_document_status(document_id, 2, None)
        
        logger.info(f"Document {document_id} processed successfully")
        return True
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error processing document {document_id}: {error_msg}")
        update_document_status(document_id, 3, error_msg)
        return False

def main():
    """Main worker loop"""
    logger.info("Starting document processing worker")
    
    # Initialize connections
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    qdrant_client = initialize_qdrant()
    
    logger.info(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
    logger.info(f"Connected to Qdrant at {QDRANT_URL}")
    logger.info(f"Listening on queue: {REDIS_QUEUE}")
    
    # Worker loop
    while True:
        try:
            # Blocking pop from queue (timeout 1 second)
            result = redis_client.blpop(REDIS_QUEUE, timeout=1)
            
            if result:
                queue_name, job_json = result
                job_data = json.loads(job_json)
                
                logger.info(f"Received job: {job_data}")
                process_job(job_data, qdrant_client)
            else:
                # No job, wait a bit
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Worker stopped by user")
            break
        except Exception as e:
            logger.error(f"Unexpected error in worker loop: {e}")
            time.sleep(5)

if __name__ == '__main__':
    main()
