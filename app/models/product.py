from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    barcode = Column(
        String(100),
        unique=True,
        nullable=True,
        index=True,
    )

    item_name = Column(
        String(255),
        nullable=False,
    )

    cost_price = Column(
        Numeric(10, 2),
        nullable=False,
        default=0,
    )

    selling_price = Column(
        Numeric(10, 2),
        nullable=False,
    )

    stock_quantity = Column(
        Integer,
        nullable=False,
        default=0,
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.category_id"),
        nullable=True,
    )

    supplier_id = Column(
        Integer,
        ForeignKey("suppliers.supplier_id"),
        nullable=True,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )