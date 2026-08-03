from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.payment import payment_repository
from schemas.payment import PaymentCreate, PaymentUpdate

class PaymentService:
    def list_payments(self, db: Session):
        return payment_repository.get_all(db)

    def get_payment(self, db: Session, payment_id: int):
        payment = payment_repository.get(db, payment_id)
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Payment entry with id {payment_id} not found"
            )
        return payment

    def get_payments_by_sale(self, db: Session, sale_id: int):
        return payment_repository.get_by_sale_id(db, sale_id)

    def create_payment(self, db: Session, data: PaymentCreate):
        return payment_repository.create(db, data.model_dump())

    def update_payment(self, db: Session, payment_id: int, data: PaymentUpdate):
        payment = self.get_payment(db, payment_id)
        return payment_repository.update(db, payment, data.model_dump(exclude_unset=True))

    def delete_payment(self, db: Session, payment_id: int):
        payment = self.get_payment(db, payment_id)
        return payment_repository.delete(db, payment)

payment_service = PaymentService()
