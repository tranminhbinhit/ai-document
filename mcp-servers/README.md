# MCP Servers - Custom Implementation

## 📁 Tại sao cần thư mục này?

**Đây là source code cho custom MCP servers**, không phải pre-built packages.

### 2 loại MCP servers:

#### 1. Pre-built (như `uvx mcp-server-github`)
```json
{
  "command": "uvx",
  "args": ["mcp-server-github"]
}
```
✅ Không cần source code  
✅ Chỉ cần command trong `mcp.json`

#### 2. Custom (như servers này)
```json
{
  "command": "python",
  "args": ["${workspaceFolder}/mcp-servers/filesystem/server.py"]
}
```
✅ Cần source code để chạy  
✅ Có thể customize cho company  
✅ Add features theo nhu cầu

## 🏗️ Cấu trúc

```
mcp-servers/
├── filesystem/
│   ├── server.py          # Logic đọc PDF/DOCX/XLSX
│   └── requirements.txt   # Dependencies
├── gitlab/
│   ├── server.py          # Logic tích hợp GitLab
│   └── requirements.txt
├── sqlserver/
│   ├── server.py          # Logic query SQL Server
│   └── requirements.txt
└── kubernetes/
    ├── server.py          # Logic monitor K8s
    └── requirements.txt
```

## 🔄 Workflow

1. **Kiro đọc** `.kiro/settings/mcp.json`
2. **Execute** `python mcp-servers/filesystem/server.py`
3. **Server chạy** và expose tools
4. **Kiro gọi tools** khi cần

## 🛠️ Khi nào cần modify?

- Thêm tools mới (vd: parse XML)
- Fix bugs
- Optimize performance
- Add company-specific logic
- Change behavior

## 📦 Installation

Mỗi server cần install dependencies:

```bash
# Filesystem
cd mcp-servers/filesystem
pip install -r requirements.txt

# GitLab
cd ../gitlab
pip install -r requirements.txt

# SQL Server
cd ../sqlserver
pip install -r requirements.txt

# Kubernetes
cd ../kubernetes
pip install -r requirements.txt
```

## 🧪 Testing

Test từng server standalone:

```bash
python mcp-servers/filesystem/server.py
python mcp-servers/gitlab/server.py
python mcp-servers/sqlserver/server.py
python mcp-servers/kubernetes/server.py
```

## 🔐 Security

- Credentials trong `.kiro/settings/.env`, không hardcode
- SQL Server: READ_ONLY mode
- Kubernetes: Chỉ read operations
- Filesystem: Directory whitelist

## 📝 Adding New Tools

Ví dụ thêm tool vào Filesystem MCP:

```python
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        # ... existing tools ...
        Tool(
            name="parse_xml",
            description="Parse XML file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                }
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any):
    if name == "parse_xml":
        return await handle_parse_xml(arguments)
    # ... existing handlers ...
```

## 📚 Dependencies

### Common
- `mcp>=0.9.0` - MCP SDK

### Filesystem
- `PyPDF2` - PDF parsing
- `python-docx` - Word documents
- `openpyxl` - Excel spreadsheets

### GitLab
- `python-gitlab` - GitLab API client

### SQL Server
- `pyodbc` - SQL Server driver
- Requires: ODBC Driver 17 for SQL Server

### Kubernetes
- `kubernetes` - K8s Python client

## 🚀 Future Servers

Có thể thêm:
- `jenkins/` - CI/CD monitoring
- `harbor/` - Container registry
- `slack/` - Notifications
- `email/` - Reports

Mỗi server là 1 folder với `server.py` + `requirements.txt`
