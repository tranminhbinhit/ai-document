# Deployment Guide

## Production Deployment Options

### Option 1: Docker Compose (Recommended for Single Server)

#### Prerequisites
- Linux server (Ubuntu 20.04+ recommended)
- Docker & Docker Compose installed
- Domain name (optional but recommended)
- SSL certificate (Let's Encrypt recommended)

#### Steps

1. **Server Setup**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

2. **Clone Repository**

```bash
git clone <your-repo>
cd document-rag-system
```

3. **Configure Environment**

```bash
cp .env.example .env
nano .env
```

Set production values:
```env
SQL_SA_PASSWORD=<strong-random-password>
OPENAI_API_KEY=<your-production-key>
```

4. **Update docker-compose for Production**

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    environment:
      - ASPNETCORE_ENVIRONMENT=Production
      - ASPNETCORE_URLS=https://+:443;http://+:80
      - ASPNETCORE_Kestrel__Certificates__Default__Path=/app/cert.pfx
      - ASPNETCORE_Kestrel__Certificates__Default__Password=${CERT_PASSWORD}
    volumes:
      - ./certs:/app/certs
    ports:
      - "443:443"
      - "80:80"

  frontend:
    environment:
      - API_URL=https://your-domain.com/api
```

5. **SSL Certificate Setup**

```bash
# Install Certbot
sudo apt install certbot

# Get certificate
sudo certbot certonly --standalone -d your-domain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ./certs/
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ./certs/
```

6. **Start Services**

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

7. **Setup Nginx Reverse Proxy (Optional)**

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:4200;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Option 2: Kubernetes

#### Prerequisites
- Kubernetes cluster (EKS, GKE, AKS, or self-hosted)
- kubectl configured
- Helm installed

#### Steps

1. **Create Kubernetes Manifests**

See `k8s/` directory for example manifests:
- `k8s/namespace.yaml`
- `k8s/secrets.yaml`
- `k8s/configmap.yaml`
- `k8s/deployments/`
- `k8s/services/`
- `k8s/ingress.yaml`

2. **Deploy**

```bash
kubectl apply -f k8s/
```

### Option 3: Cloud-Specific

#### AWS

- **ECS**: Use Docker images with ECS tasks
- **EKS**: Kubernetes deployment
- **RDS**: Replace SQL Server container with RDS SQL Server
- **ElastiCache**: Replace Redis container
- **S3**: For document storage

#### Azure

- **AKS**: Kubernetes deployment
- **Azure SQL**: Replace SQL Server container
- **Azure Cache for Redis**: Replace Redis
- **Azure Blob Storage**: For document storage
- **Azure OpenAI**: Replace OpenAI API

#### Google Cloud

- **GKE**: Kubernetes deployment
- **Cloud SQL**: Replace SQL Server
- **Memorystore**: Replace Redis
- **Cloud Storage**: For document storage

## Security Hardening

### 1. Environment Variables

Never commit `.env` to git. Use secrets management:

- **Docker**: Docker secrets
- **Kubernetes**: Kubernetes secrets
- **Cloud**: AWS Secrets Manager, Azure Key Vault, GCP Secret Manager

### 2. Network Security

```yaml
# docker-compose with network isolation
networks:
  backend:
    internal: true
  frontend:

services:
  backend:
    networks:
      - backend
      - frontend
  
  sql-server:
    networks:
      - backend
```

### 3. SQL Server Security

```sql
-- Create application user (don't use sa in production)
CREATE LOGIN app_user WITH PASSWORD = 'StrongPassword123!';
CREATE USER app_user FOR LOGIN app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON SCHEMA::dbo TO app_user;
```

### 4. API Rate Limiting

Add rate limiting middleware in backend:

```csharp
builder.Services.AddRateLimiter(options => {
    options.GlobalLimiter = PartitionedRateLimiter.Create<HttpContext, string>(context =>
        RateLimitPartition.GetFixedWindowLimiter(
            partitionKey: context.Connection.RemoteIpAddress?.ToString() ?? "unknown",
            factory: _ => new FixedWindowRateLimiterOptions
            {
                PermitLimit = 100,
                Window = TimeSpan.FromMinutes(1)
            }));
});
```

### 5. CORS Configuration

Update for production domains:

```csharp
builder.Services.AddCors(options => {
    options.AddPolicy("Production", policy => {
        policy.WithOrigins("https://your-domain.com")
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});
```

## Monitoring & Logging

### 1. Application Monitoring

Add Prometheus metrics:

```csharp
builder.Services.AddOpenTelemetry()
    .WithMetrics(metrics => {
        metrics.AddPrometheusExporter();
        metrics.AddMeter("DocumentRAG");
    });
```

### 2. Log Aggregation

Configure centralized logging:

```yaml
# docker-compose with logging
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

Or use ELK stack, Grafana Loki, etc.

### 3. Health Checks

Add health check endpoints:

```csharp
builder.Services.AddHealthChecks()
    .AddSqlServer(connectionString)
    .AddRedis(redisConnection)
    .AddUrlGroup(new Uri(qdrantUrl + "/healthz"), "qdrant");

app.MapHealthChecks("/health");
```

## Backup Strategy

### 1. SQL Server Backup

```bash
# Automated backup script
docker exec rag-sqlserver /opt/mssql-tools/bin/sqlcmd \
  -S localhost -U sa -P "${SQL_SA_PASSWORD}" \
  -Q "BACKUP DATABASE DocumentRAG TO DISK = '/var/opt/mssql/backup/DocumentRAG.bak'"

# Copy to external storage
docker cp rag-sqlserver:/var/opt/mssql/backup/DocumentRAG.bak ./backups/
```

### 2. Qdrant Backup

```bash
# Create snapshot
curl -X POST http://localhost:6333/collections/documents/snapshots

# Download snapshot
curl http://localhost:6333/collections/documents/snapshots/<snapshot-name> -o qdrant-backup.snapshot
```

### 3. Document Storage Backup

```bash
# Backup document volume
docker run --rm -v document-storage:/data -v $(pwd)/backups:/backup \
  alpine tar czf /backup/documents-$(date +%Y%m%d).tar.gz /data
```

## Performance Optimization

### 1. Database Indexing

Indexes are already created in init-db.sql, but monitor query performance:

```sql
-- Check missing indexes
SELECT * FROM sys.dm_db_missing_index_details;
```

### 2. Qdrant Performance

```python
# Increase HNSW parameters for better performance
client.update_collection(
    collection_name="documents",
    hnsw_config=models.HnswConfigDiff(
        m=32,
        ef_construct=200
    )
)
```

### 3. Redis Configuration

```bash
# Increase max memory
docker run -d --name rag-redis redis:7-alpine \
  --maxmemory 256mb \
  --maxmemory-policy allkeys-lru
```

### 4. Backend Scaling

Scale backend horizontally:

```bash
docker-compose up -d --scale backend=3
```

Add load balancer (nginx, HAProxy, cloud LB).

## Cost Optimization

### 1. OpenAI Costs

- Use caching for repeated queries
- Implement query deduplication
- Monitor usage via OpenAI dashboard

### 2. Infrastructure Costs

- Use spot/preemptible instances
- Scale down during off-hours
- Use reserved instances for predictable workloads

## Troubleshooting

### Logs Location

```bash
# Container logs
docker logs rag-backend
docker logs rag-indexer

# SQL Server logs
docker exec rag-sqlserver cat /var/opt/mssql/log/errorlog

# Qdrant logs
docker logs rag-qdrant
```

### Performance Issues

```bash
# Check resource usage
docker stats

# Check database connections
docker exec rag-sqlserver /opt/mssql-tools/bin/sqlcmd \
  -S localhost -U sa -P "${SQL_SA_PASSWORD}" \
  -Q "SELECT * FROM sys.dm_exec_sessions"
```

## Maintenance

### Updates

```bash
# Pull latest images
docker-compose pull

# Restart with new images
docker-compose up -d
```

### Database Maintenance

```sql
-- Rebuild indexes
ALTER INDEX ALL ON Documents REBUILD;

-- Update statistics
UPDATE STATISTICS Documents;
```

## Rollback Strategy

```bash
# Tag current version
docker-compose down
docker tag <image> <image>:backup-$(date +%Y%m%d)

# Deploy new version
docker-compose up -d

# If issues, rollback
docker-compose down
docker tag <image>:backup-20240101 <image>:latest
docker-compose up -d
```

## Production Checklist

- [ ] SSL certificates configured
- [ ] Strong passwords in .env
- [ ] CORS configured for production domain
- [ ] Rate limiting enabled
- [ ] Health checks configured
- [ ] Monitoring setup (Prometheus/Grafana)
- [ ] Log aggregation configured
- [ ] Backup automation setup
- [ ] Disaster recovery plan documented
- [ ] Security scanning completed
- [ ] Load testing performed
- [ ] Documentation updated

## Support

For production issues:
1. Check logs: `docker-compose logs <service>`
2. Review monitoring dashboards
3. Check health endpoints
4. Verify external dependencies (OpenAI, network)
