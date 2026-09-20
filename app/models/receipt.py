from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.sql import func

from app.database import Base


class Receipt(Base):
    __tablename__ = "receipts"

    receipt_id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    sale_id = Column(
        Integer,
        ForeignKey("sales.sale_id"),
        nullable=False,
    )

    receipt_number = Column(
        String,
        nullable=False,
        unique=True,
        index=True,
    )

    issued_datetime = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )