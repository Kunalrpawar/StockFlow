from datetime import datetime

from app.extensions import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    sku = db.Column(db.String(100), nullable=False, unique=True)
    product_type = db.Column(db.String(50), nullable=False, default="standard", index=True)
    price = db.Column(db.Numeric(12, 2), nullable=False)
    low_stock_threshold = db.Column(db.Integer, nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    company = db.relationship("Company", back_populates="products")
    inventory_items = db.relationship("Inventory", back_populates="product", cascade="all, delete-orphan")
    product_suppliers = db.relationship("ProductSupplier", back_populates="product", cascade="all, delete-orphan")
    sales_records = db.relationship("SalesRecord", back_populates="product", cascade="all, delete-orphan")

    bundle_components = db.relationship(
        "ProductBundle",
        foreign_keys="ProductBundle.bundle_product_id",
        back_populates="bundle_product",
        cascade="all, delete-orphan",
    )
    component_of = db.relationship(
        "ProductBundle",
        foreign_keys="ProductBundle.component_product_id",
        back_populates="component_product",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        db.CheckConstraint("price >= 0", name="ck_products_price_non_negative"),
        db.CheckConstraint(
            "low_stock_threshold IS NULL OR low_stock_threshold >= 0",
            name="ck_products_threshold_non_negative",
        ),
        db.Index("ix_products_company_name", "company_id", "name"),
    )
