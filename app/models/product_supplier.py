from app.extensions import db


class ProductSupplier(db.Model):
    __tablename__ = "product_suppliers"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=False)
    is_primary = db.Column(db.Boolean, nullable=False, default=False)
    lead_time_days = db.Column(db.Integer, nullable=True)

    product = db.relationship("Product", back_populates="product_suppliers")
    supplier = db.relationship("Supplier", back_populates="product_links")

    __table_args__ = (
        db.UniqueConstraint("product_id", "supplier_id", name="uq_product_supplier_pair"),
        db.CheckConstraint(
            "lead_time_days IS NULL OR lead_time_days >= 0",
            name="ck_product_suppliers_lead_time_non_negative",
        ),
        db.Index("ix_product_suppliers_product_primary", "product_id", "is_primary"),
    )
