using DocumentRAG.API.DTOs;
using DocumentRAG.Core.Entities;
using DocumentRAG.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;
using StackExchange.Redis;
using System.Text.Json;

namespace DocumentRAG.API.Services;

public class DocumentService : IDocumentService
{
    private readonly ApplicationDbContext _context;
    private readonly IConnectionMultiplexer _redis;
    private readonly IConfiguration _configuration;
    private readonly ILogger<DocumentService> _logger;

    public DocumentService(
        ApplicationDbContext context,
        IConnectionMultiplexer redis,
        IConfiguration configuration,
        ILogger<DocumentService> logger)
    {
        _context = context;
        _redis = redis;
        _configuration = configuration;
        _logger = logger;
    }

    public async Task<DocumentDto> UploadAsync(IFormFile file, int categoryId)
    {
        try
        {
            // Validate category exists
            var category = await _context.Categories.FindAsync(categoryId);
            if (category == null)
                throw new Exception("Category not found");

            // Generate unique filename
            var storageFileName = $"{Guid.NewGuid()}{Path.GetExtension(file.FileName)}";
            var storagePath = _configuration["Storage:Path"] ?? "/app/storage";
            Directory.CreateDirectory(storagePath);
            
            var filePath = Path.Combine(storagePath, storageFileName);

            // Save file
            using (var stream = new FileStream(filePath, FileMode.Create))
            {
                await file.CopyToAsync(stream);
            }

            // Create document record
            var document = new Document
            {
                Title = Path.GetFileNameWithoutExtension(file.FileName),
                OriginalFileName = file.FileName,
                StorageFileName = storageFileName,
                FilePath = filePath,
                FileSize = file.Length,
                FileType = Path.GetExtension(file.FileName).TrimStart('.').ToLowerInvariant(),
                CategoryId = categoryId,
                Status = DocumentStatus.Pending,
                UploadedAt = DateTime.UtcNow
            };

            _context.Documents.Add(document);
            await _context.SaveChangesAsync();

            // Enqueue processing job
            var db = _redis.GetDatabase();
            var queueName = _configuration["Redis:Queue"] ?? "document_processing";
            await db.ListRightPushAsync(queueName, JsonSerializer.Serialize(new
            {
                document_id = document.Id,
                file_path = filePath,
                file_type = document.FileType
            }));

            _logger.LogInformation("Document {DocumentId} uploaded and queued for processing", document.Id);

            return MapToDto(document);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error uploading document");
            throw;
        }
    }

    public async Task<DocumentListDto> GetDocumentsAsync(int page, int pageSize, string? searchTerm, int? categoryId)
    {
        var query = _context.Documents.Include(d => d.Category).AsQueryable();

        if (!string.IsNullOrWhiteSpace(searchTerm))
        {
            query = query.Where(d => d.Title.Contains(searchTerm));
        }

        if (categoryId.HasValue)
        {
            query = query.Where(d => d.CategoryId == categoryId.Value);
        }

        var totalCount = await query.CountAsync();
        
        var documents = await query
            .OrderByDescending(d => d.UploadedAt)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync();

        return new DocumentListDto(
            documents.Select(MapToDto).ToList(),
            totalCount,
            page,
            pageSize
        );
    }

    public async Task<DocumentDto?> GetByIdAsync(int id)
    {
        var document = await _context.Documents
            .Include(d => d.Category)
            .FirstOrDefaultAsync(d => d.Id == id);

        return document == null ? null : MapToDto(document);
    }

    public async Task<DocumentDto> UpdateAsync(int id, UpdateDocumentDto dto)
    {
        var document = await _context.Documents.Include(d => d.Category).FirstOrDefaultAsync(d => d.Id == id);
        if (document == null)
            throw new Exception("Document not found");

        var category = await _context.Categories.FindAsync(dto.CategoryId);
        if (category == null)
            throw new Exception("Category not found");

        document.Title = dto.Title;
        document.CategoryId = dto.CategoryId;

        await _context.SaveChangesAsync();
        
        return MapToDto(document);
    }

    public async Task DeleteAsync(int id)
    {
        var document = await _context.Documents.FindAsync(id);
        if (document == null)
            throw new Exception("Document not found");

        // Delete physical file
        if (File.Exists(document.FilePath))
        {
            File.Delete(document.FilePath);
        }

        // Delete from database (cascades to chunks)
        _context.Documents.Remove(document);
        await _context.SaveChangesAsync();

        _logger.LogInformation("Document {DocumentId} deleted", id);
    }

    private static DocumentDto MapToDto(Document document)
    {
        return new DocumentDto(
            document.Id,
            document.Title,
            document.OriginalFileName,
            document.FileType,
            document.FileSize,
            document.CategoryId,
            document.Category.Name,
            document.Status.ToString(),
            document.UploadedAt,
            document.ProcessedAt,
            document.ErrorMessage
        );
    }
}
