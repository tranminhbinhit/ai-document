# Kiro Settings Directory

## 📁 Cấu trúc

```
.kiro/settings/
├── mcp.json          # MCP servers configuration
└── README.md         # This file

Root level:
├── .env              # Environment variables (credentials) - KHÔNG commit!
└── .env.example      # Template
```

## 🔧 mcp.json

Config cho 4 MCP servers:
- **filesystem** - Đọc documents
- **gitlab** - Source code & CI/CD  
- **sqlserver** - Database queries
- **kubernetes** - K8s monitoring

## 🔐 .env

**Chứa credentials - KHÔNG commit vào Git!**

Copy từ template:
```bash
cp .env.example .env
```

Sau đó edit `.env` với credentials thực:
- GitLab token
- SQL Server connection
- Kubernetes config path

## 🚀 Setup

1. Copy template (ở root level):
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` với credentials của bạn

3. Restart Kiro → Command Palette → "MCP: Reconnect Servers"

## ⚠️ Security

- `.env` đã được thêm vào `.gitignore`
- KHÔNG bao giờ commit credentials
- Dùng environment variables, không hardcode
- Regular token rotation
