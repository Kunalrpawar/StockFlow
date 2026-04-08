from datetime import datetime

from app.extensions import db


class Supplier(db.Model):
    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    contact_email = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    company = db.relationship("Company", back_populates="suppliers")
    product_links = db.relationship("ProductSupplier", back_populates="supplier", cascade="all, delete-orphan")

    __table_args__ = (
        db.UniqueConstraint("company_id", "name", name="uq_supplier_company_name"),
        db.Index("ix_suppliers_company_name", "company_id", "name"),
    )
