from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base 

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(String, nullable=False)  
    shift_status = Column(String, nullable=False, default="Clocked Out")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

