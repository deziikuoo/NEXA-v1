# Contributing to NEXA Game Recommender

Thank you for your interest in contributing to NEXA! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

We welcome contributions from the community! Here are several ways you can help:

### 🐛 Report Bugs
- Use the [GitHub Issues](https://github.com/deziikuoo/NEXA-v1/issues) page
- Include a clear description of the bug
- Provide steps to reproduce the issue
- Include your system information (OS, browser, etc.)

### 💡 Suggest Features
- Use the [GitHub Issues](https://github.com/deziikuoo/NEXA-v1/issues) page
- Describe the feature you'd like to see
- Explain why this feature would be useful
- Consider implementation details if possible

### 🔧 Submit Code Changes
- Fork the repository
- Create a feature branch
- Make your changes
- Test thoroughly
- Submit a pull request

## 🛠️ Development Setup

### Prerequisites
- Python 3.9+
- Node.js 16+
- Git

### Local Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/NEXA-v1.git
   cd NEXA-v1
   ```

2. **Set up the backend:**
   ```bash
   pip install -r requirements.txt
   python setup_env.py  # Interactive setup for API keys
   # Or manually: cp .env.example .env and edit with your API keys
   ```

3. **Set up the frontend:**
   ```bash
   npm install
   ```

4. **Start development servers:**
   ```bash
   npm run start
   ```

5. **🌐 Live Demo**: [https://nexa-pro.up.railway.app](https://nexa-pro.up.railway.app)

## 📝 Code Style Guidelines

### Python (Backend)
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and single-purpose

### JavaScript/React (Frontend)
- Use consistent indentation (2 spaces)
- Follow ESLint configuration
- Use meaningful variable and function names
- Write comments for complex logic

### General Guidelines
- Write clear, descriptive commit messages
- Keep changes focused and atomic
- Test your changes thoroughly
- Update documentation when necessary

## 🧪 Testing

### Backend Testing
```bash
# Run Python tests
python -m pytest

# Run with coverage
python -m pytest --cov=app_fastapi
```

### Frontend Testing
```bash
# Run React tests
npm test

# Run tests with coverage
npm test -- --coverage
```

### Manual Testing
- Test on different browsers (Chrome, Firefox, Safari, Edge)
- Test on mobile devices
- Verify API endpoints work correctly
- Check for responsive design issues

## 📋 Pull Request Process

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Write clean, well-documented code
   - Add tests for new functionality
   - Update documentation if needed

3. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

4. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request:**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Select the main branch as the target
   - Fill out the PR template

### Pull Request Template

```markdown
## Description
Brief description of the changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement

## Testing
- [ ] Backend tests pass
- [ ] Frontend tests pass
- [ ] Manual testing completed
- [ ] Cross-browser testing completed

## Screenshots (if applicable)
Add screenshots for UI changes.

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes introduced
```

## 🏷️ Issue Labels

We use the following labels to categorize issues:

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements or additions to documentation
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `question` - Further information is requested

## 🚀 Release Process

1. **Version bump** in `package.json` and `app_fastapi.py`
2. **Update CHANGELOG.md** with new features and fixes
3. **Create a release tag** on GitHub
4. **Deploy to production** (Railway)

## 📞 Getting Help

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For general questions and discussions
- **Email**: IfDawanPrintQualified14@gmail.com for private matters

## 🎯 Areas for Contribution

### High Priority
- Performance optimizations
- Security improvements
- Better error handling
- Enhanced API documentation

### Medium Priority
- Additional game data sources
- UI/UX improvements
- Mobile app development
- Advanced filtering options

### Low Priority
- Code refactoring
- Documentation improvements
- Test coverage expansion
- Internationalization

## 📜 Code of Conduct

### Our Standards
- Be respectful and inclusive
- Use welcoming and inclusive language
- Be collaborative and constructive
- Focus on what is best for the community

### Enforcement
- Unacceptable behavior will not be tolerated
- Violations may result in temporary or permanent ban
- Report violations to maintainers

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

Thank you for contributing to NEXA! 🎮 