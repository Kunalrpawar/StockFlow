from app.extensions import db
from app.models.company import Company
from app.models.product import Product
from app.models.warehouse import Warehouse


def create_company_with_warehouse():
    company = Company(name="Test Co")
    db.session.add(company)
    db.session.flush()

    warehouse = Warehouse(company_id=company.id, name="Test WH")
    db.session.add(warehouse)
    db.session.commit()
    return company, warehouse


def test_create_product_success(client, app):
    with app.app_context():
        company, warehouse = create_company_with_warehouse()

    response = client.post(
        "/api/products",
        json={
            "name": "Widget A",
            "sku": "SKU-100",
            "price": "49.95",
            "company_id": company.id,
            "warehouse_id": warehouse.id,
            "initial_quantity": 10,
            "low_stock_threshold": 20,
        },
    )

    assert response.status_code == 201
    body = response.get_json()
    assert body["message"] == "Product created"


def test_create_product_duplicate_sku(client, app):
    with app.app_context():
        company, warehouse = create_company_with_warehouse()
        existing = Product(
            company_id=company.id,
            name="Existing Product",
            sku="SKU-DUP",
            price=10,
            product_type="standard",
        )
        db.session.add(existing)
        db.session.commit()

    response = client.post(
        "/api/products",
        json={
            "name": "Another",
            "sku": "SKU-DUP",
            "price": "12.00",
            "company_id": company.id,
            "warehouse_id": warehouse.id,
        },
    )

    assert response.status_code == 400
    assert "SKU already exists" in response.get_json()["error"]
