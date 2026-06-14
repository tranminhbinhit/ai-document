---
inclusion: auto
---

# MCP Servers Usage Guide

## Filesystem MCP - Đọc Tài Liệu

### Mục đích
- Phân tích tài liệu nghiệp vụ (PDF, DOCX, XLSX)
- Đọc requirements, specs từ file
- Extract thông tin từ documents

### Tools Available
- `list_directory`: List files trong thư mục
- `read_text_file`: Đọc file text thông thường
- `parse_pdf`: Extract text từ PDF
- `parse_docx`: Extract text từ Word documents
- `parse_xlsx`: Extract data từ Excel spreadsheets

### Use Cases
1. **Phân tích requirements document**
   ```
   Hãy đọc file requirements.pdf trong thư mục docs và tóm tắt các yêu cầu chính
   ```

2. **Đọc business specifications**
   ```
   Parse file business-spec.docx và liệt kê các user stories
   ```

3. **Analyze data từ Excel**
   ```
   Đọc file data-model.xlsx và mô tả cấu trúc bảng
   ```

## GitLab MCP - Source Code & CI/CD

### Mục đích
- Browse và analyze source code
- Review Merge Requests
- Kiểm tra pipeline status
- Search code trong repository

### Tools Available
- `list_merge_requests`: Liệt kê MRs
- `get_merge_request`: Chi tiết một MR
- `get_mr_changes`: Xem code changes
- `list_pipelines`: Xem CI/CD pipelines
- `get_file_content`: Đọc file từ repo
- `search_code`: Search code

### Use Cases
1. **Review Merge Request**
   ```
   Xem MR #123 và phân tích code changes, suggest improvements
   ```

2. **Check pipeline status**
   ```
   Kiểm tra status của pipelines đang chạy
   ```

3. **Search và analyze code**
   ```
   Tìm tất cả các file có implement interface IUserService
   ```

## SQL Server MCP - Database

### Mục đích
- Hiểu database schema
- Query data để phân tích
- Investigate data-related issues
- Read-only mode để đảm bảo an toàn

### Tools Available
- `list_tables`: Liệt kê tất cả tables
- `describe_table`: Xem cấu trúc table
- `get_table_relationships`: Xem foreign keys
- `query_readonly`: Execute SELECT queries
- `get_table_sample`: Lấy sample data

### Use Cases
1. **Understand schema**
   ```
   Mô tả cấu trúc của bảng Users và các relationships
   ```

2. **Data analysis**
   ```
   Query 10 orders mới nhất và phân tích pattern
   ```

3. **Debug data issues**
   ```
   Kiểm tra xem có records nào bị duplicate trong bảng Customers không
   ```

## Best Practices

### Security
- SQL Server: Luôn dùng READ_ONLY mode
- Filesystem: Chỉ cho phép access vào thư mục được config
- GitLab: Store token trong environment variables, không commit

### Performance
- Limit số lượng rows khi query database
- PDF/Excel lớn có thể mất thời gian parse
- GitLab API có rate limits

### Workflow Examples

#### Investigate Bug từ Production
1. Check Kubernetes logs (future)
2. Query SQL Server để xem data state
3. Search code trong GitLab để tìm root cause
4. Review recent MRs có thể liên quan

#### Analyze New Feature Request
1. Parse requirement document (PDF/DOCX)
2. Check database schema (SQL Server)
3. Search existing code implementation (GitLab)
4. Suggest implementation approach

#### Code Review Support
1. Get MR details và changes
2. Check nếu có breaking changes với database schema
3. Verify business logic với requirements doc
4. Check pipeline status

## Environment Variables

Cần setup các biến môi trường sau:

```bash
# GitLab
export GITLAB_URL=https://gitlab.yourcompany.com
export GITLAB_TOKEN=your_token_here

# SQL Server
export SQL_SERVER=your-server.database.windows.net
export SQL_DATABASE=your_database
export SQL_USER=your_username
export SQL_PASSWORD=your_password

# Kubernetes (future)
export KUBECONFIG=~/.kube/config
```
