from sqlalchemy.orm import Session
from app.models.customer import Customer

class CustomerRepository:
    def __init__(self):
        self.model = Customer

    def get(self, db: Session, customer_id: int):
        return db.get(self.model, customer_id)

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def get_by_phone(self, db: Session, phone_number: str):
        return db.query(self.model).filter(self.model.phone_number == phone_number).first()

    def create(self, db: Session, data: dict):
        customer = self.model(**data)
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer

    def update(self, db: Session, db_obj: Customer, data: dict):
        for field, value in data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Customer):
        db.delete(db_obj)
        db.commit()
        return db_obj

customer_repository = CustomerRepository()
