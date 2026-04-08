from datetime import datetime

from app.extensions import db


class Inventory(db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    product = db.relationship("Product", back_populates="inventory_items")
    warehouse = db.relationship("Warehouse", back_populates="inventory_items")
    logs = db.relationship("InventoryLog", back_populates="inventory", cascade="all, delete-orphan")

    __table_args__ = (
        db.UniqueConstraint("product_id", "warehouse_id", name="uq_inventory_product_warehouse"),
        db.CheckConstraint("quantity >= 0", name="ck_inventory_quantity_non_negative"),
        db.Index("ix_inventory_warehouse_product", "warehouse_id", "product_id"),
    )
