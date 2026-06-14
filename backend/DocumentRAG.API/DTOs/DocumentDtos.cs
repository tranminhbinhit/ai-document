using DocumentRAG.Core.Entities;

namespace DocumentRAG.API.DTOs;

public record DocumentDto(
    int Id,
    string Title,
    string OriginalFileName,
    string FileType,
    long FileSize,
    int CategoryId,
    string CategoryName,
    string Status,
    DateTime UploadedAt,
    DateTime? ProcessedAt,
    string? ErrorMessage
);

public record DocumentListDto(
    List<DocumentDto> Documents,
    int TotalCount,
    int Page,
    int PageSize
);

public record UpdateDocumentDto(string Title, int CategoryId);
