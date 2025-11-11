# Contributing to Post-Conversation Analysis

Thank you for your interest in contributing! Here's how you can help.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/post-conversation-analysis.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Set up development environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   ```

## Development Workflow

1. Make your changes in a feature branch
2. Test your changes:
   ```bash
   python test_api.py
   python manage.py test
   ```
3. Commit with descriptive messages:
   ```bash
   git commit -m "Add feature: description of what you added"
   ```
4. Push your branch: `git push origin feature/your-feature-name`
5. Open a Pull Request with a clear description

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small

## Testing

- Add tests for new features
- Ensure all tests pass before submitting PR
- Test API endpoints with `test_api.py`

## Reporting Bugs

1. Check existing issues first
2. Create a new issue with:
   - Clear title describing the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)

## Feature Requests

1. Open an issue with the label `enhancement`
2. Describe the feature and use case
3. Explain the expected behavior

## Questions?

Open an issue or start a discussion. We're here to help!

Thank you for contributing! 🎉
