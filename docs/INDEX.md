# Documentation Index

Complete documentation for Document RAG System.

## 🚀 Getting Started

**New to the project? Start here:**

1. **[QUICK_START.md](../QUICK_START.md)** - 5-minute setup guide
2. **[README.md](../README.md)** - Project overview and features
3. **[SETUP_GUIDE.md](../SETUP_GUIDE.md)** - Detailed installation guide

## 📚 Core Documentation

### Project Information
- **[README.md](../README.md)** - Project overview, features, architecture
- **[PLAN.md](../PLAN.md)** - Original project requirements
- **[REQUIREMENTS_QUESTIONS.md](../REQUIREMENTS_QUESTIONS.md)** - Requirements clarification
- **[FINAL_SUMMARY.md](../FINAL_SUMMARY.md)** - Project completion summary

### Technical Documentation
- **[IMPLEMENTATION_PLAN.md](../IMPLEMENTATION_PLAN.md)** - Detailed technical architecture
- **[RAG_FLOW_DETAIL.md](../RAG_FLOW_DETAIL.md)** - How RAG works (with examples)
- **[PROJECT_STATUS.md](../PROJECT_STATUS.md)** - Implementation status and progress

### Setup & Deployment
- **[SETUP_GUIDE.md](../SETUP_GUIDE.md)** - Complete setup instructions
- **[QUICK_START.md](../QUICK_START.md)** - Quick 5-minute start
- **[DEPLOYMENT.md](../DEPLOYMENT.md)** - Production deployment guide

### Development
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - How to contribute
- **[CHANGELOG.md](../CHANGELOG.md)** - Version history and changes

### Component-Specific
- **[MCP Server README](../mcp-server/README.md)** - MCP server documentation

## 📖 Documentation by Topic

### Architecture & Design

**Understanding the System:**
- Architecture Overview → [IMPLEMENTATION_PLAN.md](../IMPLEMENTATION_PLAN.md#architecture-overview)
- Database Schema → [IMPLEMENTATION_PLAN.md](../IMPLEMENTATION_PLAN.md#database-schema)
- RAG Pipeline → [RAG_FLOW_DETAIL.md](../RAG_FLOW_DETAIL.md)
- Docker Services → [README.md](../README.md#architecture)

### Installation & Setup

**Getting Started:**
- Quick Start (5 min) → [QUICK_START.md](../QUICK_START.md)
- Full Setup Guide → [SETUP_GUIDE.md](../SETUP_GUIDE.md)
- Prerequisites → [README.md](../README.md#quick-start)
- Environment Config → [SETUP_GUIDE.md](../SETUP_GUIDE.md#step-2-clone-and-setup)

### Usage & Features

**How to Use:**
- Upload Documents → [QUICK_START.md](../QUICK_START.md#1-upload-a-document)
- Chat with AI → [QUICK_START.md](../QUICK_START.md#3-ask-a-question)
- Manage Categories → [README.md](../README.md#api-endpoints)
- Export Chat History → [RAG_FLOW_DETAIL.md](../RAG_FLOW_DETAIL.md)
- MCP Tools → [mcp-server/README.md](../mcp-server/README.md#mcp-tools)

### Development

**For Developers:**
- Project Structure → [IMPLEMENTATION_PLAN.md](../IMPLEMENTATION_PLAN.md#project-structure)
- Backend Development → [CONTRIBUTING.md](../CONTRIBUTING.md#1-backend-changes)
- Frontend Development → [CONTRIBUTING.md](../CONTRIBUTING.md#2-frontend-changes)
- Python Indexer → [CONTRIBUTING.md](../CONTRIBUTING.md#3-python-indexer-changes)
- Code Style → [CONTRIBUTING.md](../CONTRIBUTING.md#code-style)

### Deployment

**Production Deployment:**
- Docker Compose → [DEPLOYMENT.md](../DEPLOYMENT.md#option-1-docker-compose-recommended-for-single-server)
- Kubernetes → [DEPLOYMENT.md](../DEPLOYMENT.md#option-2-kubernetes)
- Cloud Providers → [DEPLOYMENT.md](../DEPLOYMENT.md#option-3-cloud-specific)
- Security → [DEPLOYMENT.md](../DEPLOYMENT.md#security-hardening)
- Monitoring → [DEPLOYMENT.md](../DEPLOYMENT.md#monitoring--logging)

### Troubleshooting

**Common Issues:**
- System Check → [QUICK_START.md](../QUICK_START.md#-verify-installation)
- Troubleshooting → [QUICK_START.md](../QUICK_START.md#-troubleshooting)
- Error Resolution → [SETUP_GUIDE.md](../SETUP_GUIDE.md#troubleshooting)
- Logs → [DEPLOYMENT.md](../DEPLOYMENT.md#troubleshooting)

## 🎯 Quick Reference

### Commands

```bash
# Start services
make start                # or docker-compose up -d

# Check status
make status               # or docker-compose ps

# View logs
make logs                 # or docker-compose logs -f

# Stop services
make stop                 # or docker-compose down

# Health check
bash check-system.sh

# Clean up
make clean                # or docker-compose down -v
```

### URLs

- Frontend: http://localhost:4200
- Backend API: http://localhost:5000
- Swagger: http://localhost:5000/swagger
- Qdrant: http://localhost:6333/dashboard
- MCP Server: http://localhost:3000

### Environment Variables

```env
SQL_SA_PASSWORD=YourStrong@Passw0rd123
OPENAI_API_KEY=sk-your-openai-api-key
```

### File Structure

```
/
├── backend/              # .NET 9 API
├── frontend/             # Angular 19 app
├── indexer/              # Python worker
├── mcp-server/           # MCP server
├── scripts/              # Helper scripts
└── docs/                 # Documentation
```

## 📋 Documentation Checklist

### For New Users
- [ ] Read QUICK_START.md
- [ ] Setup environment
- [ ] Start services
- [ ] Upload test document
- [ ] Try chat feature

### For Developers
- [ ] Read IMPLEMENTATION_PLAN.md
- [ ] Review code structure
- [ ] Setup development environment
- [ ] Read CONTRIBUTING.md
- [ ] Make first contribution

### For DevOps
- [ ] Review DEPLOYMENT.md
- [ ] Setup production environment
- [ ] Configure monitoring
- [ ] Setup backups
- [ ] Test disaster recovery

## 🔍 Search Tips

**Looking for:**
- **Setup help** → QUICK_START.md or SETUP_GUIDE.md
- **How it works** → RAG_FLOW_DETAIL.md
- **API docs** → http://localhost:5000/swagger
- **Deployment** → DEPLOYMENT.md
- **Contributing** → CONTRIBUTING.md
- **Troubleshooting** → Any doc's troubleshooting section

## 📞 Getting Help

1. **Check documentation** in this order:
   - QUICK_START.md
   - README.md
   - SETUP_GUIDE.md
   - Specific topic docs

2. **Run diagnostics**:
   ```bash
   bash check-system.sh
   docker-compose logs <service>
   ```

3. **Check existing issues** on GitHub

4. **Create new issue** with:
   - Clear description
   - Steps to reproduce
   - Logs
   - Environment info

## 🆕 What's New

See [CHANGELOG.md](../CHANGELOG.md) for version history and changes.

## 📝 Contributing to Docs

Documentation improvements are welcome! See [CONTRIBUTING.md](../CONTRIBUTING.md#documentation).

**How to contribute:**
1. Fork repository
2. Make changes
3. Test your changes
4. Submit pull request

**Documentation standards:**
- Clear and concise
- Step-by-step instructions
- Code examples
- Screenshots when helpful
- Keep index updated

## 🎓 Learning Path

**Beginner:**
1. QUICK_START.md → Get it running
2. README.md → Understand features
3. Try uploading documents
4. Experiment with chat

**Intermediate:**
1. RAG_FLOW_DETAIL.md → Understand RAG
2. IMPLEMENTATION_PLAN.md → Learn architecture
3. Explore API with Swagger
4. Check Qdrant dashboard

**Advanced:**
1. DEPLOYMENT.md → Production setup
2. CONTRIBUTING.md → Contribute code
3. Customize for your needs
4. Scale the system

---

**Last Updated**: 2024-01-01

**Documentation Version**: 1.0.0

**Need help?** Check the docs, run health check, or open an issue!
