from datetime import datetime

from app.extensions import db


class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    warehouses = db.relationship("Warehouse", back_populates="company", cascade="all, delete-orphan")
    products = db.relationship("Product", back_populates="company", cascade="all, delete-orphan")
    suppliers = db.relationship("Supplier", back_populates="company", cascade="all, delete-orphan")
