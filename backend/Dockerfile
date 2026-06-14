FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src

# Copy solution and project files
COPY ["DocumentRAG.API/DocumentRAG.API.csproj", "DocumentRAG.API/"]
COPY ["DocumentRAG.Core/DocumentRAG.Core.csproj", "DocumentRAG.Core/"]
COPY ["DocumentRAG.Infrastructure/DocumentRAG.Infrastructure.csproj", "DocumentRAG.Infrastructure/"]

# Restore dependencies
RUN dotnet restore "DocumentRAG.API/DocumentRAG.API.csproj"

# Copy everything else
COPY . .

# Build
WORKDIR "/src/DocumentRAG.API"
RUN dotnet build "DocumentRAG.API.csproj" -c Release -o /app/build

# Publish
FROM build AS publish
RUN dotnet publish "DocumentRAG.API.csproj" -c Release -o /app/publish /p:UseAppHost=false

# Runtime
FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS final
WORKDIR /app
EXPOSE 8080
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "DocumentRAG.API.dll"]
