from sqlalchemy import(
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base #defining the connection
class Product(Base):
    __tablename__ = "products"

    
    product_id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String, nullable=False, unique=True)
    item_name = Column(String, nullable=False)
    cost_price = Column(Numeric(10, 2), nullable=False)
    selling_price = Column(Numeric(10, 2), nullable=False)    
    stock_quantity = Column(Numeric(10, 2), nullable=False, default=0.00)   
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)
