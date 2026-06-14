namespace DocumentRAG.API.DTOs;

public record ChatQueryRequest(Guid? SessionId, string Message, int? CategoryId);

public record ChatQueryResponse(
    Guid SessionId,
    string Message,
    List<DocumentSource> Sources,
    decimal ConfidenceScore,
    DateTime Timestamp
);

public record DocumentSource(
    int DocumentId,
    string DocumentTitle,
    string ChunkContent,
    double Score
);

public record ChatSessionDto(Guid SessionId, DateTime CreatedAt, List<ChatMessageDto> Messages);

public record ChatMessageDto(
    string Role,
    string Content,
    List<DocumentSource>? Sources,
    decimal? ConfidenceScore,
    DateTime CreatedAt
);

public record ExportChatRequest(string Format); // json or csv
