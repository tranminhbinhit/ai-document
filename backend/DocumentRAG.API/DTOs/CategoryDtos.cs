namespace DocumentRAG.API.DTOs;

public record CategoryDto(int Id, string Name, string? Description, DateTime CreatedAt);

public record CreateCategoryDto(string Name, string? Description);

public record UpdateCategoryDto(string Name, string? Description);
