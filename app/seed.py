from datetime import datetime, timedelta
from decimal import Decimal

from app.extensions import db
from app.models.company import Company
from app.models.inventory import Inventory
from app.models.inventory_log import InventoryLog
from app.models.product import Product
from app.models.product_supplier import ProductSupplier
from app.models.sales_record import SalesRecord
from app.models.supplier import Supplier
from app.models.warehouse import Warehouse


def seed_sample_data() -> None:
    if Company.query.filter_by(name="Acme Retail").first() is not None:
        return

    company = Company(name="Acme Retail")
    db.session.add(company)
    db.session.flush()

    warehouse_main = Warehouse(company_id=company.id, name="Main Warehouse", location="Pune")
    warehouse_secondary = Warehouse(company_id=company.id, name="Overflow Warehouse", location="Mumbai")
    db.session.add_all([warehouse_main, warehouse_secondary])
    db.session.flush()

    supplier = Supplier(company_id=company.id, name="Supplier Corp", contact_email="orders@supplier.com")
    db.session.add(supplier)
    db.session.flush()

    product_a = Product(
        company_id=company.id,
        name="Widget A",
        sku="WID-001",
        product_type="standard",
        price=Decimal("19.99"),
        low_stock_threshold=20,
    )
    product_b = Product(
        company_id=company.id,
        name="Widget B",
        sku="WID-002",
        product_type="standard",
        price=Decimal("29.99"),
        low_stock_threshold=10,
    )
    db.session.add_all([product_a, product_b])
    db.session.flush()

    db.session.add_all(
        [
            ProductSupplier(product_id=product_a.id, supplier_id=supplier.id, is_primary=True, lead_time_days=4),
            ProductSupplier(product_id=product_b.id, supplier_id=supplier.id, is_primary=True, lead_time_days=7),
        ]
    )

    inv_a_main = Inventory(product_id=product_a.id, warehouse_id=warehouse_main.id, quantity=5)
    inv_a_secondary = Inventory(product_id=product_a.id, warehouse_id=warehouse_secondary.id, quantity=6)
    inv_b_main = Inventory(product_id=product_b.id, warehouse_id=warehouse_main.id, quantity=40)
    db.session.add_all([inv_a_main, inv_a_secondary, inv_b_main])
    db.session.flush()

    for inv in [inv_a_main, inv_a_secondary, inv_b_main]:
        db.session.add(
            InventoryLog(
                inventory_id=inv.id,
                product_id=inv.product_id,
                warehouse_id=inv.warehouse_id,
                change_type="initial_stock",
                quantity_delta=inv.quantity,
                quantity_before=0,
                quantity_after=inv.quantity,
                reason="Seed data",
            )
        )

    now = datetime.utcnow()
    db.session.add_all(
        [
            SalesRecord(
                company_id=company.id,
                product_id=product_a.id,
                warehouse_id=warehouse_main.id,
                quantity=15,
                sold_at=now - timedelta(days=5),
            ),
            SalesRecord(
                company_id=company.id,
                product_id=product_a.id,
                warehouse_id=warehouse_main.id,
                quantity=10,
                sold_at=now - timedelta(days=2),
            ),
            SalesRecord(
                company_id=company.id,
                product_id=product_b.id,
                warehouse_id=warehouse_main.id,
                quantity=2,
                sold_at=now - timedelta(days=3),
            ),
        ]
    )

    db.session.commit()
