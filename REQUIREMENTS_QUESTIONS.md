# Câu hỏi làm rõ yêu cầu dự án

## 1. MCP Server
**Q1.1:** MCP trong dự án này là gì? 
- [ x] Model Context Protocol server để AI agents truy cập tài liệu
- [ ] Một microservice riêng biệt
- [ ] Tích hợp vào .NET API
- [ ] Khác (ghi rõ): _______________

**Q1.2:** Chức năng chính của MCP?
- Trả lời: có thể tôi chưa hiểu rõ, project này chạy hoàn toàn trên docker . mcp ở đây để các repo khác khi sử dụng có thể kết nối để đọc tài liệu. kiểu như dựng mcp đến server 

## 2. Document Processing

**Q2.1:** Định dạng tài liệu cần hỗ trợ?
- [ x] PDF
- [ x] DOCX / DOC
- [x ] TXT
- [ x] XLSX / XLS
- [x ] PPT / PPTX
- [ x] HTML
- [x ] Markdown
- [ ] Khác: _______________

**Q2.2:** Kích thước file tối đa cho phép?
- [ ] 10MB
- [ ] 50MB
- [ ] 100MB
- [ x] Không giới hạn
- [ ] Khác: _______________

**Q2.3:** Xử lý tài liệu như thế nào?
- [ ] Đồng bộ (upload xong xử lý luôn)
- [ x] Bất đồng bộ (queue background job)

## 3. RAG & AI Configuration

**Q3.1:** OpenAI API key đã có chưa?
- [ x] Có sẵn
- [ ] Cần đăng ký
- [ ] Dùng Azure OpenAI
- [ ] Dùng model khác: _______________

**Q3.2:** Embedding model nào?
- [ x] text-embedding-3-small (OpenAI)
- [ ] text-embedding-3-large (OpenAI)
- [ ] text-embedding-ada-002 (OpenAI)
- [ ] Khác: chu

**Q3.3:** Chat model nào?
- [ ] gpt-4o
- [ x] gpt-4o-mini
- [ ] gpt-4-turbo
- [ ] gpt-3.5-turbo
- [ ] Khác: _______________

**Q3.4:** Chunk size cho tài liệu?
- [ x] 500 tokens
- [ ] 1000 tokens
- [ ] 2000 tokens
- [ ] Khác: _______________

**Q3.5:** Số chunks retrieve cho mỗi câu hỏi?
- [x ] 3
- [ ] 5
- [ ] 10
- [ ] Khác: _______________

## 4. Database & Storage

**Q4.1:** SQL Server đã có sẵn chưa?
- [ ] Có sẵn (connection string): _______________
- [ ] Cần setup local
- [ ] Dùng Azure SQL
- [ ] Dùng SQL Express
- Chưa có tạo mới trong docker compose. Dự án này tất cả tạo trong docker compose

**Q4.2:** Lưu trữ file ở đâu?
- [ ] Local disk (đường dẫn): _______________
- [ ] Azure Blob Storage
- [ ] AWS S3
- [ ] Khác: tạo 1 docker storage để lưu trữ

**Q4.3:** Vector Database - Qdrant?
- [ ] Self-hosted local
- [ ] Qdrant Cloud
- [x ] Docker container
- [ ] Khác: _______________

## 5. Security & Authentication

**Q5.1:** Có cần authentication không?
- [ x] Không cần (public access)
- [ ] Cần đăng nhập cơ bản
- [ ] OAuth / Azure AD
- [ ] Khác: _______________

**Q5.2:** Có cần phân quyền theo user không?
- [x ] Không
- [ ] Có (admin vs user)
- [ ] Khác: _______________

**Q5.3:** Rate limiting cho OpenAI?
- [ x] Không giới hạn
- [ ] X requests/minute: _______________
- [ ] Dựa vào quota OpenAI

## 6. Frontend Requirements

**Q6.1:** Category dropdown - tạo mới category:
- Khi chọn option "Tạo mới", hiển thị:
- [ ] Modal popup nhập tên category
- [ x] Inline input field
- [ ] Navigate to trang quản lý category
- [ ] Khác: _______________

**Q6.2:** Danh sách tài liệu - số items mỗi trang?
- [ ] 10
- [ x] 20
- [ ] 50
- [ ] Khác: _______________

**Q6.3:** Chat interface cần hiển thị:
- [x ] Chỉ câu hỏi/trả lời
- [ x] Hiển thị sources (documents được tham chiếu)
- [ x] Hiển thị confidence score
- [ ] Chat history
- [ ] Khác: _______________

## 7. Development Environment

**Q7.1:** Môi trường phát triển?
- [ ] Windows
- [ ] macOS
- [ ] Linux
- [ x] Docker containers

**Q7.2:** .NET version?
- [ ] .NET 6
- [ ] .NET 7
- [ ] .NET 8
- [ x] .NET 9

**Q7.3:** Python version?
- [ ] Python 3.9
- [ ] Python 3.10
- [ ] Python 3.11
- [ x] Python 3.12

**Q7.4:** Angular version?
- [ ] Angular 15
- [ ] Angular 16
- [ ] Angular 17
- [ x] Angular 19

**Q7.5:** Node.js version?
- [ ] Node 18 LTS
- [ ] Node 20 LTS
- [ x] Node 22
- [ ] Khác: _______________

## 8. Deployment

**Q8.1:** Deployment target?
- [ ] Local development only
- [ ] On-premise server
- [ ] Azure
- [ ] AWS
- [x ] Docker compose
- [ ] Kubernetes
- [ ] Khác: _______________

**Q8.2:** Có cần CI/CD không?
- [ x] Không
- [ ] GitHub Actions
- [ ] Azure DevOps
- [ ] Khác: _______________

## 9. Additional Features

**Q9.1:** Có cần search/filter trong danh sách tài liệu?
- [x ] Có - search by title
- [ ] Có - filter by date
- [ ] Có - full text search
- [ ] Không

**Q9.2:** Có cần xóa/sửa tài liệu đã upload?
- [ x] Có
- [ ] Không

**Q9.3:** Có cần export chat history?
- [ x] Có
- [ ] Không

**Q9.4:** Có cần analytics/logging?
- [ ] Có - track user queries
- [ ] Có - track document usage
- [x ] Không

## 10. Priority & Timeline

**Q10.1:** Thứ tự ưu tiên tính năng?
1. _______________
2. _______________
3. _______________

**Q10.2:** Timeline dự kiến?
- [ ] 1-2 tuần (MVP)
- [ x] 1 tháng (full features)
- [ ] 2-3 tháng (production-ready)
- [ ] Khác: _______________

**Q10.3:** Bắt đầu với prototype đơn giản trước?
- [ ] Có - chỉ chat + 1 document test
- [ x] Không - làm full ngay

---

## Ghi chú thêm
(Bất kỳ requirements hoặc constraints nào khác):
thực hiện toàn bộ ở đây. gồm project angular, ... 
tạo 1 docker-compose để deploy tất cả 
ngoài trang hỏi đáp này. chúng ta có thêm mcp mà các repo khác có thể kết nối và sủ dụng. hay vì dùng filesystem mcp trên kiro hay dùng

