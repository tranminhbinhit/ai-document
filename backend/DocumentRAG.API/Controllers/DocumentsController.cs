using DocumentRAG.API.DTOs;
using DocumentRAG.API.Services;
using Microsoft.AspNetCore.Mvc;

namespace DocumentRAG.API.Controllers;

[ApiController]
[Route("api/[controller]")]
public class DocumentsController : ControllerBase
{
    private readonly IDocumentService _documentService;

    public DocumentsController(IDocumentService documentService)
    {
        _documentService = documentService;
    }

    [HttpPost("upload")]
    public async Task<ActionResult<DocumentDto>> Upload([FromForm] IFormFile file, [FromForm] int categoryId)
    {
        if (file == null || file.Length == 0)
            return BadRequest("No file uploaded");

        try
        {
            var result = await _documentService.UploadAsync(file, categoryId);
            return Ok(result);
        }
        catch (Exception ex)
        {
            return BadRequest(ex.Message);
        }
    }

    [HttpGet]
    public async Task<ActionResult<DocumentListDto>> GetDocuments(
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 20,
        [FromQuery] string? search = null,
        [FromQuery] int? categoryId = null)
    {
        var result = await _documentService.GetDocumentsAsync(page, pageSize, search, categoryId);
        return Ok(result);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<DocumentDto>> GetById(int id)
    {
        var document = await _documentService.GetByIdAsync(id);
        if (document == null)
            return NotFound();

        return Ok(document);
    }

    [HttpPut("{id}")]
    public async Task<ActionResult<DocumentDto>> Update(int id, UpdateDocumentDto dto)
    {
        try
        {
            var result = await _documentService.UpdateAsync(id, dto);
            return Ok(result);
        }
        catch (Exception ex)
        {
            return BadRequest(ex.Message);
        }
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
        try
        {
            await _documentService.DeleteAsync(id);
            return NoContent();
        }
        catch (Exception ex)
        {
            return BadRequest(ex.Message);
        }
    }
}
