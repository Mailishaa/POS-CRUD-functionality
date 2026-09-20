from datetime import date

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.sql import func

from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    first_name = Column(
        String(100),
        nullable=False,
    )

    last_name = Column(
        String(100),
        nullable=False,
    )

    phone_number = Column(
        String(50),
        nullable=True,
    )

    email = Column(
        String(255),
        nullable=True,
    )

    loyalty_points = Column(
        Integer,
        nullable=False,
        default=0,
    )

    registration_date = Column(
        Date,
        nullable=False,
        default=date.today,
    )