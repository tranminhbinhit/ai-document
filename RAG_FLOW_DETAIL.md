# Chi tiết luồng RAG - Ví dụ thực tế

## Câu hỏi người dùng
**"Cung cấp cho tôi tài liệu về các thay đổi trong order service"**

---

## Luồng xử lý chi tiết

### Step 1: User gửi câu hỏi từ Frontend

**Request từ Angular → .NET API**
```http
POST /api/chat/query
Content-Type: application/json

{
  "sessionId": "123e4567-e89b-12d3-a456-426614174000",
  "message": "Cung cấp cho tôi tài liệu về các thay đổi trong order service",
  "categoryId": null  // optional filter
}
```

---

### Step 2: .NET API nhận request → RAGService xử lý

**RAGService.QueryAsync() thực hiện:**

#### 2.1. Tạo embedding cho câu hỏi

**Call OpenAI Embeddings API:**
```csharp
var embeddingRequest = new {
    model = "text-embedding-3-small",
    input = "Cung cấp cho tôi tài liệu về các thay đổi trong order service"
};

// POST https://api.openai.com/v1/embeddings
```

**OpenAI Response:**
```json
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "embedding": [0.0023, -0.0091, 0.0045, ... ], // 1536 dimensions
      "index": 0
    }
  ],
  "model": "text-embedding-3-small",
  "usage": { "prompt_tokens": 15, "total_tokens": 15 }
}
```

#### 2.2. Search Qdrant với embedding vector

**Call Qdrant API:**
```csharp
var searchRequest = new {
    vector = embeddingVector, // [0.0023, -0.0091, ...]
    limit = 3,                // Retrieve top 3 chunks
    score_threshold = 0.7,    // Minimum similarity
    filter = categoryId != null ? new { 
        must = [{ key = "category_id", match = { value = categoryId } }] 
    } : null
};

// POST http://qdrant:6333/collections/documents/points/search
```

**Qdrant Response:**
```json
{
  "result": [
    {
      "id": "chunk-doc-45-0",
      "version": 1,
      "score": 0.92,
      "payload": {
        "document_id": 45,
        "document_title": "Order Service API Changes v2.3.md",
        "chunk_index": 0,
        "content": "# Order Service Changes\n\n## Version 2.3 Updates\n\n- Added new endpoint POST /api/orders/bulk for bulk order creation\n- Modified order status enum to include 'PENDING_PAYMENT' state\n- Updated order validation to require email field...",
        "category_id": 5,
        "category_name": "Technical Documentation"
      }
    },
    {
      "id": "chunk-doc-67-2",
      "version": 1,
      "score": 0.88,
      "payload": {
        "document_id": 67,
        "document_title": "Migration Guide - Order Service.pdf",
        "chunk_index": 2,
        "content": "Breaking changes in Order Service:\n1. The old /orders endpoint is deprecated\n2. New authentication required for all order operations\n3. Payment integration changed from Stripe to PayPal...",
        "category_id": 5,
        "category_name": "Technical Documentation"
      }
    },
    {
      "id": "chunk-doc-89-1",
      "version": 1,
      "score": 0.85,
      "payload": {
        "document_id": 89,
        "document_title": "Changelog 2024-Q1.docx",
        "chunk_index": 1,
        "content": "Order Service updates in Q1:\n- Performance optimization reducing order processing time by 40%\n- New caching layer for frequent queries\n- Database schema changes for better scalability...",
        "category_id": 8,
        "category_name": "Release Notes"
      }
    }
  ],
  "status": "ok",
  "time": 0.023
}
```

#### 2.3. Tính toán Confidence Score

```csharp
// Average similarity score
var confidenceScore = searchResults.Average(r => r.Score); // 0.88
```

#### 2.4. Xây dựng Context cho GPT

```csharp
var context = string.Join("\n\n---\n\n", searchResults.Select(r => 
    $"Document: {r.Payload.DocumentTitle}\n" +
    $"Category: {r.Payload.CategoryName}\n" +
    $"Content:\n{r.Payload.Content}"
));
```

**Context được tạo:**
```
Document: Order Service API Changes v2.3.md
Category: Technical Documentation
Content:
# Order Service Changes

## Version 2.3 Updates

- Added new endpoint POST /api/orders/bulk for bulk order creation
- Modified order status enum to include 'PENDING_PAYMENT' state
- Updated order validation to require email field...

---

Document: Migration Guide - Order Service.pdf
Category: Technical Documentation
Content:
Breaking changes in Order Service:
1. The old /orders endpoint is deprecated
2. New authentication required for all order operations
3. Payment integration changed from Stripe to PayPal...

---

Document: Changelog 2024-Q1.docx
Category: Release Notes
Content:
Order Service updates in Q1:
- Performance optimization reducing order processing time by 40%
- New caching layer for frequent queries
- Database schema changes for better scalability...
```

#### 2.5. Gọi OpenAI Chat API

**Xây dựng prompt:**
```csharp
var messages = new List<Message> {
    new Message {
        Role = "system",
        Content = @"Bạn là trợ lý AI hỗ trợ truy xuất thông tin từ tài liệu kỹ thuật.
        
Nhiệm vụ:
- Trả lời câu hỏi dựa CHÍNH XÁC trên context được cung cấp
- Nếu context không có thông tin, hãy nói rõ
- Trích dẫn tên tài liệu khi trả lời
- Trả lời bằng tiếng Việt
- Cấu trúc câu trả lời rõ ràng, dễ đọc"
    },
    new Message {
        Role = "user",
        Content = $@"Context từ tài liệu:

{context}

---

Câu hỏi: {userQuestion}

Hãy trả lời dựa trên context trên."
    }
};

var chatRequest = new {
    model = "gpt-4o-mini",
    messages = messages,
    temperature = 0.3,  // Lower = more factual
    max_tokens = 1000
};

// POST https://api.openai.com/v1/chat/completions
```

**OpenAI Chat Response:**
```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1704067200,
  "model": "gpt-4o-mini",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Dựa trên các tài liệu có sẵn, đây là thông tin về các thay đổi trong Order Service:\n\n## Phiên bản 2.3 (từ \"Order Service API Changes v2.3.md\")\n\n**Tính năng mới:**\n- Thêm endpoint POST /api/orders/bulk để tạo nhiều order cùng lúc\n- Thêm trạng thái 'PENDING_PAYMENT' vào order status enum\n- Yêu cầu bắt buộc trường email trong validation\n\n## Breaking Changes (từ \"Migration Guide - Order Service.pdf\")\n\n**Các thay đổi quan trọng:**\n1. Endpoint /orders cũ đã deprecated\n2. Tất cả operations với order hiện yêu cầu authentication\n3. Payment integration chuyển từ Stripe sang PayPal\n\n## Cải tiến Q1 2024 (từ \"Changelog 2024-Q1.docx\")\n\n**Performance & Infrastructure:**\n- Tối ưu hiệu suất, giảm 40% thời gian xử lý order\n- Thêm caching layer cho các query thường xuyên\n- Thay đổi database schema để scale tốt hơn\n\nBạn cần thông tin chi tiết hơn về phần nào không?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 456,
    "completion_tokens": 312,
    "total_tokens": 768
  }
}
```

---

### Step 3: .NET API chuẩn bị response

#### 3.1. Lưu vào database (ChatMessages table)

```sql
INSERT INTO ChatMessages (SessionId, Role, Content, Sources, ConfidenceScore)
VALUES (
  (SELECT Id FROM ChatSessions WHERE SessionId = '123e4567-e89b-12d3-a456-426614174000'),
  'user',
  'Cung cấp cho tôi tài liệu về các thay đổi trong order service',
  NULL,
  NULL
);

INSERT INTO ChatMessages (SessionId, Role, Content, Sources, ConfidenceScore)
VALUES (
  (SELECT Id FROM ChatSessions WHERE SessionId = '123e4567-e89b-12d3-a456-426614174000'),
  'assistant',
  'Dựa trên các tài liệu có sẵn...',
  '[{"documentId":45,"title":"Order Service API Changes v2.3.md"},{"documentId":67,"title":"Migration Guide - Order Service.pdf"},{"documentId":89,"title":"Changelog 2024-Q1.docx"}]',
  0.88
);
```

#### 3.2. Format response

```csharp
var response = new ChatResponse {
    SessionId = sessionId,
    Message = gptResponse.Choices[0].Message.Content,
    Sources = searchResults.Select(r => new DocumentSource {
        DocumentId = r.Payload.DocumentId,
        DocumentTitle = r.Payload.DocumentTitle,
        ChunkContent = r.Payload.Content,
        Score = r.Score
    }).ToList(),
    ConfidenceScore = confidenceScore,
    Timestamp = DateTime.UtcNow
};

return Ok(response);
```

---

### Step 4: Response trả về Frontend

**API Response:**
```json
{
  "sessionId": "123e4567-e89b-12d3-a456-426614174000",
  "message": "Dựa trên các tài liệu có sẵn, đây là thông tin về các thay đổi trong Order Service:\n\n## Phiên bản 2.3 (từ \"Order Service API Changes v2.3.md\")\n\n**Tính năng mới:**\n- Thêm endpoint POST /api/orders/bulk để tạo nhiều order cùng lúc\n- Thêm trạng thái 'PENDING_PAYMENT' vào order status enum\n- Yêu cầu bắt buộc trường email trong validation\n\n## Breaking Changes (từ \"Migration Guide - Order Service.pdf\")\n\n**Các thay đổi quan trọng:**\n1. Endpoint /orders cũ đã deprecated\n2. Tất cả operations với order hiện yêu cầu authentication\n3. Payment integration chuyển từ Stripe sang PayPal\n\n## Cải tiến Q1 2024 (từ \"Changelog 2024-Q1.docx\")\n\n**Performance & Infrastructure:**\n- Tối ưu hiệu suất, giảm 40% thời gian xử lý order\n- Thêm caching layer cho các query thường xuyên\n- Thay đổi database schema để scale tốt hơn\n\nBạn cần thông tin chi tiết hơn về phần nào không?",
  "sources": [
    {
      "documentId": 45,
      "documentTitle": "Order Service API Changes v2.3.md",
      "chunkContent": "# Order Service Changes\n\n## Version 2.3 Updates...",
      "score": 0.92
    },
    {
      "documentId": 67,
      "documentTitle": "Migration Guide - Order Service.pdf",
      "chunkContent": "Breaking changes in Order Service:\n1. The old /orders endpoint...",
      "score": 0.88
    },
    {
      "documentId": 89,
      "documentTitle": "Changelog 2024-Q1.docx",
      "chunkContent": "Order Service updates in Q1:\n- Performance optimization...",
      "score": 0.85
    }
  ],
  "confidenceScore": 0.88,
  "timestamp": "2024-01-01T10:30:00Z"
}
```

---

### Step 5: Angular hiển thị

**Chat UI hiển thị:**

```
┌─────────────────────────────────────────────────────┐
│  User                                    10:29 AM   │
│  ┌───────────────────────────────────────────────┐ │
│  │ Cung cấp cho tôi tài liệu về các thay đổi    │ │
│  │ trong order service                           │ │
│  └───────────────────────────────────────────────┘ │
│                                                     │
│  AI Assistant                            10:30 AM   │
│  ┌───────────────────────────────────────────────┐ │
│  │ Dựa trên các tài liệu có sẵn, đây là thông   │ │
│  │ tin về các thay đổi trong Order Service:     │ │
│  │                                               │ │
│  │ ## Phiên bản 2.3                              │ │
│  │ - Thêm endpoint POST /api/orders/bulk...      │ │
│  │ ...                                           │ │
│  │                                               │ │
│  │ [Sources: 3 documents] [Confidence: 88%]     │ │
│  │                                               │ │
│  │ 📄 Order Service API Changes v2.3.md   (92%) │ │
│  │ 📄 Migration Guide - Order Service.pdf (88%) │ │
│  │ 📄 Changelog 2024-Q1.docx              (85%) │ │
│  └───────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

---

## Tóm tắt Data Flow

### Input/Output cho mỗi component

| Component | Input | Output |
|-----------|-------|--------|
| **User** | Click send | Raw question text |
| **Angular** | User question | HTTP POST với question |
| **.NET API** | Question string | Chat response JSON |
| **OpenAI Embedding** | Question text | Vector [1536 dims] |
| **Qdrant** | Search vector + top_k | Top 3 similar chunks với metadata |
| **OpenAI Chat** | System prompt + Context + Question | Natural language answer |
| **.NET API** | GPT answer + sources | Formatted response |
| **Angular** | Response JSON | Rendered chat UI |

---

## Key Points

### 1. OpenAI được gọi 2 lần
- **Lần 1**: Embedding API - chuyển câu hỏi thành vector để search
- **Lần 2**: Chat API - tạo câu trả lời từ context

### 2. Qdrant vai trò
- Không trả lời câu hỏi
- Chỉ tìm các chunks **tương tự** nhất với câu hỏi
- Return: document chunks + metadata + similarity score

### 3. GPT vai trò
- Đọc context từ Qdrant
- Tổng hợp thông tin
- Trả lời bằng ngôn ngữ tự nhiên
- Trích dẫn sources

### 4. .NET API vai trò (orchestrator)
- Điều phối toàn bộ flow
- Call OpenAI embedding
- Query Qdrant
- Build prompt cho GPT
- Lưu chat history
- Format response

---

## Trường hợp không tìm thấy

**Nếu Qdrant không tìm thấy chunks phù hợp (score < 0.7):**

```json
{
  "message": "Xin lỗi, tôi không tìm thấy tài liệu nào về 'order service' trong hệ thống. Bạn có thể thử:\n- Upload thêm tài liệu liên quan\n- Kiểm tra lại từ khóa tìm kiếm\n- Liên hệ admin để bổ sung tài liệu",
  "sources": [],
  "confidenceScore": 0.0
}
```

---

## Cost Estimate (per query)

```
Embedding API: ~$0.00002 (15 tokens)
Chat API: ~$0.00015 (768 tokens)
Total per query: ~$0.00017
```

Với 1000 queries/day = ~$5/month
