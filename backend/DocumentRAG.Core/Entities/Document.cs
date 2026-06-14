namespace DocumentRAG.Core.Entities;

public class Document
{
    public int Id { get; set; }
    public string Title { get; set; } = string.Empty;
    public string OriginalFileName { get; set; } = string.Empty;
    public string StorageFileName { get; set; } = string.Empty;
    public string FilePath { get; set; } = string.Empty;
    public long FileSize { get; set; }
    public string FileType { get; set; } = string.Empty;
    public int CategoryId { get; set; }
    public DocumentStatus Status { get; set; }
    public DateTime UploadedAt { get; set; }
    public DateTime? ProcessedAt { get; set; }
    public string? ErrorMessage { get; set; }
    
    public Category Category { get; set; } = null!;
    public ICollection<DocumentChunk> Chunks { get; set; } = new List<DocumentChunk>();
}

public enum DocumentStatus
{
    Pending,
    Processing,
    Completed,
    Failed
}
