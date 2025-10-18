# Contributing to Chinook Service

Thank you for your interest in contributing to Chinook Service! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Code Style](#code-style)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project adheres to the Contributor Covenant Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment (see below)
4. Create a new branch for your changes
5. Make your changes
6. Submit a pull request

## Development Setup

This project uses [uv](https://github.com/astral-sh/uv) for dependency management. Follow these steps to set up your development environment:

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/servicetest.git
cd servicetest

# Create a virtual environment with uv
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install all dependencies including dev tools
uv sync --all-groups
```

## Making Changes

1. Create a new branch from `main`:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the code style guidelines
3. Add or update tests as needed
4. Ensure all tests pass
5. Commit your changes with clear, descriptive commit messages

## Code Style

This project uses the following tools to maintain code quality:

- **Ruff** - Fast Python linter and formatter
- **mypy** - Static type checker
- **markdownlint** - Markdown linter

Before submitting a pull request, run the following commands:

```bash
# Format code with Ruff
ruff format .

# Lint code with Ruff
ruff check .

# Type check with mypy
mypy src/

# Run tests
pytest
```

### Code Guidelines

- Follow PEP 8 style guidelines
- Use type hints for all function signatures
- Write docstrings for all public functions and classes
- Keep functions focused and concise
- Avoid deep nesting (max 3-4 levels)
- Use meaningful variable and function names

## Testing

All new features and bug fixes should include tests:

- Write unit tests using `pytest`
- Aim for high test coverage (>80%)
- Test both success and failure scenarios
- Use mocks for external dependencies

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src/chinook_service --cov-report=html
```

## Pull Request Process

1. Update the README.md or documentation if needed
2. Update CHANGELOG.md with your changes under the "Unreleased" section
3. Ensure all CI checks pass (linting, type checking, tests)
4. Request review from maintainers
5. Address any feedback from reviewers
6. Once approved, a maintainer will merge your PR

### Pull Request Guidelines

- Keep PRs focused on a single feature or fix
- Write a clear description of what the PR does
- Reference any related issues
- Include screenshots for UI changes (if applicable)
- Update documentation as needed

## Questions?

If you have questions or need help, feel free to:

- Open an issue for discussion
- Reach out to the maintainers
- Check existing issues and pull requests

Thank you for contributing!

