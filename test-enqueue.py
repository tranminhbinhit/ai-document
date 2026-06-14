import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

job = {
    "document_id": 5,
    "file_path": "/app/storage/919d423c-cab6-427b-af47-079fb87dc391.docx",
    "file_type": "docx"
}

r.rpush('document_processing', json.dumps(job))
print(f"Enqueued document 5 for processing")
print(f"Queue length: {r.llen('document_processing')}")
