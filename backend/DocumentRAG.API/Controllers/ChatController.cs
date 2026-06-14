using DocumentRAG.API.DTOs;
using DocumentRAG.API.Services;
using DocumentRAG.Infrastructure.Data;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Text;
using System.Text.Json;

namespace DocumentRAG.API.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ChatController : ControllerBase
{
    private readonly IRAGService _ragService;
    private readonly ApplicationDbContext _context;

    public ChatController(IRAGService ragService, ApplicationDbContext context)
    {
        _ragService = ragService;
        _context = context;
    }

    [HttpPost("query")]
    public async Task<ActionResult<ChatQueryResponse>> Query(ChatQueryRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.Message))
            return BadRequest("Message is required");

        try
        {
            var response = await _ragService.QueryAsync(request.Message, request.SessionId, request.CategoryId);
            return Ok(response);
        }
        catch (Exception ex)
        {
            return StatusCode(500, ex.Message);
        }
    }

    [HttpPost("sessions")]
    public async Task<ActionResult<ChatSessionDto>> CreateSession()
    {
        var session = new Core.Entities.ChatSession
        {
            SessionId = Guid.NewGuid(),
            CreatedAt = DateTime.UtcNow
        };

        _context.ChatSessions.Add(session);
        await _context.SaveChangesAsync();

        return Ok(new ChatSessionDto(session.SessionId, session.CreatedAt, new List<ChatMessageDto>()));
    }

    [HttpGet("sessions/{sessionId}")]
    public async Task<ActionResult<ChatSessionDto>> GetSession(Guid sessionId)
    {
        var session = await _context.ChatSessions
            .Include(s => s.Messages)
            .FirstOrDefaultAsync(s => s.SessionId == sessionId);

        if (session == null)
            return NotFound();

        var messages = session.Messages.OrderBy(m => m.CreatedAt).Select(m => new ChatMessageDto(
            m.Role,
            m.Content,
            string.IsNullOrEmpty(m.Sources) ? null : JsonSerializer.Deserialize<List<DocumentSource>>(m.Sources),
            m.ConfidenceScore,
            m.CreatedAt
        )).ToList();

        return Ok(new ChatSessionDto(session.SessionId, session.CreatedAt, messages));
    }

    [HttpGet("sessions/{sessionId}/export")]
    public async Task<IActionResult> ExportSession(Guid sessionId, [FromQuery] string format = "json")
    {
        var session = await _context.ChatSessions
            .Include(s => s.Messages)
            .FirstOrDefaultAsync(s => s.SessionId == sessionId);

        if (session == null)
            return NotFound();

        var messages = session.Messages.OrderBy(m => m.CreatedAt).Select(m => new
        {
            role = m.Role,
            content = m.Content,
            sources = string.IsNullOrEmpty(m.Sources) ? null : JsonSerializer.Deserialize<List<DocumentSource>>(m.Sources),
            confidenceScore = m.ConfidenceScore,
            createdAt = m.CreatedAt
        }).ToList();

        if (format.ToLower() == "json")
        {
            var json = JsonSerializer.Serialize(new
            {
                sessionId = session.SessionId,
                createdAt = session.CreatedAt,
                messages
            }, new JsonSerializerOptions { WriteIndented = true });

            return File(Encoding.UTF8.GetBytes(json), "application/json", $"chat-{sessionId}.json");
        }
        else if (format.ToLower() == "csv")
        {
            var csv = new StringBuilder();
            csv.AppendLine("Role,Content,ConfidenceScore,CreatedAt");

            foreach (var msg in messages)
            {
                csv.AppendLine($"\"{msg.role}\",\"{msg.content.Replace("\"", "\"\"")}\",\"{msg.confidenceScore}\",\"{msg.createdAt:yyyy-MM-dd HH:mm:ss}\"");
            }

            return File(Encoding.UTF8.GetBytes(csv.ToString()), "text/csv", $"chat-{sessionId}.csv");
        }

        return BadRequest("Invalid format. Use 'json' or 'csv'");
    }
}
