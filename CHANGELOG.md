# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-15

### Added
- Initial project setup with Flask app factory pattern
- SQLAlchemy ORM models for multi-warehouse inventory management
- Product creation endpoint with input validation and atomic transactions
- Low-stock alerts API with sales activity filtering
- Comprehensive database schema with constraints and indexes
- Inventory audit logging via InventoryLog model
- Product bundle support (self-referencing relationships)
- Pre-commit hooks for code quality
- CI/CD pipeline with GitHub Actions
- Unit tests with pytest and coverage reporting
- Development tooling: black, ruff, isort, mypy
- Docker support with Dockerfile and docker-compose
- Makefile for convenient development commands

### Fixed
- Product creation endpoint issues:
  - No input validation
  - Race condition on SKU uniqueness
  - Transaction boundaries (two commits)
  - Missing inventory log
  - No proper HTTP status codes
  - No error handling

### Documentation
- Complete README with setup instructions
- API endpoint specifications with examples
- Database design rationale
- Contribution guidelines
- Architecture and design decisions

---

## Unreleased

### Planned Features
- API authentication and authorization
- Supplier order management
- Inventory forecasting
- Barcode/QR code support
- Multi-tenancy enhancements
- Advanced reporting and analytics
