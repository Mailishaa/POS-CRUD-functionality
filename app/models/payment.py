from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class Payment(Base):
    __tablename__ = "payment"

    payment_id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    sale_id = Column(
        Integer,
        ForeignKey("sales.sale_id"),
        nullable=False,
    )

    amount_tendered = Column(
        Numeric(10, 2),
        nullable=False,
    )

    payment_method = Column(
        String(50),
        nullable=False,
    )

    payment_status = Column(
        String(50),
        nullable=False,
        default="Completed",
    )

    reference_number = Column(
        String(255),
        nullable=True,
    )

    payment_datetime = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )