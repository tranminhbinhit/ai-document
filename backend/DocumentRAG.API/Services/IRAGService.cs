using DocumentRAG.API.DTOs;

namespace DocumentRAG.API.Services;

public interface IRAGService
{
    Task<ChatQueryResponse> QueryAsync(string message, Guid? sessionId, int? categoryId);
}
