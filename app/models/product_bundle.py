from app.extensions import db


class ProductBundle(db.Model):
    __tablename__ = "product_bundles"

    id = db.Column(db.Integer, primary_key=True)
    bundle_product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    component_product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    component_quantity = db.Column(db.Integer, nullable=False, default=1)

    bundle_product = db.relationship(
        "Product",
        foreign_keys=[bundle_product_id],
        back_populates="bundle_components",
    )
    component_product = db.relationship(
        "Product",
        foreign_keys=[component_product_id],
        back_populates="component_of",
    )

    __table_args__ = (
        db.UniqueConstraint(
            "bundle_product_id",
            "component_product_id",
            name="uq_bundle_component_pair",
        ),
        db.CheckConstraint(
            "bundle_product_id <> component_product_id",
            name="ck_product_bundle_not_self",
        ),
        db.CheckConstraint(
            "component_quantity > 0",
            name="ck_product_bundle_component_quantity_positive",
        ),
    )
