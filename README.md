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

1. Create virtual environment and install dependencies:
```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

2. Configure database connection:
```bash
set DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/stockflow
```

3. Run migrations (after initializing migration environment):
```bash
set FLASK_APP=run.py
flask db init
flask db migrate -m "initial schema"
flask db upgrade
```

4. Start server:
```bash
python run.py
```

## Seed Sample Data

```bash
set FLASK_APP=run.py
flask seed-data
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
