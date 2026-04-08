from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.inventory import Inventory
from app.models.inventory_log import InventoryLog
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.utils.validators import ValidationError


class ProductServiceError(Exception):
    pass


class ProductService:
    @staticmethod
    def create_product(payload: dict) -> Product:
        warehouse = Warehouse.query.filter_by(
            id=payload["warehouse_id"],
            company_id=payload["company_id"],
        ).first()
        if warehouse is None:
            raise ValidationError("warehouse_id is invalid for the given company_id")

        existing_product = Product.query.filter_by(sku=payload["sku"]).first()
        if existing_product is not None:
            raise ValidationError("SKU already exists")

        try:
            product = Product(
                company_id=payload["company_id"],
                name=payload["name"],
                sku=payload["sku"],
                price=payload["price"],
                product_type=payload["product_type"],
                low_stock_threshold=payload["low_stock_threshold"],
            )
            db.session.add(product)
            db.session.flush()

            inventory = Inventory(
                product_id=product.id,
                warehouse_id=payload["warehouse_id"],
                quantity=payload["initial_quantity"],
            )
            db.session.add(inventory)
            db.session.flush()

            log = InventoryLog(
                inventory_id=inventory.id,
                product_id=product.id,
                warehouse_id=payload["warehouse_id"],
                change_type="initial_stock",
                quantity_delta=payload["initial_quantity"],
                quantity_before=0,
                quantity_after=payload["initial_quantity"],
                reason="Initial stock during product creation",
            )
            db.session.add(log)
            db.session.commit()
        except IntegrityError as exc:
            db.session.rollback()
            raise ProductServiceError("Failed to create product due to data integrity constraints") from exc
        except Exception as exc:
            db.session.rollback()
            raise ProductServiceError("Unexpected error while creating product") from exc

        return product
