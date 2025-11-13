# Contributing to GOAT v2.1

Thank you for your interest in contributing to GOAT! We welcome contributions from the community.

## 🌟 How to Contribute

### Reporting Bugs

1. Check existing issues to avoid duplicates
2. Use the bug report template
3. Include:
   - Clear description of the issue
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Docker version, etc.)
   - Relevant logs or screenshots

### Suggesting Features

1. Check existing feature requests
2. Open a new issue with the "enhancement" label
3. Describe:
   - The problem you're trying to solve
   - Your proposed solution
   - Alternative solutions considered
   - Additional context

### Pull Request Process

#### 1. Fork & Clone

```bash
git clone https://github.com/YOUR_USERNAME/GOAT.git
cd GOAT
git remote add upstream https://github.com/Spruked/GOAT.git
```

#### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

#### 3. Make Your Changes

- Follow the existing code style
- Add tests for new functionality
- Update documentation as needed
- Keep commits focused and atomic

#### 4. Test Your Changes

**Backend:**
```bash
# Run tests
pytest

# Check linting
flake8 .
black --check .
```

**Frontend:**
```bash
cd frontend
npm run lint
npm run build
```

**Docker:**
```bash
docker-compose up --build
```

#### 5. Commit Your Changes

Use clear, descriptive commit messages:

```bash
git commit -m "feat: add skill prerequisite validation"
git commit -m "fix: resolve IPFS gateway timeout"
git commit -m "docs: update deployment guide"
```

Commit message format:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Formatting, missing semicolons, etc.
- `refactor:` Code restructuring
- `test:` Adding tests
- `chore:` Maintenance tasks

#### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title and description
- Reference to related issues
- Screenshots for UI changes
- Test results

## 📋 Development Guidelines

### Code Style

**Python (Backend):**
- Follow PEP 8
- Use `black` for formatting
- Use `flake8` for linting
- Type hints encouraged
- Docstrings for all public functions

**JavaScript (Frontend):**
- ESLint configuration provided
- Use functional components with hooks
- Prop types or TypeScript preferred
- Consistent naming conventions

### Architecture Principles

1. **Separation of Concerns**: Keep modules focused
2. **Security First**: Validate all inputs, use encryption properly
3. **Async/Await**: Use async patterns for I/O operations
4. **Error Handling**: Graceful error handling with user feedback
5. **Documentation**: Comment complex logic

### Testing

- Write unit tests for new functions
- Integration tests for API endpoints
- E2E tests for critical user flows
- Maintain test coverage above 70%

## 🎯 Areas for Contribution

### High Priority
- [ ] OpenAI/Anthropic LLM integration for quiz generation
- [ ] Advanced knowledge graph visualizations
- [ ] Smart contract deployment scripts
- [ ] Production deployment templates

### Medium Priority
- [ ] Additional blockchain network support (Ethereum, Base, etc.)
- [ ] Plugin system for custom data sources
- [ ] Advanced analytics dashboard
- [ ] Mobile-responsive UI improvements

### Good First Issues
- [ ] Documentation improvements
- [ ] UI/UX enhancements
- [ ] Test coverage expansion
- [ ] Code refactoring

## 🔒 Security

If you discover a security vulnerability:
1. **DO NOT** open a public issue
2. Email the maintainers directly
3. Include details to reproduce the issue
4. Allow time for a fix before public disclosure

## 📖 Resources

- [README.md](README.md) - Project overview
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [BUILD_SUMMARY.md](BUILD_SUMMARY.md) - Technical details
- [QUICK_START.md](QUICK_START.md) - Quick reference

## 💬 Community

- **GitHub Discussions**: For questions and ideas
- **GitHub Issues**: For bugs and feature requests
- **Pull Requests**: For code contributions

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make GOAT better! 🐐
