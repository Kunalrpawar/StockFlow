from dataclasses import dataclass
from datetime import datetime, timedelta
from math import ceil

from sqlalchemy import func

from app.models.inventory import Inventory
from app.models.product import Product
from app.models.product_supplier import ProductSupplier
from app.models.sales_record import SalesRecord
from app.models.supplier import Supplier
from app.models.warehouse import Warehouse


@dataclass
class AlertRow:
    product_id: int
    product_name: str
    sku: str
    warehouse_id: int
    warehouse_name: str
    current_stock: int
    threshold: int
    days_until_stockout: int | None
    supplier: dict | None


class AlertService:
    SALES_WINDOW_DAYS = 30
    PRODUCT_TYPE_THRESHOLDS = {
        "standard": 20,
        "fragile": 15,
        "bulk": 50,
    }

    @classmethod
    def _resolve_threshold(cls, product_type: str, explicit_threshold: int | None) -> int:
        if explicit_threshold is not None:
            return explicit_threshold
        return cls.PRODUCT_TYPE_THRESHOLDS.get(product_type, cls.PRODUCT_TYPE_THRESHOLDS["standard"])

    @classmethod
    def get_low_stock_alerts(cls, company_id: int) -> dict:
        cutoff = datetime.utcnow() - timedelta(days=cls.SALES_WINDOW_DAYS)

        sales_subquery = (
            SalesRecord.query.with_entities(
                SalesRecord.product_id.label("product_id"),
                SalesRecord.warehouse_id.label("warehouse_id"),
                func.sum(SalesRecord.quantity).label("sales_qty_30d"),
            )
            .filter(SalesRecord.company_id == company_id, SalesRecord.sold_at >= cutoff)
            .group_by(SalesRecord.product_id, SalesRecord.warehouse_id)
            .subquery()
        )

        primary_supplier_subquery = (
            ProductSupplier.query.with_entities(
                ProductSupplier.product_id.label("product_id"),
                ProductSupplier.supplier_id.label("supplier_id"),
            )
            .filter(ProductSupplier.is_primary.is_(True))
            .subquery()
        )

        rows = (
            Inventory.query.with_entities(
                Product.id.label("product_id"),
                Product.name.label("product_name"),
                Product.sku.label("sku"),
                Product.product_type.label("product_type"),
                Warehouse.id.label("warehouse_id"),
                Warehouse.name.label("warehouse_name"),
                Inventory.quantity.label("current_stock"),
                Product.low_stock_threshold.label("threshold"),
                sales_subquery.c.sales_qty_30d.label("sales_qty_30d"),
                Supplier.id.label("supplier_id"),
                Supplier.name.label("supplier_name"),
                Supplier.contact_email.label("supplier_email"),
            )
            .join(Product, Product.id == Inventory.product_id)
            .join(Warehouse, Warehouse.id == Inventory.warehouse_id)
            .join(
                sales_subquery,
                (sales_subquery.c.product_id == Product.id)
                & (sales_subquery.c.warehouse_id == Warehouse.id),
            )
            .outerjoin(
                primary_supplier_subquery,
                primary_supplier_subquery.c.product_id == Product.id,
            )
            .outerjoin(Supplier, Supplier.id == primary_supplier_subquery.c.supplier_id)
            .filter(
                Product.company_id == company_id,
                Warehouse.company_id == company_id,
                Product.is_active.is_(True),
            )
            .all()
        )

        alerts: list[dict] = []
        for row in rows:
            threshold = cls._resolve_threshold(row.product_type, row.threshold)
            if row.current_stock >= threshold:
                continue

            daily_sales = float(row.sales_qty_30d) / cls.SALES_WINDOW_DAYS
            if daily_sales <= 0:
                days_until_stockout = None
            else:
                days_until_stockout = max(0, ceil(row.current_stock / daily_sales))

            supplier = None
            if row.supplier_id is not None:
                supplier = {
                    "id": row.supplier_id,
                    "name": row.supplier_name,
                    "contact_email": row.supplier_email,
                }

            alert = AlertRow(
                product_id=row.product_id,
                product_name=row.product_name,
                sku=row.sku,
                warehouse_id=row.warehouse_id,
                warehouse_name=row.warehouse_name,
                current_stock=row.current_stock,
                threshold=threshold,
                days_until_stockout=days_until_stockout,
                supplier=supplier,
            )
            alerts.append(alert.__dict__)

        return {
            "alerts": alerts,
            "total_alerts": len(alerts),
        }
