from datetime import datetime

from app.extensions import db


class Warehouse(db.Model):
    __tablename__ = "warehouses"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    company = db.relationship("Company", back_populates="warehouses")
    inventory_items = db.relationship("Inventory", back_populates="warehouse", cascade="all, delete-orphan")
    sales_records = db.relationship("SalesRecord", back_populates="warehouse", cascade="all, delete-orphan")

    __table_args__ = (
        db.UniqueConstraint("company_id", "name", name="uq_warehouse_company_name"),
    )
