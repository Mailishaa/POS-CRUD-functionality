from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    parent_category_id = Column(
        Integer,
        ForeignKey("categories.category_id"),
        nullable=True,
    )

    tax_rate = Column(
        Numeric(5, 2),
        nullable=False,
        default=0.00,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    subcategories = relationship(
        "Category",
        backref="parent",
        remote_side=[category_id],
    )