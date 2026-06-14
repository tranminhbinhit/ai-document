document-indexer

├── watcher.py        # theo dõi folder
├── processor.py      # xử lý file
├── database.py       # làm việc với DB
└── config.py         # cấu hình

pip install watchdog

py watcher.py

Cấu hình thư mục
WATCH_FOLDER = r"D:\DOC-MCP"

Cấu hình database

CREATE TABLE Documents
(
    Id INT IDENTITY PRIMARY KEY,

    FileName NVARCHAR(255),

    Path NVARCHAR(500),

    Summary NVARCHAR(MAX),

    Keywords NVARCHAR(MAX),

    IsDelete BOOLEN,

    CreatedDate DATETIME
)



database.py
Nó không xử lý AI, không đọc PDF. Nhiệm vụ của nó chỉ là:

mở connection SQL Server
insert tài liệu mới
update tài liệu
kiểm tra file đã index chưa
tìm kiếm metadata

Tách riêng để sau này đổi SQL Server → PostgreSQL → SQLite không phải sửa toàn bộ code.