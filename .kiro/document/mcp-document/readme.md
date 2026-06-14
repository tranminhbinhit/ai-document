Nâng câp MCP filesystem
                Kiro

                  |

      +-----------+-----------+

      |                       |

Filesystem MCP         SQL MCP

      |                       |

Documents         Document Index

Hiện có Filesystem MCP 
Kế hoạch 30 ngày
Tuần 1

Hoàn thiện Filesystem MCP.

Đọc được:

PDF
DOCX
XLSX
MD
TXT
Tuần 2

Xây bảng:

Document

Lưu:

FileName
Path
Summary
Keywords
Tuần 3

Viết tool:

index_document()

Tự động:

File mới
↓
Đọc
↓
Tóm tắt
↓
Lưu SQL
Tuần 4

Tạo MCP mới:

document-search-mcp

Có tool:

search_documents()
get_document_summary()

Lúc đó bạn sẽ có một hệ thống rất thực dụng:

20.000 tài liệu
↓
SQL Index
↓
Kiro tìm đúng tài liệu
↓
Filesystem MCP đọc nội dung chi tiết




Cách 1 - Thủ công

Bạn bỏ file:

D:\DOC-MCP

new-policy.pdf

Sau đó hỏi:

Hãy index tài liệu mới

AI:

read_file()

↓

summary

↓

keywords

↓

insert SQL

Ưu điểm:

Dễ làm

Nhược điểm:

Quên chạy
Cách 2 - Tự động (nên dùng)

Bạn có thư mục:

D:\DOC-MCP

Viết service nhỏ bằng Python.

Theo dõi folder:

watch folder

Khi có file mới:

new-policy.pdf

thì tự động:

1. đọc file

2. sinh summary

3. sinh keywords

4. lưu SQL

5. đánh dấu indexed

Luồng:

Copy file

↓

Folder Watcher

↓

Parse PDF

↓

Summary

↓

SQL Server

Document Table

Không cần mở Kiro.

Không cần prompt.

Kiến trúc mình khuyên
D:/DOC-MCP

      |

Folder Watcher

      |

Document Processor

      |

+-------------------+

| Parse PDF/DOCX    |

| Summary           |

| Keywords          |

+-------------------+

      |

SQL Server

Document Index



Thông tin database 
| Id | FileName | Path | Summary | Keywords | CreatedDate |
| -- | -------- | ---- | ------- | -------- | ----------- |
| 1 | keycloak.pdf | D:/DOC-MCP/keycloak.pdf | Hướng dẫn Keycloak | keycloak, oauth2, token | ... |