Mục tiêu dự án
Dựng hệ thống gồm
- Database sql server
   + Lưu trữ thông tin tài liệu
- Trang web Angular không authen author (Gồm menu có 3 trang)
   + Trang Có 1 khung chat hỏi và Ai trả lời các thông tin đọc từ database , file trong hệ thống có được
   + Upload tài liệu lưu lên storage, python dọc và lưu thông tin tài liệu vào database, lưu file vào dish (Gồm button upload, Dropdownlist chọn chủ đề, trong dropdownlist có 1 option tạo dropdown list mới)
   + Danh sách tài liệu theo category (Chọn category để hiển thị tài liệu có phân trang)
- MCP kết nối và lưu trữ, đọc tài liệu

Kiến trúc dự kiến 
 Angular
   |
Backend API
   |
RAG Service
   |
+----------------+
|                |
LLM API       Vector DB
(OpenAI...)   (Qdrant...)
|
SQL Server + Storage


Kiến trúc 
Angular
.NET API
Python Indexer
Qdrant
OpenAI API
SQL Server


