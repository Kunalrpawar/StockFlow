from datetime import datetime

from app.extensions import db


class SalesRecord(db.Model):
    __tablename__ = "sales_records"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False, index=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False)
    sold_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    product = db.relationship("Product", back_populates="sales_records")
    warehouse = db.relationship("Warehouse", back_populates="sales_records")

    __table_args__ = (
        db.CheckConstraint("quantity > 0", name="ck_sales_records_quantity_positive"),
        db.Index("ix_sales_records_company_date", "company_id", "sold_at"),
        db.Index("ix_sales_records_product_warehouse_date", "product_id", "warehouse_id", "sold_at"),
    )
