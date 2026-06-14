# Document Indexer

Hệ thống tự động theo dõi và index tài liệu vào SQL Server database. Khi có file mới hoặc thay đổi trong thư mục được giám sát, hệ thống sẽ tự động:
- Đọc và phân tích nội dung (PDF, DOCX, XLSX, TXT, MD)
- Tạo summary và extract keywords
- Lưu metadata vào database để tra cứu nhanh

## Kiến trúc

```
Kiro
  |
  +-----------+-----------+
  |                       |
Filesystem MCP      SQL MCP
  |                       |
Documents         Document Index
```

- **Filesystem MCP**: Đọc và phân tích tài liệu từ thư mục
- **SQL MCP**: Truy vấn document index từ database
- **Document Indexer**: Service tự động index khi có thay đổi

## Cấu trúc thư mục

```
document-indexer/
├── watcher.py           # Theo dõi thư mục và trigger index
├── processor.py         # Xử lý file: đọc, phân tích, extract metadata
├── database.py          # Kết nối và thao tác với SQL Server
├── config.py            # Cấu hình database
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker image cho watcher
├── docker-compose.yml   # Triển khai toàn bộ stack
├── init.sql            # Script khởi tạo database
└── .env.example        # Template cấu hình
```

## Database Schema

```sql
CREATE TABLE Documents (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    FileName NVARCHAR(255) NOT NULL,
    Path NVARCHAR(500) NOT NULL UNIQUE,
    Summary NVARCHAR(MAX),
    Keywords NVARCHAR(MAX),
    IsDelete BIT DEFAULT 0,
    CreatedDate DATETIME DEFAULT GETDATE(),
    ModifiedDate DATETIME DEFAULT GETDATE()
);
```

## Triển khai

### Option 1: Docker (Khuyến nghị)

**Bước 1**: Tạo file `.env` từ template

```bash
cp .env.example .env
```

Chỉnh sửa `.env`:
```env
WATCH_FOLDER=./documents
```

**Bước 2**: Khởi động stack

```bash
docker-compose up -d
```

Stack bao gồm:
- SQL Server 2022 (port 1433)
- Document Watcher service
- Auto-init database với schema

**Bước 3**: Kiểm tra logs

```bash
docker-compose logs -f document-watcher
```

**Bước 4**: Test bằng cách copy file vào thư mục

```bash
cp sample.pdf ./documents/
```

### Option 2: Chạy Local

**Yêu cầu**:
- Python 3.11+
- SQL Server (local hoặc remote)
- FreeTDS (cho pymssql connection)

**Bước 1**: Cài đặt dependencies

```bash
pip install -r requirements.txt
```

**Bước 2**: Cấu hình database

Tạo database và table:
```bash
# Kết nối SQL Server và chạy init.sql
sqlcmd -S localhost -U sa -P YourPassword -i init.sql
```

**Bước 3**: Cấu hình environment

```bash
export DB_SERVER=localhost
export DB_DATABASE=DocumentAI
export DB_USER=sa
export DB_PASSWORD=YourPassword
export WATCH_FOLDER=/path/to/documents
```

**Bước 4**: Chạy watcher

```bash
python watcher.py
```

## Cấu hình MCP Servers

Để Kiro có thể truy vấn documents, cần cấu hình 2 MCP servers:

### 1. Filesystem MCP (Đọc tài liệu)

File: `.kiro/settings/mcp.json`

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "python",
      "args": ["mcp-servers/filesystem/server.py"],
      "env": {
        "WORKSPACE_ROOT": ".",
        "ALLOWED_DIRECTORIES": "./documents"
      }
    }
  }
}
```

**Các tool có sẵn**:
- `list_directory` - Liệt kê files trong thư mục
- `read_text_file` - Đọc file text
- `parse_pdf` - Đọc file PDF
- `parse_docx` - Đọc file Word
- `parse_xlsx` - Đọc file Excel

### 2. SQL Server MCP (Query database)

```json
{
  "mcpServers": {
    "sqlserver": {
      "command": "python",
      "args": ["mcp-servers/sqlserver/server.py"],
      "env": {
        "SQL_SERVER": "localhost",
        "SQL_DATABASE": "DocumentAI",
        "SQL_USER": "sa",
        "SQL_PASSWORD": "YourPassword",
        "READ_ONLY": "true"
      }
    }
  }
}
```

**Các tool có sẵn**:
- `list_tables` - Liệt kê tables
- `describe_table` - Xem cấu trúc table
- `query_readonly` - Chạy SELECT query
- `get_table_sample` - Lấy sample data
- `get_table_relationships` - Xem foreign keys

## Sử dụng với Kiro

### Tìm kiếm tài liệu theo keyword

```
Tìm tất cả tài liệu có keyword "contract"
```

Kiro sẽ:
1. Gọi `sqlserver.query_readonly`:
   ```sql
   SELECT FileName, Path, Summary 
   FROM Documents 
   WHERE Keywords LIKE '%contract%'
   ```

### Đọc nội dung tài liệu

```
Đọc file tại /documents/contract.pdf
```

Kiro sẽ:
1. Gọi `filesystem.parse_pdf` với path `/documents/contract.pdf`

### Workflow tổng hợp

```
Tìm tài liệu về "API documentation" và tóm tắt nội dung
```

Kiro sẽ:
1. Query database tìm documents có keyword "API"
2. Dùng Filesystem MCP đọc nội dung các file tìm được
3. Tổng hợp và trả lời

## API Reference (database.py)

### `get_connection()`
Tạo kết nối SQL Server

### `insert_document(file_name, path, summary, keywords)`
Insert document mới vào database

### `document_exists(path)`
Kiểm tra document đã được index chưa

### `search_document(keyword)`
Tìm kiếm document theo keyword

### `update_document(path, summary, keywords)`
Cập nhật metadata của document

## Troubleshooting

### Lỗi kết nối SQL Server

```
Error: Unable to connect to SQL Server
```

**Giải pháp**:
- Kiểm tra SQL Server đã chạy: `docker-compose ps`
- Kiểm tra credentials trong `.env`
- Nếu dùng local SQL Server, đảm bảo port 1433 đang mở
- Test kết nối: `telnet localhost 1433`

### Watcher không phát hiện file mới

```
No events detected
```

**Giải pháp**:
- Kiểm tra WATCH_FOLDER đúng path
- Kiểm tra permissions của thư mục
- Xem logs: `docker-compose logs document-watcher`

### File không được index

```
Already indexed: file.pdf
```

**Giải pháp**:
- File đã tồn tại trong database với cùng path
- Delete record để re-index: `DELETE FROM Documents WHERE Path = '/path/to/file.pdf'`

## Development

### Chạy tests

```bash
python -m pytest tests/
```

### Format code

```bash
black *.py
```

### Xem database

```bash
docker exec -it document-indexer-db /opt/mssql-tools/bin/sqlcmd \
  -S localhost -U sa -P YourStrong@Password123 \
  -Q "SELECT * FROM DocumentAI.dbo.Documents"
```

## Roadmap

- [ ] Hỗ trợ AI summary (OpenAI/Claude)
- [ ] Vector search với embeddings
- [ ] Web UI để quản lý documents
- [ ] Hỗ trợ nhiều database backends (PostgreSQL, SQLite)
- [ ] OCR cho scanned PDFs
- [ ] Batch re-indexing

## License

MIT