namespace DocumentRAG.Core.Entities;

public class ChatSession
{
    public int Id { get; set; }
    public Guid SessionId { get; set; }
    public DateTime CreatedAt { get; set; }
    
    public ICollection<ChatMessage> Messages { get; set; } = new List<ChatMessage>();
}
