# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub compliance documentation (LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md)
- Code quality tools configuration (Ruff, mypy, markdownlint)
- GitHub Actions CI/CD workflows
- PyPI-standard src-layout directory structure
- UV package manager configuration
- Enhanced README with badges and table of contents

### Changed
- Migrated to src-layout structure (`src/chinook_service/`)
- Updated all dependencies to latest compatible versions
- Replaced requirements.txt with pyproject.toml configuration
- Updated Dockerfile to use UV package manager
- Enhanced SECURITY.md with correct version information

### Removed
- requirements.txt (replaced by pyproject.toml)

## [0.1.0] - 2025-01-01

### Added
- Initial Flask RESTful API for Chinook database
- Employee management endpoints (list, create, get by ID)
- Tracks read-only endpoint
- Stock quote integration with Yahoo Finance
- SQLite database integration with SQLAlchemy
- Basic request validation and error handling
- Docker containerization support
- Unit test suite with pytest
- Basic documentation (README.md, SECURITY.md)

### Security
- SQL injection protection via SQLAlchemy parameter binding
- Input validation for employee payloads
- Graceful error handling for external API dependencies
