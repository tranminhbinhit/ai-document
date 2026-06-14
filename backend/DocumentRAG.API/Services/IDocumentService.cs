using DocumentRAG.API.DTOs;

namespace DocumentRAG.API.Services;

public interface IDocumentService
{
    Task<DocumentDto> UploadAsync(IFormFile file, int categoryId);
    Task<DocumentListDto> GetDocumentsAsync(int page, int pageSize, string? searchTerm, int? categoryId);
    Task<DocumentDto?> GetByIdAsync(int id);
    Task<DocumentDto> UpdateAsync(int id, UpdateDocumentDto dto);
    Task DeleteAsync(int id);
}
