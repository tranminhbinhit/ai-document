using DocumentRAG.API.Services;
using DocumentRAG.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;
using StackExchange.Redis;
using OpenAI.Extensions;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Database
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// Redis with retry
var redisHost = builder.Configuration["Redis:Host"] ?? "localhost";
var redisPort = builder.Configuration["Redis:Port"] ?? "6379";
var redisConfig = $"{redisHost}:{redisPort},abortConnect=false,connectTimeout=5000,connectRetry=5";
builder.Services.AddSingleton<IConnectionMultiplexer>(ConnectionMultiplexer.Connect(redisConfig));

// OpenAI
var openAiKey = builder.Configuration["OpenAI:ApiKey"] ?? throw new Exception("OpenAI API key is required");
builder.Services.AddOpenAIService(settings => settings.ApiKey = openAiKey);

// HTTP Client for Qdrant
builder.Services.AddHttpClient<IQdrantService, QdrantService>();

// Application Services
builder.Services.AddScoped<IDocumentService, DocumentService>();
builder.Services.AddScoped<IRAGService, RAGService>();

// CORS
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

var app = builder.Build();

// Configure the HTTP request pipeline
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseCors("AllowAll");

app.UseAuthorization();

app.MapControllers();

// Ensure database is created
using (var scope = app.Services.CreateScope())
{
    var context = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
    try
    {
        // Wait for SQL Server to be ready
        var retries = 10;
        while (retries > 0)
        {
            try
            {
                await context.Database.CanConnectAsync();
                app.Logger.LogInformation("Database connection successful");
                break;
            }
            catch
            {
                retries--;
                if (retries == 0) throw;
                app.Logger.LogWarning("Waiting for database... {Retries} retries left", retries);
                await Task.Delay(5000);
            }
        }
    }
    catch (Exception ex)
    {
        app.Logger.LogError(ex, "Database connection failed");
    }
}

app.Run();
