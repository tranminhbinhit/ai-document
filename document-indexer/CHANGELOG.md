# Changelog

## [1.0.1] - 2026-06-14

### Changed
- **Đổi từ pyodbc sang pymssql** để đơn giản hóa deployment
  - Không cần cài ODBC Driver phức tạp
  - Build Docker image nhanh hơn và nhẹ hơn
  - Dễ dàng chạy trên nhiều platform

### Technical Details
- **Before**: `pyodbc` + Microsoft ODBC Driver 18
  - Cần cài đặt system packages phức tạp
  - Docker image size lớn (~500MB)
  - Build time lâu (2-3 phút)

- **After**: `pymssql` + FreeTDS
  - Chỉ cần FreeTDS libraries (có sẵn trong apt)
  - Docker image size nhỏ (~250MB)
  - Build time nhanh (30 giây)

### Migration
Nếu đang dùng version cũ:
1. Backup database: `docker exec document-indexer-db ...`
2. Stop containers: `docker-compose down`
3. Pull changes: `git pull`
4. Rebuild: `docker-compose build`
5. Start: `docker-compose up -d`

Không cần thay đổi code hoặc database schema.

## [1.0.0] - 2026-06-14

### Added
- Initial release
- Document watching và auto-indexing
- Support PDF, DOCX, XLSX, TXT, MD
- Docker deployment
- SQL Server integration
- MCP server compatibility
