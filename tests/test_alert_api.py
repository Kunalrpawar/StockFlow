from datetime import datetime, timedelta

from app.extensions import db
from app.models.company import Company
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.product_supplier import ProductSupplier
from app.models.sales_record import SalesRecord
from app.models.supplier import Supplier
from app.models.warehouse import Warehouse


def setup_alert_fixture():
    company = Company(name="Alert Co")
    db.session.add(company)
    db.session.flush()

    warehouse = Warehouse(company_id=company.id, name="Main")
    db.session.add(warehouse)
    db.session.flush()

    supplier = Supplier(company_id=company.id, name="Supplier One", contact_email="buy@supplier.com")
    db.session.add(supplier)
    db.session.flush()

    product = Product(
        company_id=company.id,
        name="Widget Alert",
        sku="ALT-001",
        price=20,
        product_type="standard",
        low_stock_threshold=10,
    )
    db.session.add(product)
    db.session.flush()

    db.session.add(ProductSupplier(product_id=product.id, supplier_id=supplier.id, is_primary=True))
    db.session.add(Inventory(product_id=product.id, warehouse_id=warehouse.id, quantity=3))
    db.session.add(
        SalesRecord(
            company_id=company.id,
            product_id=product.id,
            warehouse_id=warehouse.id,
            quantity=30,
            sold_at=datetime.utcnow() - timedelta(days=3),
        )
    )
    db.session.commit()
    return company


def test_low_stock_alerts(client, app):
    with app.app_context():
        company = setup_alert_fixture()

    response = client.get(f"/api/companies/{company.id}/alerts/low-stock")

    assert response.status_code == 200
    body = response.get_json()
    assert body["total_alerts"] == 1
    assert body["alerts"][0]["supplier"]["name"] == "Supplier One"
