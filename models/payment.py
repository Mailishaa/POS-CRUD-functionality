from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base 


class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.sale_id"), nullable=False)
    payment_method = Column(String, nullable=False)  # 'Cash', 'Credit Card', 'Mobile Wallet'
    amount_tendered = Column(Numeric(10, 2), nullable=False)
    amount_returned = Column(Numeric(10, 2), nullable=False, default=0.00)
    payment_datetime = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    gateway_reference = Column(String, nullable=True)
    status = Column(String, nullable=False, default="Approved")  
