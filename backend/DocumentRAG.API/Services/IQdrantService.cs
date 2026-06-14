namespace DocumentRAG.API.Services;

public interface IQdrantService
{
    Task<List<QdrantSearchResult>> SearchAsync(float[] vector, int limit = 3, int? categoryId = null);
    Task<bool> IsHealthyAsync();
}

public record QdrantSearchResult(
    string Id,
    double Score,
    int DocumentId,
    string DocumentTitle,
    string Content,
    int CategoryId,
    string CategoryName,
    int ChunkIndex
);
