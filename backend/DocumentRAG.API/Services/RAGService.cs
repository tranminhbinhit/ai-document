using DocumentRAG.API.DTOs;
using DocumentRAG.Core.Entities;
using DocumentRAG.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;
using OpenAI.Interfaces;
using OpenAI.ObjectModels.RequestModels;
using OpenAI.ObjectModels;
using System.Text.Json;
using ChatMessageEntity = DocumentRAG.Core.Entities.ChatMessage;
using OpenAIChatMessage = OpenAI.ObjectModels.RequestModels.ChatMessage;

namespace DocumentRAG.API.Services;

public class RAGService : IRAGService
{
    private readonly ApplicationDbContext _context;
    private readonly IQdrantService _qdrantService;
    private readonly IOpenAIService _openAIService;
    private readonly ILogger<RAGService> _logger;
    private readonly IConfiguration _configuration;

    public RAGService(
        ApplicationDbContext context,
        IQdrantService qdrantService,
        IOpenAIService openAIService,
        ILogger<RAGService> logger,
        IConfiguration configuration)
    {
        _context = context;
        _qdrantService = qdrantService;
        _openAIService = openAIService;
        _logger = logger;
        _configuration = configuration;
    }

    public async Task<ChatQueryResponse> QueryAsync(string message, Guid? sessionId, int? categoryId)
    {
        try
        {
            // 1. Get or create session
            var session = await GetOrCreateSessionAsync(sessionId);

            // 2. Save user message
            await SaveMessageAsync(session.Id, "user", message, null, null);

            // 3. Generate embedding for the question
            var embeddingModel = _configuration["OpenAI:EmbeddingModel"] ?? "text-embedding-3-small";
            var embeddingResponse = await _openAIService.Embeddings.CreateEmbedding(new EmbeddingCreateRequest
            {
                Model = embeddingModel,
                Input = message
            });

            if (!embeddingResponse.Successful)
            {
                _logger.LogError("OpenAI embedding failed: {Error}", embeddingResponse.Error?.Message);
                throw new Exception("Failed to generate embedding");
            }

            var vector = embeddingResponse.Data.FirstOrDefault()?.Embedding.Select(d => (float)d).ToArray();
            if (vector == null)
                throw new Exception("No embedding returned");

            // 4. Search Qdrant
            var topK = int.Parse(_configuration["RAG:TopK"] ?? "3");
            var searchResults = await _qdrantService.SearchAsync(vector, topK, categoryId);

            if (searchResults.Count == 0)
            {
                var noResultsMessage = "Xin lỗi, tôi không tìm thấy tài liệu phù hợp trong hệ thống. Bạn có thể thử:\n- Upload thêm tài liệu liên quan\n- Kiểm tra lại từ khóa tìm kiếm\n- Liên hệ admin để bổ sung tài liệu";
                await SaveMessageAsync(session.Id, "assistant", noResultsMessage, null, 0);
                
                return new ChatQueryResponse(
                    session.SessionId,
                    noResultsMessage,
                    new List<DocumentSource>(),
                    0,
                    DateTime.UtcNow
                );
            }

            // 5. Calculate confidence score
            var confidenceScore = (decimal)searchResults.Average(r => r.Score);

            // 6. Build context
            var context = string.Join("\n\n---\n\n", searchResults.Select(r =>
                $"Document: {r.DocumentTitle}\nCategory: {r.CategoryName}\nContent:\n{r.Content}"));

            // 7. Call OpenAI Chat
            var chatModel = _configuration["OpenAI:ChatModel"] ?? "gpt-4o-mini";
            var chatResponse = await _openAIService.ChatCompletion.CreateCompletion(new ChatCompletionCreateRequest
            {
                Model = chatModel,
                Temperature = 0.3f,
                MaxTokens = 1000,
                Messages = new List<OpenAIChatMessage>
                {
                    OpenAIChatMessage.FromSystem(@"Bạn là trợ lý AI hỗ trợ truy xuất thông tin từ tài liệu kỹ thuật.

Nhiệm vụ:
- Trả lời câu hỏi dựa CHÍNH XÁC trên context được cung cấp
- Nếu context không có thông tin, hãy nói rõ
- Trích dẫn tên tài liệu khi trả lời
- Trả lời bằng tiếng Việt nếu câu hỏi bằng tiếng Việt
- Cấu trúc câu trả lời rõ ràng, dễ đọc"),
                    OpenAIChatMessage.FromUser($@"Context từ tài liệu:

{context}

---

Câu hỏi: {message}

Hãy trả lời dựa trên context trên.")
                }
            });

            if (!chatResponse.Successful)
            {
                _logger.LogError("OpenAI chat completion failed: {Error}", chatResponse.Error?.Message);
                throw new Exception("Failed to generate response");
            }

            var answer = chatResponse.Choices.FirstOrDefault()?.Message.Content ?? "Không thể tạo câu trả lời";

            // 8. Prepare sources
            var sources = searchResults.Select(r => new DocumentSource(
                r.DocumentId,
                r.DocumentTitle,
                r.Content,
                r.Score
            )).ToList();

            // 9. Save assistant message
            await SaveMessageAsync(session.Id, "assistant", answer, sources, confidenceScore);

            return new ChatQueryResponse(
                session.SessionId,
                answer,
                sources,
                confidenceScore,
                DateTime.UtcNow
            );
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error in RAG query");
            throw;
        }
    }

    private async Task<ChatSession> GetOrCreateSessionAsync(Guid? sessionId)
    {
        if (sessionId.HasValue)
        {
            var existing = await _context.ChatSessions.FirstOrDefaultAsync(s => s.SessionId == sessionId.Value);
            if (existing != null)
                return existing;
        }

        var session = new ChatSession
        {
            SessionId = Guid.NewGuid(),
            CreatedAt = DateTime.UtcNow
        };

        _context.ChatSessions.Add(session);
        await _context.SaveChangesAsync();
        return session;
    }

    private async Task SaveMessageAsync(int sessionId, string role, string content, List<DocumentSource>? sources, decimal? confidenceScore)
    {
        var message = new ChatMessageEntity
        {
            SessionId = sessionId,
            Role = role,
            Content = content,
            Sources = sources != null ? JsonSerializer.Serialize(sources) : null,
            ConfidenceScore = confidenceScore,
            CreatedAt = DateTime.UtcNow
        };

        _context.ChatMessages.Add(message);
        await _context.SaveChangesAsync();
    }
}
