# MCP Servers Setup Guide

Hướng dẫn cấu hình MCP servers để tích hợp với Document Indexer.

## Kiến trúc

```
Kiro (AI Assistant)
  |
  +-----------+-----------+
  |                       |
Filesystem MCP      SQL MCP
  |                       |
Documents         Document Index DB
```

- **Filesystem MCP**: Đọc và phân tích tài liệu trực tiếp từ filesystem
- **SQL MCP**: Truy vấn metadata và index từ database

## Cấu hình Kiro MCP

Tạo/chỉnh sửa file: `.kiro/settings/mcp.json`

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "python",
      "args": ["mcp-servers/filesystem/server.py"],
      "env": {
        "WORKSPACE_ROOT": ".",
        "ALLOWED_DIRECTORIES": "./documents,./docs"
      },
      "disabled": false,
      "autoApprove": []
    },
    "sqlserver": {
      "command": "python",
      "args": ["mcp-servers/sqlserver/server.py"],
      "env": {
        "SQL_SERVER": "localhost",
        "SQL_DATABASE": "DocumentAI",
        "SQL_USER": "sa",
        "SQL_PASSWORD": "YourStrong@Password123",
        "READ_ONLY": "true"
      },
      "disabled": false,
      "autoApprove": ["list_tables", "describe_table", "get_table_sample"]
    }
  }
}
```

## Environment Variables

### Filesystem MCP

| Variable | Mô tả | Mặc định |
|----------|-------|----------|
| `WORKSPACE_ROOT` | Thư mục gốc của workspace | `.` |
| `ALLOWED_DIRECTORIES` | Danh sách thư mục được phép truy cập (phân tách bằng dấu phẩy) | `WORKSPACE_ROOT` |

### SQL Server MCP

| Variable | Mô tả | Mặc định |
|----------|-------|----------|
| `SQL_SERVER` | SQL Server hostname/IP | Required |
| `SQL_DATABASE` | Tên database | Required |
| `SQL_USER` | Username | Required |
| `SQL_PASSWORD` | Password | Required |
| `READ_ONLY` | Chỉ cho phép SELECT queries | `true` |

## Filesystem MCP Tools

### 1. list_directory
Liệt kê files và folders trong thư mục

```javascript
{
  "path": "./documents"
}
```

### 2. read_text_file
Đọc file text (txt, md, json, csv)

```javascript
{
  "path": "./documents/readme.txt"
}
```

### 3. parse_pdf
Extract text từ file PDF

```javascript
{
  "path": "./documents/contract.pdf"
}
```

### 4. parse_docx
Extract text từ file Word

```javascript
{
  "path": "./documents/report.docx"
}
```

### 5. parse_xlsx
Extract data từ file Excel

```javascript
{
  "path": "./documents/data.xlsx",
  "sheet_name": "Sheet1"  // optional
}
```

## SQL Server MCP Tools

### 1. list_tables
Liệt kê tất cả tables trong database

```javascript
{}
```

### 2. describe_table
Xem cấu trúc của table

```javascript
{
  "table_name": "Documents"
}
```

### 3. query_readonly
Thực thi SELECT query (read-only)

```javascript
{
  "query": "SELECT * FROM Documents WHERE Keywords LIKE '%contract%'",
  "limit": 100
}
```

### 4. get_table_sample
Lấy sample data từ table

```javascript
{
  "table_name": "Documents",
  "limit": 10
}
```

### 5. get_table_relationships
Xem foreign key relationships

```javascript
{
  "table_name": "Documents"
}
```

## Use Cases với Kiro

### 1. Tìm kiếm tài liệu

**Prompt**: "Tìm tất cả tài liệu về contract"

**Kiro workflow**:
1. `sqlserver.query_readonly`:
   ```sql
   SELECT FileName, Path, Summary 
   FROM Documents 
   WHERE Keywords LIKE '%contract%'
   ```
2. Trả về danh sách documents phù hợp

### 2. Đọc nội dung tài liệu

**Prompt**: "Đọc file contract.pdf và tóm tắt"

**Kiro workflow**:
1. `filesystem.parse_pdf`: Đọc nội dung PDF
2. AI tổng hợp và tóm tắt nội dung

### 3. Phân tích nhiều tài liệu

**Prompt**: "So sánh các tài liệu về pricing"

**Kiro workflow**:
1. `sqlserver.query_readonly`: Tìm documents có keyword "pricing"
2. `filesystem.parse_*`: Đọc từng file
3. AI so sánh và phân tích

### 4. Thống kê documents

**Prompt**: "Có bao nhiêu tài liệu đã được index?"

**Kiro workflow**:
1. `sqlserver.query_readonly`:
   ```sql
   SELECT COUNT(*) as total,
          COUNT(DISTINCT SUBSTRING(FileName, LEN(FileName) - CHARINDEX('.', REVERSE(FileName)) + 2, 10)) as file_types
   FROM Documents
   ```

## Security

### Filesystem MCP
- Chỉ cho phép truy cập trong `ALLOWED_DIRECTORIES`
- Path traversal protection
- Read-only access

### SQL Server MCP
- Chỉ cho phép SELECT queries (READ_ONLY mode)
- SQL injection protection
- Connection timeout

## Troubleshooting

### MCP Server không kết nối

**Triệu chứng**: Kiro không nhìn thấy tools

**Giải pháp**:
1. Kiểm tra `mcp.json` syntax
2. Kiểm tra Python path: `which python` hoặc `where python`
3. Kiểm tra dependencies: `pip list | grep mcp`
4. Xem MCP logs trong Kiro

### Filesystem: Path not allowed

**Triệu chứng**: "Error: Path not allowed"

**Giải pháp**:
- Thêm thư mục vào `ALLOWED_DIRECTORIES`
- Dùng absolute path
- Kiểm tra permissions

### SQL Server: Connection failed

**Triệu chứng**: "Error: Unable to connect"

**Giải pháp**:
- Kiểm tra SQL Server đang chạy
- Kiểm tra credentials
- Kiểm tra network/firewall
- Cài ODBC Driver: [Download](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

### Query timeout

**Triệu chứng**: "Error: Query timeout"

**Giải pháp**:
- Thêm `TOP` clause để limit kết quả
- Tối ưu query với index
- Tăng timeout trong connection string

## Testing

### Test Filesystem MCP

```bash
# Test server chạy được
python mcp-servers/filesystem/server.py

# Test parse PDF
echo '{"method": "tools/call", "params": {"name": "parse_pdf", "arguments": {"path": "./test.pdf"}}}' | python mcp-servers/filesystem/server.py
```

### Test SQL Server MCP

```bash
# Set environment variables
export SQL_SERVER=localhost
export SQL_DATABASE=DocumentAI
export SQL_USER=sa
export SQL_PASSWORD=YourPassword

# Test server
python mcp-servers/sqlserver/server.py
```

## Development

### Thêm tool mới cho Filesystem MCP

1. Thêm Tool definition trong `list_tools()`
2. Implement handler function
3. Add handler vào `call_tool()`
4. Test

### Thêm tool mới cho SQL Server MCP

1. Thêm Tool definition trong `list_tools()`
2. Implement async handler
3. Add handler vào `call_tool()`
4. Test với sample query

## Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [ODBC Driver Download](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
- [PyPDF2 Docs](https://pypdf2.readthedocs.io/)
- [python-docx Docs](https://python-docx.readthedocs.io/)
