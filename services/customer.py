from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.customer import customer_repository
from schemas.customer import CustomerCreate, CustomerUpdate

class CustomerService:
    def list_customers(self, db: Session):
        return customer_repository.get_all(db)

    def get_customer(self, db: Session, customer_id: int):
        customer = customer_repository.get(db, customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer with id {customer_id} not found"
            )
        return customer

    def get_customer_by_phone(self, db: Session, phone_number: str):
        customer = customer_repository.get_by_phone(db, phone_number)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer with phone number {phone_number} not found"
            )
        return customer

    def create_customer(self, db: Session, data: CustomerCreate):
        existing = customer_repository.get_by_phone(db, data.phone_number)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already registered to a loyalty profile"
            )
        return customer_repository.create(db, data.model_dump())

    def update_customer(self, db: Session, customer_id: int, data: CustomerUpdate):
        customer = self.get_customer(db, customer_id)
        update_data = data.model_dump(exclude_unset=True)
        return customer_repository.update(db, customer, update_data)

    def delete_customer(self, db: Session, customer_id: int):
        customer = self.get_customer(db, customer_id)
        return customer_repository.delete(db, customer)

customer_service = CustomerService()
