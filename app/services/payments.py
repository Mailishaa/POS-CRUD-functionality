from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.sales import Sale
from app.repositories.payment import payment_repository
from app.schemas.payment import PaymentCreate, PaymentUpdate


class PaymentService:

    def list_payments(self, db: Session):
        return payment_repository.get_all(db)

    def get_payment(self, db: Session, payment_id: int):
        payment = payment_repository.get(db, payment_id)

        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found",
            )

        return payment

    def _validate_sale(self, db: Session, sale_id: int):
        sale = db.get(Sale, sale_id)

        if sale is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sale not found",
            )

    def create_payment(self, db: Session, data: PaymentCreate):
        self._validate_sale(db, data.sale_id)

        return payment_repository.create(
            db,
            {
                "sale_id": data.sale_id,
                "amount_tendered": data.amount_paid,
                "payment_method": data.payment_method,
                "payment_status": data.payment_status,
                "reference_number": data.reference_number,
            },
        )

    def update_payment(
        self,
        db: Session,
        payment_id: int,
        data: PaymentUpdate,
    ):
        payment = self.get_payment(db, payment_id)
        values = data.model_dump(exclude_unset=True)

        if "sale_id" in values:
            self._validate_sale(db, values["sale_id"])

        mapped = {}

        if "sale_id" in values:
            mapped["sale_id"] = values["sale_id"]

        if "amount_paid" in values:
            mapped["amount_tendered"] = values["amount_paid"]

        if "payment_method" in values:
            mapped["payment_method"] = values["payment_method"]

        if "payment_status" in values:
            mapped["payment_status"] = values["payment_status"]

        if "reference_number" in values:
            mapped["reference_number"] = values["reference_number"]

        return payment_repository.update(
            db,
            payment,
            mapped,
        )

    def delete_payment(self, db: Session, payment_id: int):
        payment = self.get_payment(db, payment_id)
        payment_repository.delete(db, payment)


payment_service = PaymentService()