using System.Text.Json;

namespace DocumentRAG.API.Services;

public class QdrantService : IQdrantService
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<QdrantService> _logger;
    private readonly string _collectionName = "documents";

    public QdrantService(HttpClient httpClient, IConfiguration configuration, ILogger<QdrantService> logger)
    {
        _httpClient = httpClient;
        _logger = logger;
        var qdrantUrl = configuration["Qdrant:Url"] ?? "http://localhost:6333";
        _httpClient.BaseAddress = new Uri(qdrantUrl);
    }

    public async Task<List<QdrantSearchResult>> SearchAsync(float[] vector, int limit = 3, int? categoryId = null)
    {
        try
        {
            var searchRequest = new
            {
                vector,
                limit,
                score_threshold = 0.7,
                with_payload = true,
                filter = categoryId.HasValue ? new
                {
                    must = new[] { new { key = "category_id", match = new { value = categoryId.Value } } }
                } : null
            };

            var response = await _httpClient.PostAsJsonAsync($"/collections/{_collectionName}/points/search", searchRequest);
            response.EnsureSuccessStatusCode();

            var result = await response.Content.ReadFromJsonAsync<QdrantSearchResponse>();
            
            if (result?.Result == null)
                return new List<QdrantSearchResult>();

            return result.Result.Select(r => new QdrantSearchResult(
                Id: r.Id,
                Score: r.Score,
                DocumentId: r.Payload.DocumentId,
                DocumentTitle: r.Payload.DocumentTitle,
                Content: r.Payload.Content,
                CategoryId: r.Payload.CategoryId,
                CategoryName: r.Payload.CategoryName,
                ChunkIndex: r.Payload.ChunkIndex
            )).ToList();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error searching Qdrant");
            throw;
        }
    }

    public async Task<bool> IsHealthyAsync()
    {
        try
        {
            var response = await _httpClient.GetAsync("/healthz");
            return response.IsSuccessStatusCode;
        }
        catch
        {
            return false;
        }
    }

    private record QdrantSearchResponse(List<QdrantPoint> Result);
    private record QdrantPoint(string Id, double Score, QdrantPayload Payload);
    private record QdrantPayload(
        int DocumentId,
        string DocumentTitle,
        string Content,
        int CategoryId,
        string CategoryName,
        int ChunkIndex
    );
}
