namespace DocumentRAG.Core.Entities;

public class ChatMessage
{
    public int Id { get; set; }
    public int SessionId { get; set; }
    public string Role { get; set; } = string.Empty;
    public string Content { get; set; } = string.Empty;
    public string? Sources { get; set; }
    public decimal? ConfidenceScore { get; set; }
    public DateTime CreatedAt { get; set; }
    
    public ChatSession Session { get; set; } = null!;
}
