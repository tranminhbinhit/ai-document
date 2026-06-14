# Kiro MCP Servers - Complete Development Assistant

Hệ thống MCP servers biến Kiro thành trợ lý kỹ thuật toàn diện cho workflow Angular + GitLab + Jenkins + Harbor + Kubernetes + SQL Server.

## 🎯 Tổng Quan

Bộ MCP servers + Document Indexer tích hợp với Kiro để hỗ trợ:
- 📄 **Filesystem MCP** - Đọc và phân tích tài liệu (PDF, DOCX, XLSX)
- 📚 **Document Indexer** - Tự động index và search tài liệu
- 🔧 **GitLab MCP** - Browse code, review MRs, monitor pipelines
- 🗄️ **SQL Server MCP** - Query database, analyze schema (read-only)
- ☸️ **Kubernetes MCP** - Monitor pods, check logs, debug issues

## 🏗️ Kiến trúc

```
           Kiro (AI Assistant)
                  |
      +-----------+-----------+
      |                       |
Filesystem MCP          SQL MCP
      |                       |
   Documents          Document Index DB
                            ↑
                     Document Indexer
                       (Auto-sync)
```

**Document Indexer** tự động:
1. Theo dõi thư mục documents
2. Phân tích file mới/thay đổi (PDF, DOCX, XLSX, TXT)
3. Extract summary và keywords
4. Lưu metadata vào SQL Server

**Kiro** có thể:
- Tìm kiếm documents qua SQL MCP (nhanh)
- Đọc nội dung chi tiết qua Filesystem MCP
- Phân tích và tổng hợp thông tin từ nhiều documents

## 🚀 Quick Start

### Prerequisites
```bash
# Python 3.8+
python --version

# Install MCP SDK
pip install mcp
```

### Installation
```bash
# 1. Install dependencies cho từng server
cd mcp-servers/filesystem && pip install -r requirements.txt
cd ../gitlab && pip install -r requirements.txt
cd ../sqlserver && pip install -r requirements.txt
cd ../kubernetes && pip install -r requirements.txt

# 2. Setup environment variables
cp .env.example .env
# Edit .env với credentials của bạn

# 3. Restart Kiro và reconnect MCP servers
# Command Palette → "MCP: Reconnect Servers"
```

**Chi tiết:** Xem [SETUP.md](SETUP.md)

## 📋 Features

### 1. Filesystem MCP - Đọc Tài Liệu

**Công dụng:**
- Phân tích requirements documents (PDF/DOCX)
- Extract data từ Excel spreadsheets
- Hiểu context nghiệp vụ từ tài liệu
- Làm việc với Filesystem trực tiếp

**Ví dụ:**
```
Đọc file requirements.pdf và tóm tắt các yêu cầu chính
List files trong thư mục docs
Parse Excel data từ users.xlsx
```

**Chi tiết:** [mcp-servers/filesystem/](mcp-servers/filesystem/)

### Document Indexer - Auto Document Management

**Công dụng:**
- Tự động theo dõi và index documents
- Search nhanh theo keywords
- Metadata và summary tự động
- Database-backed storage

**Deploy:**
```bash
cd document-indexer
docker-compose up -d
```

**Chi tiết:** [document-indexer/readme.md](document-indexer/readme.md)

### 2. GitLab MCP - Development

**Công dụng:**
- Review Merge Requests tự động
- Search code trong repository
- Monitor CI/CD pipelines
- Browse source code

**Ví dụ:**
```
Review MR #123 và suggest improvements
Tìm tất cả các file implement IUserService
Check pipeline status của branch feature/auth
```

### 3. SQL Server MCP - Database

**Công dụng:**
- Hiểu database schema
- Query data để analysis
- Debug data issues
- Read-only mode để an toàn

**Ví dụ:**
```
Describe schema của bảng Users và relationships
Query 10 orders mới nhất
Kiểm tra duplicate records trong Customers
```

### 4. Kubernetes MCP - Operations

**Công dụng:**
- Monitor production/staging
- Debug pod issues
- Analyze logs
- Investigate incidents

**Ví dụ:**
```
Check logs của api-service pod
List pods đang crash
Analyze events để debug deployment issue
```

## 🔄 Workflows

### Investigate Production Bug
```
1. "API /users/login đang lỗi 500"
   
2. Kiro tự động:
   ✓ Check K8s logs
   ✓ Query database state
   ✓ Search code implementation
   ✓ Check recent MRs
   
3. → Root cause + suggested fix
```

### Review Merge Request
```
1. "Review MR #456"
   
2. Kiro tự động:
   ✓ Get MR details và changes
   ✓ Check DB schema impact
   ✓ Verify business logic
   ✓ Check pipeline status
   
3. → Comprehensive review comments
```

### Analyze Documents
```
1. "Tìm tất cả tài liệu về API documentation"
   
2. Kiro tự động:
   ✓ Query Document Index (SQL MCP)
   ✓ Đọc nội dung các file (Filesystem MCP)
   ✓ Phân tích và tổng hợp
   
3. → Comprehensive summary
```

## 📚 Documentation

- **[PLAN.md](PLAN.md)** - Roadmap chi tiết và timeline
- **[SETUP.md](SETUP.md)** - Hướng dẫn cài đặt từng bước
- **[.kiro/steering/mcp-usage-guide.md](.kiro/steering/mcp-usage-guide.md)** - Hướng dẫn sử dụng
- **[.kiro/steering/gitlab-code-review.md](.kiro/steering/gitlab-code-review.md)** - Code review guidelines

## 🔐 Security

- SQL Server luôn ở **READ_ONLY mode**
- Kubernetes chỉ có **read permissions**
- Filesystem chỉ access **allowed directories**
- Credentials trong **environment variables** (không commit)
- GitLab token với **minimal scopes**

## 🛠️ Configuration

File `.kiro/settings/mcp.json` đã được tạo sẵn với 4 servers:

```json
{
  "mcpServers": {
    "filesystem": { ... },
    "gitlab": { ... },
    "sqlserver": { ... },
    "kubernetes": { "disabled": true }  // Enable khi cần
  }
}
```

## 📊 Structure

Xem chi tiết: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

```
.
├── .env                          # Environment variables
├── .env.example                  # Template
│
├── document-indexer/             # 🆕 Auto document indexing
│   ├── watcher.py                # File watcher
│   ├── processor.py              # Document processor
│   ├── database.py               # Database operations
│   ├── docker-compose.yml        # Deploy stack
│   ├── Dockerfile                # Watcher container
│   └── readme.md                 # Full documentation
│
├── .kiro/
│   ├── settings/
│   │   └── mcp.json              # MCP configuration
│   └── steering/
│       ├── mcp-usage-guide.md    # Usage guide
│       └── gitlab-code-review.md # Review guidelines
│
├── mcp-servers/                  # Custom server implementations
│   ├── filesystem/
│   ├── gitlab/
│   ├── sqlserver/
│   └── kubernetes/
│
├── PLAN.md                       # Roadmap & timeline
├── SETUP.md                      # Setup guide
├── PROJECT_STRUCTURE.md          # Architecture explanation
└── README.md                     # This file
```

## 🧪 Testing

```bash
# Test individual servers
python mcp-servers/filesystem/server.py
python mcp-servers/gitlab/server.py
python mcp-servers/sqlserver/server.py
python mcp-servers/kubernetes/server.py

# Test trong Kiro
# 1. Reconnect MCP servers
# 2. Chat: "List files trong thư mục docs"
# 3. Chat: "Liệt kê merge requests mới nhất"
```

## 📈 Roadmap

- [x] **Phase 1:** Filesystem MCP
- [x] **Phase 2:** GitLab MCP
- [x] **Phase 3:** SQL Server MCP
- [x] **Phase 4:** Kubernetes MCP (foundation)
- [ ] **Phase 5:** Jenkins & Harbor integration
- [ ] **Phase 6:** AI-powered code suggestions
- [ ] **Phase 7:** Team collaboration features

## 🤝 Contributing

Để thêm features hoặc fix bugs:

1. Test server standalone trước
2. Update documentation
3. Add tests
4. Submit MR với description rõ ràng

## 📞 Support

Gặp vấn đề? Check:
1. Logs trong Kiro Output panel (Kiro MCP)
2. Test server standalone: `python server.py`
3. Verify environment variables: `echo $GITLAB_TOKEN`
4. Review [SETUP.md](SETUP.md)

## 📝 License

MIT License - Use freely!

---

**Version:** 1.0  
**Last Updated:** 2026-06-06  
**Author:** Your Team

### Quick Links
- 📖 [Setup Guide](SETUP.md)
- 🗺️ [Roadmap](PLAN.md)
- 🏗️ [Project Structure](PROJECT_STRUCTURE.md)
- 📁 [Why This Structure?](STRUCTURE_SUMMARY.md)
- 📚 [Usage Guide](.kiro/steering/mcp-usage-guide.md)
- ✅ [Code Review Guide](.kiro/steering/gitlab-code-review.md)
