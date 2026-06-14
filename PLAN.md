# Plan Xây Dựng MCP Servers cho Kiro

## Mục Tiêu

Biến Kiro thành trợ lý kỹ thuật toàn diện cho workflow: **Angular + GitLab + Jenkins + Harbor + Kubernetes + SQL Server**

## Timeline & Priority

### Phase 1: Foundation (Tuần 1-2) ⭐⭐⭐ PRIORITY
**MCP 1: Filesystem - Đọc Tài Liệu**

**Mục tiêu:**
- Đọc và phân tích tài liệu nghiệp vụ (PDF, DOCX, XLSX)
- Extract requirements, specs
- Hỗ trợ hiểu context của dự án

**Tools:**
- `list_directory` - Browse thư mục documents
- `read_text_file` - Đọc file text
- `parse_pdf` - Extract text từ PDF
- `parse_docx` - Extract text từ Word
- `parse_xlsx` - Extract data từ Excel

**Use Cases:**
1. "Đọc requirements.pdf và tóm tắt các yêu cầu chính"
2. "Parse design document và extract user stories"
3. "Phân tích data model từ file Excel"

**Implementation:**
- ✅ Python-based server
- ✅ PyPDF2 cho PDF
- ✅ python-docx cho Word
- ✅ openpyxl cho Excel
- ✅ Security: Chỉ cho phép access thư mục được config

**Testing:**
- Đọc sample PDF về requirements
- Parse DOCX business spec
- Extract data từ Excel schema definition

---

### Phase 2: Development (Tuần 2-3) ⭐⭐⭐ PRIORITY
**MCP 2: GitLab - Source Code & CI/CD**

**Mục tiêu:**
- Browse và analyze source code
- Review Merge Requests tự động
- Monitor pipeline status
- Search code hiệu quả

**Tools:**
- `list_merge_requests` - List MRs
- `get_merge_request` - Chi tiết MR
- `get_mr_changes` - Xem code diff
- `list_pipelines` - Pipeline status
- `get_file_content` - Đọc file từ repo
- `search_code` - Search trong codebase

**Use Cases:**
1. "Review MR #123 và suggest improvements"
2. "Tìm tất cả các file implement IUserService"
3. "Check pipeline của branch feature/user-management"
4. "Analyze code changes trong MR liên quan đến authentication"

**Implementation:**
- ✅ Python với python-gitlab library
- ✅ GitLab API integration
- ✅ Token-based authentication
- ✅ Rate limiting handling

**Testing:**
- List recent MRs
- Get và analyze một MR cụ thể
- Search code patterns
- Check pipeline status

**Steering Rules:**
- Code review guidelines
- Common issues checklist
- Security review points

---

### Phase 3: Data Layer (Tuần 3-4) ⭐⭐ MEDIUM PRIORITY
**MCP 3: SQL Server - Database**

**Mục tiêu:**
- Hiểu database schema
- Query data để analysis và debug
- Read-only mode để đảm bảo an toàn
- Support data investigation

**Tools:**
- `list_tables` - Liệt kê tables
- `describe_table` - Schema của table
- `get_table_relationships` - Foreign keys
- `query_readonly` - SELECT queries only
- `get_table_sample` - Sample data

**Use Cases:**
1. "Describe schema của bảng Users và relationships"
2. "Query 10 orders mới nhất và phân tích pattern"
3. "Kiểm tra xem có duplicate records trong Customers không"
4. "Explain data model của module Payment"

**Implementation:**
- ✅ Python với pyodbc
- ✅ ODBC Driver 17 for SQL Server
- ✅ READ_ONLY connection mode
- ✅ Query validation (chỉ SELECT)
- ✅ Row limit để tránh quá tải

**Security:**
- Chỉ cho phép SELECT queries
- Automatic TOP clause
- Connection với READ_ONLY flag
- Separate DB user với minimal permissions (recommended)

**Testing:**
- List tables
- Describe complex table
- Query với joins
- Verify read-only enforcement

---

### Phase 4: Operations (Tuần 5-6) ⭐ FUTURE
**MCP 4: Kubernetes - Monitoring & Debug**

**Mục tiêu:**
- Monitor production/staging environments
- Debug pod issues
- Analyze logs
- Support incident investigation

**Tools:**
- `list_pods` - List pods trong namespace
- `get_pod_logs` - Xem logs
- `describe_pod` - Pod details
- `list_deployments` - Deployment status
- `get_deployment` - Deployment details
- `list_services` - Services
- `get_events` - K8s events

**Use Cases:**
1. "Check logs của api-service pod trong production"
2. "List tất cả pods đang crash trong staging"
3. "Analyze events để debug deployment issue"
4. "Xem resource usage của deployment user-api"

**Implementation:**
- ✅ Python với kubernetes client
- ✅ Kubeconfig-based auth
- ✅ Read-only operations
- ✅ Namespace filtering

**Security:**
- Chỉ read operations (logs, describe, list)
- No delete/update/create
- Namespace-based access control
- Kubeconfig với RBAC

**Testing:**
- List pods trong namespace
- Get logs từ running pod
- Describe deployment
- Get events để debug

---

## Tích Hợp & Workflows

### Workflow 1: Investigate Production Bug
```
1. User: "API endpoint /users/login đang lỗi 500"

2. Kiro:
   - Check K8s logs của api pods (Kubernetes MCP)
   - Query database để xem data state (SQL Server MCP)
   - Search code implementation (GitLab MCP)
   - Check recent MRs có thể liên quan (GitLab MCP)
   
3. Output: Root cause analysis + suggested fix
```

### Workflow 2: Analyze New Feature Request
```
1. User: "Implement tính năng user profile trong file spec.pdf"

2. Kiro:
   - Parse requirements document (Filesystem MCP)
   - Check current database schema (SQL Server MCP)
   - Search existing related code (GitLab MCP)
   - Suggest implementation approach
   
3. Output: Implementation plan + DB changes needed
```

### Workflow 3: Code Review Automation
```
1. User: "Review MR #456"

2. Kiro:
   - Get MR details và changes (GitLab MCP)
   - Check DB schema impact (SQL Server MCP)
   - Verify business logic với requirements (Filesystem MCP)
   - Check pipeline status (GitLab MCP)
   
3. Output: Comprehensive review comments
```

### Workflow 4: Incident Response
```
1. Alert: "High CPU in production"

2. Kiro:
   - Check pod status và logs (Kubernetes MCP)
   - Query database cho slow queries (SQL Server MCP)
   - Correlate với recent deployments (GitLab MCP)
   
3. Output: Incident timeline + remediation steps
```

---

## Steering Rules Created

### 1. `mcp-usage-guide.md`
- Hướng dẫn sử dụng từng MCP
- Use cases cụ thể
- Best practices
- Environment variables setup

### 2. `gitlab-code-review.md`
- Code review checklist
- Common issues to look for
- Angular-specific checks
- SQL Server best practices
- Security considerations

### 3. Future Steering Rules
- `incident-investigation.md` - SOP cho incident response
- `feature-implementation.md` - Workflow implement feature mới
- `database-migration.md` - Guidelines cho DB changes
- `k8s-debugging.md` - K8s troubleshooting guide

---

## Installation & Setup

### Prerequisites
```bash
# Python 3.8+
python --version

# pip hoặc uv
pip install uv

# MCP SDK
pip install mcp
```

### Quick Start
```bash
# 1. Clone/setup project
git clone <your-repo>

# 2. Install dependencies cho từng MCP
cd mcp-servers/filesystem && pip install -r requirements.txt
cd mcp-servers/gitlab && pip install -r requirements.txt
cd mcp-servers/sqlserver && pip install -r requirements.txt
cd mcp-servers/kubernetes && pip install -r requirements.txt

# 3. Setup environment variables (xem .env.example)
cp .env.example .env
# Edit .env với credentials của bạn

# 4. Configure Kiro
# File .kiro/settings/mcp.json đã được tạo sẵn
# Chỉnh sửa paths và credentials nếu cần

# 5. Restart Kiro
# Command Palette → "MCP: Reconnect Servers"
```

### Detailed Setup
Xem file `SETUP.md` cho hướng dẫn chi tiết.

---

## Testing Plan

### Unit Tests
- Mỗi MCP server có test suite riêng
- Mock external dependencies (GitLab API, SQL Server, K8s API)
- Test error handling

### Integration Tests
```bash
# Test Filesystem MCP
python -m pytest tests/test_filesystem.py

# Test GitLab MCP
python -m pytest tests/test_gitlab.py

# Test SQL Server MCP
python -m pytest tests/test_sqlserver.py

# Test Kubernetes MCP
python -m pytest tests/test_kubernetes.py
```

### End-to-End Tests
- Test workflows trong Kiro
- Verify MCP tools hoạt động đúng
- Test error scenarios

---

## Monitoring & Maintenance

### Logs
- Mỗi MCP server log ra stdout
- Kiro Output panel → "Kiro MCP"
- Monitor errors và performance

### Performance
- GitLab API: Rate limiting (10 req/sec)
- SQL Server: Row limits (default 100)
- K8s: Namespace filtering
- Filesystem: Directory whitelist

### Security Checklist
- [ ] GitLab token không commit vào Git
- [ ] SQL Server ở READ_ONLY mode
- [ ] K8s chỉ có read permissions
- [ ] Filesystem chỉ access allowed directories
- [ ] Credentials trong environment variables
- [ ] Regular token rotation

---

## Future Enhancements

### Phase 5: CI/CD Integration
- **Jenkins MCP**: Build status, job logs
- **Harbor MCP**: Container images, vulnerabilities

### Phase 6: Communication
- **Slack MCP**: Notifications, status updates
- **Email MCP**: Send reports, alerts

### Phase 7: Intelligence
- AI-powered code suggestions
- Automatic bug pattern detection
- Performance optimization recommendations
- Security vulnerability scanning

### Phase 8: Team Features
- Code review assignments
- Knowledge base từ past MRs
- Team metrics và analytics

---

## Success Metrics

### Developer Productivity
- Time to review MR: -50%
- Time to debug production issue: -60%
- Time to understand new feature: -40%

### Code Quality
- Bug detection rate: +30%
- Security issues found: +40%
- Code review thoroughness: +50%

### Knowledge Transfer
- New team member onboarding: -70% time
- Documentation completeness: +80%
- Cross-team collaboration: +40%

---

## Risks & Mitigations

### Risk 1: API Rate Limits
**Mitigation:**
- Implement caching
- Request batching
- Retry with exponential backoff

### Risk 2: Security Concerns
**Mitigation:**
- READ_ONLY modes
- Least privilege access
- Audit logging
- Regular security reviews

### Risk 3: Performance Issues
**Mitigation:**
- Query limits
- Timeout configurations
- Connection pooling
- Resource monitoring

### Risk 4: Credential Management
**Mitigation:**
- Environment variables
- Secret management system
- Token rotation
- No commits to repo

---

## Deliverables Checklist

Phase 1 - Filesystem MCP:
- [x] Server implementation
- [x] Requirements file
- [x] MCP config
- [ ] Tests
- [ ] Documentation

Phase 2 - GitLab MCP:
- [x] Server implementation
- [x] Requirements file
- [x] MCP config
- [x] Steering rules
- [ ] Tests

Phase 3 - SQL Server MCP:
- [x] Server implementation
- [x] Requirements file
- [x] MCP config
- [ ] Tests
- [ ] Documentation

Phase 4 - Kubernetes MCP:
- [x] Server implementation
- [x] Requirements file
- [x] MCP config (disabled by default)
- [ ] Tests
- [ ] Documentation

General:
- [x] Setup guide
- [x] .env.example
- [x] Overall plan
- [ ] Demo video
- [ ] Training materials

---

## Next Actions

### Immediate (This Week)
1. ✅ Create all MCP server implementations
2. ✅ Setup MCP configuration
3. ✅ Create steering rules
4. Setup environment variables
5. Test Filesystem MCP
6. Test GitLab MCP

### Short-term (Next 2 Weeks)
1. Complete SQL Server MCP testing
2. Write unit tests
3. Create demo workflows
4. Document common use cases
5. Train team on usage

### Long-term (Next Month)
1. Enable Kubernetes MCP
2. Optimize performance
3. Add more steering rules
4. Collect feedback
5. Plan Phase 5 (Jenkins/Harbor)

---

## Support & Resources

### Documentation
- `SETUP.md` - Installation guide
- `README.md` - Project overview
- `.kiro/steering/` - Usage guides
- This `PLAN.md` - Roadmap

### External Links
- [MCP Documentation](https://modelcontextprotocol.io/)
- [python-gitlab](https://python-gitlab.readthedocs.io/)
- [pyodbc](https://github.com/mkleehammer/pyodbc)
- [Kubernetes Python Client](https://github.com/kubernetes-client/python)

### Getting Help
- Check logs in Kiro Output panel
- Test servers standalone
- Review error messages
- Check this documentation

---

**Created:** 2026-06-06  
**Last Updated:** 2026-06-06  
**Version:** 1.0
