# Contributing to StockFlow

Thank you for your interest in contributing! This document provides guidelines for contributing to the StockFlow project.

## Code of Conduct

Be respectful and inclusive. We're building a welcoming community.

## How to Contribute

### Reporting Bugs

1. Check existing issues to avoid duplicates
2. Create a detailed issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Python version and environment

### Proposing Features

1. Open an issue with the `enhancement` label
2. Describe the use case and proposed solution
3. Wait for feedback before starting implementation

### Code Contributions

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes, then run: `make format && make lint && make test`
4. Ensure all tests pass: `pytest`
5. Push your branch and create a Pull Request

## Development Setup

```bash
make install-dev
pre-commit install
```

## Code Standards

- **Python**: 3.11+
- **Style**: Black formatting, line length 120
- **Imports**: Sorted with isort (black profile)
- **Linting**: Ruff for all violations
- **Tests**: Minimum 75% coverage
- **Type hints**: Encouraged (not required)

### Running Code Quality Tools

```bash
make format      # Auto-fix formatting
make lint        # Check code quality
make test        # Run tests with coverage
```

## Testing Guidelines

- Write tests for new features
- Unit tests in `tests/test_*.py`
- Mock external dependencies
- Aim for >75% coverage

Example:
```python
def test_create_product_success(client, app):
    with app.app_context():
        company, warehouse = create_company_with_warehouse()
    
    response = client.post("/api/products", json={...})
    assert response.status_code == 201
```

## Database Changes

1. Never commit direct schema changes
2. Use Alembic migrations: `flask db migrate -m "description"`
3. Review migration files before commit
4. Test migrations: `flask db upgrade && flask db downgrade`

## Commit Messages

```
<type>: <short description>

<longer explanation if needed>

Fixes #123
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

Example:
```
feat: add product bundle support

- Create ProductBundle model with self-referencing relationships
- Add validation to prevent circular bundles
- Update inventory calculations for bundles

Fixes #45
```

## PR Checklist

- [ ] Code passes `make lint`
- [ ] Code passes `make format`
- [ ] All tests pass: `pytest`
- [ ] Coverage maintained/improved
- [ ] Documentation updated
- [ ] No hardcoded secrets or credentials

## Questions?

Open an issue labeled `question` or contact the maintainers.
