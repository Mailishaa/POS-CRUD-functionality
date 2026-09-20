from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
)
from sqlalchemy.sql import func

from app.database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    supplier_id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    supplier_name = Column(
        String,
        nullable=False,
    )

    contact_name = Column(
        String,
        nullable=True,
    )

    phone_number = Column(
        String,
        nullable=False,
    )

    email = Column(
        String,
        nullable=True,
    )

    address = Column(
        String,
        nullable=True,
    )

    tax_id = Column(
        String,
        nullable=True,
    )

    lead_time_days = Column(
        Integer,
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