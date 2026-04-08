from datetime import datetime

from app.extensions import db


class InventoryLog(db.Model):
    __tablename__ = "inventory_logs"

    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey("inventory.id"), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False, index=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"), nullable=False, index=True)
    change_type = db.Column(db.String(50), nullable=False)
    quantity_delta = db.Column(db.Integer, nullable=False)
    quantity_before = db.Column(db.Integer, nullable=False)
    quantity_after = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    inventory = db.relationship("Inventory", back_populates="logs")

    __table_args__ = (
        db.CheckConstraint("quantity_after >= 0", name="ck_inventory_logs_quantity_after_non_negative"),
        db.Index("ix_inventory_logs_product_warehouse_created", "product_id", "warehouse_id", "created_at"),
    )
