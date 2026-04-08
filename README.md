# StockFlow - Inventory Management System (B2B SaaS)

Production-style Flask backend case study covering:
1. Debugging and fixing a broken product creation API.
2. Database schema design for multi-warehouse inventory.
3. Low-stock alert API implementation with supplier and sales-aware logic.

## Tech Stack
- Python 3.11+
- Flask
- SQLAlchemy
- PostgreSQL
- Flask-Migrate (Alembic)
- Pytest

## Project Structure

```
stockflow/
  app/
    models/
    routes/
    services/
    utils/
    __init__.py
    extensions.py
    seed.py
  config/
    settings.py
  migrations/
  tests/
  run.py
  requirements.txt
  README.md
```

## Setup

### Quick Start (5 minutes)

```bash
# 1. Activate venv
.venv\Scripts\activate

# 2. Initialize database
python manage.py init

# 3. Seed sample data
python manage.py seed

# 4. Start server
python run.py
```

Then visit:
- **API Docs**: http://localhost:5000/
- **Health Check**: http://localhost:5000/health

### Quick Start (Mac/Linux)

```bash
source .venv/bin/activate
python manage.py init
python manage.py seed
python run.py
```

### Development Setup with Pre-commit Hooks

```bash
# Install development dependencies
pip install -e ".[dev]"

# Setup pre-commit hooks
pre-commit install

# Now automatic code quality checks run on every commit
```

### Full Setup (Alternative with Alembic migrations)

```bash
# Configure PostgreSQL connection
set DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/stockflow

# Initialize Alembic migrations
set FLASK_APP=run.py
flask db init
flask db migrate -m "initial schema"
flask db upgrade
```

## Database Management

Quick database commands without PostgreSQL (uses SQLite):

```bash
python manage.py init    # Create database tables
python manage.py seed    # Load sample data
python manage.py reset   # Drop and recreate all tables
```

With Flask CLI (requires Alembic setup):

```bash
set FLASK_APP=run.py
flask db init            # Initialize migration environment
flask db migrate -m "description"  # Create migration
flask db upgrade         # Apply migrations
flask seed-data          # Load sample data
```

## API Endpoints Reference

### Base URL
```
http://localhost:5000
```

### Root API Documentation
- **GET** `/` - Returns API structure and endpoint documentation

### Health Check
- **GET** `/health` - Service health status

## Code Quality & Development

All commands available via `make` (or run manually):

```bash
make lint       # Check code quality (ruff, black)
make format     # Auto-format code (black, isort, ruff)
make test       # Run tests with coverage report
make clean      # Remove build artifacts and cache
make help       # Show all available commands
```

### Pre-commit Hooks

Pre-commit hooks automatically format and check code before commits:

```bash
git commit -m "your message"  # Hooks run automatically
```

Hooks configured:
- Trailing whitespace removal
- File format fixes (json, yaml)
- Large file detection
- Black formatting
- Ruff linting with auto-fix
- isort import sorting
- Type checking with mypy

### Code Standards

- **Formatter**: Black (line length 120)
- **Linter**: Ruff + flake8
- **Import sorter**: isort (black profile)
- **Type checker**: mypy
- **Test coverage**: Minimum 75%

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Docker Deployment

### Build and Run with Docker Compose

```bash
docker-compose up -d
docker-compose exec app flask db upgrade
docker-compose exec app flask seed-data
```

Application available at `http://localhost:5000`

### Manual Docker Build

```bash
docker build -t stockflow .
docker run -p 5000:5000 -e DATABASE_URL=<db_url> stockflow
```

### Production Deployment

The Dockerfile uses gunicorn with 4 workers. For production:

1. Update `docker-compose.yml` with your PostgreSQL credentials
2. Set proper environment variables
3. Use a reverse proxy (nginx) in front of gunicorn
4. Enable HTTPS/TLS
5. Set up monitoring and logging

## Project Structure Reference

- **app/** - Application code (models, routes, services, utils)
- **app/models/** - SQLAlchemy ORM definitions
- **app/routes/** - Flask blueprints for API endpoints
- **app/services/** - Business logic and database operations
- **app/utils/** - Validation, error handling, response formatting
- **config/** - Configuration management
- **tests/** - Pytest test suite
- **migrations/** - Alembic database migration scripts
- **.github/workflows/** - GitHub Actions CI/CD pipelines
- **Makefile** - Development command shortcuts
- **pyproject.toml** - Python project configuration and tool settings
- **.pre-commit-config.yaml** - Pre-commit hook configuration
- **.editorconfig** - Editor formatting standards
- **docker-compose.yml** - Docker multi-container setup
- **Dockerfile** - Container image definition
- **.gitignore** - Version control exclusions
- **.env.example** - Environment variables template
- **CONTRIBUTING.md** - Contribution guidelines
- **CHANGELOG.md** - Release history and changes
- **LICENSE** - MIT License

## Testing the API

### Manual curl commands

```bash
# Get API documentation
curl http://localhost:5000/

# Health check
curl http://localhost:5000/health

# Create product
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Widget A",
    "sku": "WID-001",
    "price": "19.99",
    "company_id": 1,
    "warehouse_id": 1,
    "initial_quantity": 10,
    "low_stock_threshold": 20
  }'

# Get low-stock alerts
curl http://localhost:5000/api/companies/1/alerts/low-stock
```

Or use:
```bash
python test_api.py  # Displays all test commands
```

### Run automated tests

```bash
pytest -v            # Verbose output
pytest --cov=app     # With coverage report
make test            # Using Makefile
```

## API Endpoints

### Health
- `GET /health`

### Create Product (fixed version)
- `POST /api/products`

Example payload:
```json
{
  "name": "Widget A",
  "sku": "WID-001",
  "price": "19.99",
  "company_id": 1,
  "warehouse_id": 1,
  "initial_quantity": 10,
  "product_type": "standard",
  "low_stock_threshold": 20
}
```

### Low Stock Alerts
- `GET /api/companies/<company_id>/alerts/low-stock`

Response shape:
```json
{
  "alerts": [
    {
      "product_id": 123,
      "product_name": "Widget A",
      "sku": "WID-001",
      "warehouse_id": 456,
      "warehouse_name": "Main Warehouse",
      "current_stock": 5,
      "threshold": 20,
      "days_until_stockout": 12,
      "supplier": {
        "id": 789,
        "name": "Supplier Corp",
        "contact_email": "orders@supplier.com"
      }
    }
  ],
  "total_alerts": 1
}
```

## Part 1: Broken API Analysis

### Issues in original code
1. No input validation, causing runtime exceptions or bad data.
2. Two commits in one request create partial writes on failure.
3. No transaction boundary around product + inventory creation.
4. Product had warehouse coupling, which breaks multi-warehouse design.
5. No handling for SKU uniqueness race/integrity errors.
6. Price and quantity types were not validated.
7. No company-level ownership validation for warehouse.
8. No inventory log for auditability.
9. No explicit HTTP status codes and error responses.

### Fix summary
- Added request validation in `app/utils/validators.py`.
- Moved business logic to service layer in `app/services/product_service.py`.
- Added atomic transaction behavior via flush + single commit.
- Added error handling for validation, integrity, and unexpected failures.
- Added inventory log entry on product creation.

## Part 2: Database Design

### Entities implemented
- `Company`
- `Warehouse`
- `Product`
- `Inventory` (Product x Warehouse)
- `Supplier`
- `ProductSupplier`
- `InventoryLog`
- `ProductBundle` (self-referencing)
- `SalesRecord` (added to support low-stock activity and stockout calculations)

### Design decisions
- Global unique SKU enforced at DB level.
- `Inventory` has unique (`product_id`, `warehouse_id`) to prevent duplicates.
- Check constraints prevent negative quantity/price and invalid bundle links.
- Composite indexes support common filtering paths for alerts and reporting.
- Inventory changes are append-only in `InventoryLog` for audit trail.

### Requirement gaps / questions for product team
1. Should SKU uniqueness be global or company-scoped?
2. Can one product have multiple primary suppliers per region?
3. Should bundles deduct component inventory automatically at sale time?
4. Should alerts consider transferable stock across warehouses?
5. What is the exact fallback when threshold is null?
6. Should inactive products still produce alerts?
7. How should backorders and negative stock be modeled?
8. Is sales activity based on orders placed or fulfilled shipments?

## Part 3: Low-Stock Alert Logic

Implemented in `app/services/alert_service.py` with rules:
1. Product inventory must be below threshold.
2. Product must have sales activity in last 30 days.
3. Handles per-warehouse inventory rows for a company.
4. Includes primary supplier if available.
5. Computes `days_until_stockout` from 30-day average daily sales.

Edge-case handling:
- Returns 404 for missing company.
- `days_until_stockout` is null when daily sales is zero.
- Supplier is null if no primary supplier mapping exists.

## Tests

Run:
```bash
pytest -q
```

Included tests:
- Product creation success
- Duplicate SKU rejection
- Low-stock alert response generation

## Notes for Live Discussion
- Atomic transaction strategy and rollback behavior.
- Why inventory is modeled separately from products for multi-warehouse support.
- Tradeoffs in threshold fallback and supplier prioritization.
- Index choices for low-stock query performance.

## Good Coding Practices Included

This repository demonstrates production-level best practices:

### Version Control
- Comprehensive `.gitignore` for Python/Flask projects
- Clean commit history with conventional commit messages

### Project Configuration
- **pyproject.toml** - Centralized tool configuration (black, ruff, pytest, coverage)
- **Makefile** - Convenient development commands
- **.editorconfig** - Consistent formatting across editors
- **.env.example** - Environment variable template

### Code Quality
- **Pre-commit hooks** - Automatic linting, formatting, and validation
- **Black** - Opinionated code formatting
- **Ruff** - Fast Python linter with auto-fix
- **isort** - Import statement organization
- **mypy** - Static type checking
- **Pytest** - Testing framework with coverage

### CI/CD
- **GitHub Actions** - Automated testing and linting on push/PR
- **Multi-version testing** - Tests run on Python 3.11 and 3.12
- **Code coverage** - Integrated Codecov reporting

### Containerization
- **Dockerfile** - Production-ready container image
- **docker-compose.yml** - Local development with PostgreSQL
- **.dockerignore** - Optimized image build

### Documentation
- **README.md** - Comprehensive setup and API documentation
- **CONTRIBUTING.md** - Guidelines for contributors
- **CHANGELOG.md** - Release history and version tracking
- **LICENSE** - MIT License
- **Code comments** - Minimal but strategic comments

### Development Workflow
```bash
# One-command setup
make install-dev

# Automatic code quality
git commit  # Pre-commit hooks run automatically

# Local development
make run    # Start dev server

# Testing
make test   # Full test suite with coverage

# Production
docker-compose up  # Or deploy container elsewhere
```
