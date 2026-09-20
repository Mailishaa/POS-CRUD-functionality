from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.users import User
from app.repositories.sales import sale_repository
from app.schemas.sales import SaleCreate, SaleUpdate


class SaleService:

    def list_sales(self, db: Session):
        return sale_repository.get_all(db)

    def get_sale(self, db: Session, sale_id: int):
        sale = sale_repository.get(db, sale_id)

        if not sale:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sale not found",
            )

        return sale

    def create_sale(self, db: Session, data: SaleCreate):
        user = db.get(User, data.user_id)
        customer = db.get(Customer, data.customer_id)

        if user is None or customer is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Invalid user_id or customer_id. "
                    "Make sure both exist."
                ),
            )

        total = data.total_amount

        subtotal = (
            data.subtotal
            if data.subtotal is not None
            else total
        )

        transaction_number = (
            data.transaction_number
            or f"TXN-{uuid4().hex[:12].upper()}"
        )

        return sale_repository.create(
            db,
            {
                "transaction_number": transaction_number,
                "user_id": data.user_id,
                "customer_id": data.customer_id,
                "terminal_id": data.terminal_id,
                "subtotal": subtotal,
                "discount_amount": data.discount_amount,
                "tax_amount": data.tax_amount,
                "total_amount": total,
                "payment_method": data.payment_method,
                "status": data.status,
            },
        )

    def update_sale(
        self,
        db: Session,
        sale_id: int,
        data: SaleUpdate,
    ):
        sale = self.get_sale(db, sale_id)

        values = data.model_dump(exclude_unset=True)

        if "user_id" in values:
            if db.get(User, values["user_id"]) is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Invalid user_id or customer_id. "
                        "Make sure both exist."
                    ),
                )

        if "customer_id" in values:
            if db.get(Customer, values["customer_id"]) is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Invalid user_id or customer_id. "
                        "Make sure both exist."
                    ),
                )

        return sale_repository.update(
            db,
            sale,
            values,
        )

    def delete_sale(self, db: Session, sale_id: int):
        sale = self.get_sale(db, sale_id)

        sale_repository.delete(
            db,
            sale,
        )


sale_service = SaleService()