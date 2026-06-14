using DocumentRAG.API.DTOs;
using DocumentRAG.Core.Entities;
using DocumentRAG.Infrastructure.Data;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace DocumentRAG.API.Controllers;

[ApiController]
[Route("api/[controller]")]
public class CategoriesController : ControllerBase
{
    private readonly ApplicationDbContext _context;

    public CategoriesController(ApplicationDbContext context)
    {
        _context = context;
    }

    [HttpGet]
    public async Task<ActionResult<List<CategoryDto>>> GetAll()
    {
        var categories = await _context.Categories
            .OrderBy(c => c.Name)
            .Select(c => new CategoryDto(c.Id, c.Name, c.Description, c.CreatedAt))
            .ToListAsync();

        return Ok(categories);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<CategoryDto>> GetById(int id)
    {
        var category = await _context.Categories.FindAsync(id);
        if (category == null)
            return NotFound();

        return Ok(new CategoryDto(category.Id, category.Name, category.Description, category.CreatedAt));
    }

    [HttpPost]
    public async Task<ActionResult<CategoryDto>> Create(CreateCategoryDto dto)
    {
        var category = new Category
        {
            Name = dto.Name,
            Description = dto.Description,
            CreatedAt = DateTime.UtcNow
        };

        _context.Categories.Add(category);
        await _context.SaveChangesAsync();

        var result = new CategoryDto(category.Id, category.Name, category.Description, category.CreatedAt);
        return CreatedAtAction(nameof(GetById), new { id = category.Id }, result);
    }

    [HttpPut("{id}")]
    public async Task<ActionResult<CategoryDto>> Update(int id, UpdateCategoryDto dto)
    {
        var category = await _context.Categories.FindAsync(id);
        if (category == null)
            return NotFound();

        category.Name = dto.Name;
        category.Description = dto.Description;
        category.UpdatedAt = DateTime.UtcNow;

        await _context.SaveChangesAsync();

        return Ok(new CategoryDto(category.Id, category.Name, category.Description, category.CreatedAt));
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
        var category = await _context.Categories.FindAsync(id);
        if (category == null)
            return NotFound();

        var hasDocuments = await _context.Documents.AnyAsync(d => d.CategoryId == id);
        if (hasDocuments)
            return BadRequest("Cannot delete category with documents");

        _context.Categories.Remove(category);
        await _context.SaveChangesAsync();

        return NoContent();
    }
}
