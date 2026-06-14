# Project Structure

## 📁 Cấu trúc thư mục

```
kiro-mcp-servers/
│
├── .env                          # ⚙️ Environment variables (credentials)
├── .env.example                  # 📝 Template cho .env
├── .gitignore                    # 🚫 Git ignore rules
│
├── README.md                     # 📖 Project overview
├── PLAN.md                       # 🗺️ Roadmap & timeline
├── SETUP.md                      # 🚀 Setup guide chi tiết
└── PROJECT_STRUCTURE.md          # 📁 This file
│
├── .kiro/                        # 🎯 Kiro configuration
│   ├── settings/
│   │   ├── mcp.json              # MCP servers config
│   │   └── README.md             # Settings documentation
│   │
│   └── steering/                 # 📚 Usage guides & rules
│       ├── mcp-usage-guide.md    # How to use MCPs
│       └── gitlab-code-review.md # Review guidelines
│
└── mcp-servers/                  # 🔧 Custom MCP implementations
    ├── README.md                 # Why this folder exists
    │
    ├── filesystem/               # 📄 Document reader
    │   ├── server.py
    │   ├── requirements.txt
    │   └── __init__.py
    │
    ├── gitlab/                   # 🔧 GitLab integration
    │   ├── server.py
    │   └── requirements.txt
    │
    ├── sqlserver/                # 🗄️ Database queries
    │   ├── server.py
    │   └── requirements.txt
    │
    └── kubernetes/               # ☸️ K8s monitoring
        ├── server.py
        └── requirements.txt
```

## 📝 File Descriptions

### Root Level

#### Configuration Files
- **`.env`** - Credentials & sensitive config (NOT committed to git)
- **`.env.example`** - Template showing required environment variables
- **`.gitignore`** - Ensures `.env` and sensitive files aren't committed

#### Documentation
- **`README.md`** - Quick start guide, features overview
- **`PLAN.md`** - Complete roadmap, workflows, implementation details
- **`SETUP.md`** - Step-by-step installation instructions
- **`PROJECT_STRUCTURE.md`** - This file explaining project layout

### `.kiro/` - Kiro Configuration

#### `.kiro/settings/`
- **`mcp.json`** - Defines 4 MCP servers and how to run them
  - Command to execute
  - Arguments
  - Environment variables mapping
  - Auto-approve tools
  
- **`README.md`** - Explains settings structure

#### `.kiro/steering/`
Auto-loaded guides that provide context to Kiro:

- **`mcp-usage-guide.md`** - How to use each MCP server, use cases, examples
- **`gitlab-code-review.md`** - Code review checklist, best practices

### `mcp-servers/` - Custom Implementations

**Why this folder?** These are custom MCP servers, not pre-built packages.

Each server folder contains:
- **`server.py`** - MCP server implementation
  - Tool definitions
  - Request handlers
  - Business logic
  
- **`requirements.txt`** - Python dependencies

- **`README.md`** (in parent) - Explains custom vs pre-built MCP servers

#### Filesystem Server
- Parses PDF, DOCX, XLSX documents
- Lists directories
- Reads text files
- Used for: Requirements analysis, specs reading

#### GitLab Server  
- Integrates with GitLab API
- Lists & analyzes Merge Requests
- Browses source code
- Checks pipeline status
- Used for: Code review, CI/CD monitoring

#### SQL Server
- Connects to SQL Server (read-only)
- Describes database schema
- Executes SELECT queries
- Shows table relationships
- Used for: Data analysis, debugging

#### Kubernetes Server
- Monitors K8s clusters
- Gets pod logs
- Lists deployments
- Shows events
- Used for: Production debugging, incident response

## 🔄 How It Works

```
1. User asks Kiro something
   ↓
2. Kiro checks if MCP tools can help
   ↓
3. Kiro reads .kiro/settings/mcp.json
   ↓
4. Executes: python mcp-servers/[server]/server.py
   ↓
5. Server loads credentials from .env (via ${env:VAR})
   ↓
6. Server exposes tools to Kiro
   ↓
7. Kiro calls appropriate tool with parameters
   ↓
8. Server returns result
   ↓
9. Kiro uses result to answer user
```

## 🎯 Key Design Decisions

### Why `.env` at root?
✅ **Standard convention** - Most projects have `.env` at root  
✅ **Clear separation** - Config files vs settings  
✅ **Easy to find** - Developers expect it there  
✅ **Tool support** - Most tools look for `.env` at root  

### Why separate `mcp-servers/` folder?
✅ **Custom implementations** - Not using pre-built packages  
✅ **Modifiable** - Can add features, fix bugs  
✅ **Company-specific** - Tailored to your workflow  
✅ **Clear ownership** - Your team maintains this code  

### Why `.kiro/steering/`?
✅ **Auto-loaded** - Provides context automatically  
✅ **Guidelines** - Best practices always available  
✅ **Versioned** - Guidelines evolve with project  

### Why separate each server?
✅ **Independence** - Each can be developed separately  
✅ **Dependencies** - Different libraries per server  
✅ **Testing** - Can test individually  
✅ **Deployment** - Can enable/disable individually  

## 🔐 Security

### Protected Files (in .gitignore)
- `.env` - Contains tokens, passwords, connection strings
- `__pycache__/` - Python bytecode
- `.vscode/`, `.idea/` - IDE settings

### Safe to Commit
- `.env.example` - Template only, no real credentials
- All `.py` files - Source code
- `requirements.txt` - Dependency lists
- `mcp.json` - Uses `${env:VAR}` references, not actual values

## 🚀 Getting Started

1. **Clone** repository
2. **Copy** `.env.example` to `.env`
3. **Edit** `.env` with your credentials
4. **Install** dependencies: `pip install -r mcp-servers/*/requirements.txt`
5. **Restart** Kiro
6. **Test** by asking Kiro to use MCP tools

## 📚 Reading Order

New to project? Read in this order:
1. `README.md` - Overview
2. `SETUP.md` - Get it running
3. `PROJECT_STRUCTURE.md` - Understand layout (this file)
4. `PLAN.md` - Deep dive into design
5. `.kiro/steering/*.md` - Learn usage patterns

## 🛠️ Development

### Adding a New MCP Server

1. Create folder: `mcp-servers/newserver/`
2. Add `server.py` with MCP implementation
3. Add `requirements.txt` with dependencies
4. Update `.kiro/settings/mcp.json`:
   ```json
   {
     "newserver": {
       "command": "python",
       "args": ["${workspaceFolder}/mcp-servers/newserver/server.py"],
       "env": {...}
     }
   }
   ```
5. Add steering guide: `.kiro/steering/newserver-guide.md`
6. Update documentation

### Modifying Existing Server

1. Edit `mcp-servers/[server]/server.py`
2. Test standalone: `python mcp-servers/[server]/server.py`
3. Restart Kiro → "MCP: Reconnect Servers"
4. Test in Kiro chat

## 🤝 Contributing

- Keep `.env.example` updated with new variables
- Document new tools in steering guides
- Test servers standalone before committing
- Update this structure doc when adding folders

---

**Last Updated:** 2026-06-06  
**Version:** 1.0
