# Contributing to Document RAG System

Thank you for considering contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/document-rag-system.git
   cd document-rag-system
   ```
3. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Prerequisites
- Docker & Docker Compose
- Node.js 22 (for frontend development)
- .NET 9 SDK (for backend development)
- Python 3.12 (for indexer development)

### Local Development

```bash
# Start infrastructure only
docker-compose up -d sql-server qdrant redis

# Run backend locally
cd backend/DocumentRAG.API
dotnet run

# Run frontend locally
cd frontend
npm install
npm start

# Run indexer locally
cd indexer
pip install -r requirements.txt
python worker.py
```

## Code Style

### Backend (.NET)
- Follow C# coding conventions
- Use meaningful variable names
- Add XML documentation comments
- Keep methods focused and small

### Frontend (TypeScript)
- Follow Angular style guide
- Use TypeScript strict mode
- Add JSDoc comments for complex logic
- Keep components focused

### Python
- Follow PEP 8
- Use type hints
- Add docstrings
- Keep functions focused

## Project Structure

```
backend/
├── DocumentRAG.API/        # API controllers, services
├── DocumentRAG.Core/       # Domain entities
└── DocumentRAG.Infrastructure/  # Data access

frontend/
├── src/app/
│   ├── pages/              # Page components
│   ├── services/           # HTTP services
│   └── models/             # TypeScript interfaces

indexer/
├── processors/             # Document processors
├── worker.py              # Main worker
├── embedder.py            # Embedding generation
└── chunker.py             # Text chunking
```

## Making Changes

### 1. Backend Changes

```bash
cd backend/DocumentRAG.API

# Make changes

# Build
dotnet build

# Run tests (if available)
dotnet test

# Start locally
dotnet run
```

### 2. Frontend Changes

```bash
cd frontend

# Make changes

# Start dev server
npm start

# Build for production
npm run build
```

### 3. Python Indexer Changes

```bash
cd indexer

# Make changes

# Test locally
python worker.py
```

## Testing

### Manual Testing
1. Start all services with Docker Compose
2. Test upload flow
3. Test document processing
4. Test chat functionality
5. Verify MCP server

### API Testing
```bash
# Test with curl
curl http://localhost:5000/api/categories

# Or use Swagger
open http://localhost:5000/swagger
```

## Commit Guidelines

### Commit Message Format
```
type(scope): subject

body

footer
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation
- **style**: Code style changes
- **refactor**: Code refactoring
- **test**: Adding tests
- **chore**: Maintenance

### Examples
```
feat(backend): add document version tracking

Add versioning support for documents to track changes over time.

Closes #123
```

```
fix(frontend): correct pagination calculation

Fixed off-by-one error in pagination logic.
```

## Pull Request Process

1. **Update documentation** if needed
2. **Test your changes** thoroughly
3. **Update CHANGELOG.md** if applicable
4. **Create pull request** with:
   - Clear title and description
   - Reference to related issues
   - Screenshots for UI changes
5. **Wait for review**

### PR Checklist
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] Tests pass (if applicable)
- [ ] No console errors
- [ ] Commits are clean and meaningful

## Areas for Contribution

### High Priority
- [ ] Unit tests for backend
- [ ] Unit tests for frontend
- [ ] Integration tests
- [ ] E2E tests
- [ ] Performance optimization
- [ ] Error handling improvements

### Medium Priority
- [ ] Authentication system
- [ ] Rate limiting
- [ ] Caching layer
- [ ] Document versioning
- [ ] Advanced search
- [ ] Analytics dashboard

### Low Priority
- [ ] UI/UX improvements
- [ ] Additional document formats
- [ ] Internationalization
- [ ] Dark mode
- [ ] Mobile responsiveness

## Feature Requests

1. **Check existing issues** first
2. **Create new issue** with:
   - Clear title
   - Detailed description
   - Use case
   - Expected behavior
3. **Label appropriately**: enhancement, feature-request

## Bug Reports

Include:
1. **Description**: What happened?
2. **Steps to reproduce**
3. **Expected behavior**
4. **Actual behavior**
5. **Environment**:
   - OS
   - Docker version
   - Browser (for frontend)
6. **Logs** (if applicable)
7. **Screenshots** (if applicable)

### Bug Report Template
```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g. Ubuntu 22.04]
- Docker version: [e.g. 24.0.0]
- Browser: [e.g. Chrome 120]

**Logs**
```
Paste relevant logs here
```

**Additional context**
Any other context about the problem.
```

## Documentation

### When to Update Docs
- New features added
- API changes
- Configuration changes
- Deployment changes
- Breaking changes

### Documentation Files
- **README.md**: Overview, quick start
- **SETUP_GUIDE.md**: Detailed setup
- **DEPLOYMENT.md**: Production deployment
- **API docs**: Swagger/OpenAPI
- **Architecture docs**: IMPLEMENTATION_PLAN.md

## Code Review

### For Contributors
- Be open to feedback
- Respond to comments
- Make requested changes
- Ask questions if unclear

### For Reviewers
- Be constructive
- Explain reasoning
- Suggest alternatives
- Approve when ready

## Questions?

- Open an issue with label "question"
- Check existing documentation
- Review closed issues/PRs

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.

## Code of Conduct

- Be respectful
- Be inclusive
- Be collaborative
- Focus on constructive feedback
- Help others learn

## Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort! 🙏
