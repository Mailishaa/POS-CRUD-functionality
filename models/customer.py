from sqlalchemy import Column, Integer, String, Date


from database import Base 



class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=True)
    loyalty_points = Column(Integer, nullable=False, default=0)
    registration_date = Column(Date, nullable=False)
