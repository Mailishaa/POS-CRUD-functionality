from fastapi import FastAPI
from sqlalchemy import text
from app.database import engine, Base, SessionLocal
from datetime import datetime

from app.models.category import Category 
from app.models.users import User
from app.models.customer import Customer
from app.routers import (
    products,
    customer as customer_router,
    user,
    sales as sales_router,
    sale_item as sale_item_router,
    payment,
    categories,
    suppliers,
    receipts,
    auth,
)

with engine.connect() as connection:
    connection.execute(text("""
        DROP TABLE IF EXISTS 
            receipts, payment, sale_item, sales, products, 
            categories, customers, users, suppliers 
        CASCADE;
    """))
    connection.commit()

Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    default_cat = Category(
        category_id=1,
        category_name="General",
        description="Default Category",
        parent_category_id=None,
        is_active=True
    )
    db.add(default_cat)

    default_user = User(
        user_id=1,
        username="admin",
        password_hash="8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",
        first_name="Admin",
        last_name="User",
        role="Admin",
        shift_status="Clocked Out",
        email="admin@example.com"
    )
    db.add(default_user)

    default_customer = Customer(
        customer_id=1,
        first_name="Walk-in",
        last_name="Customer",
        email="walkin@example.com",
        phone_number="0000000000",
        loyalty_points=0,
        registration_date=datetime.utcnow()
    )
    db.add(default_customer)

    db.commit()
    print("Successfully seeded database defaults!")
except Exception as database_error:
    db.rollback()
    raise RuntimeError(f"Database seeding failed critically: {database_error}") from database_error
finally:
    db.close()

app = FastAPI(title="POS API", version="1.0")

app.include_router(products.router)

app.include_router(auth.router)
app.include_router(customer_router.router)
app.include_router(user.router)
app.include_router(sales_router.router)
app.include_router(sale_item_router.router)
app.include_router(payment.router)
app.include_router(categories.router)
app.include_router(suppliers.router)
app.include_router(receipts.router)

@app.get("/")
def root():
    return {"message": "Boutique POS API is running successfully"}
    
