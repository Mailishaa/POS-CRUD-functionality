from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.receipt import receipt_repository
from app.repositories.sales import sale_repository
from app.schemas.receipt import ReceiptCreate, ReceiptUpdate


class ReceiptService:

    def list_receipts(self, db: Session):
        return receipt_repository.get_all(db)

    def get_receipt(
        self,
        db: Session,
        receipt_id: int,
    ):
        receipt = receipt_repository.get(
            db,
            receipt_id,
        )

        if not receipt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Receipt not found",
            )

        return receipt

    def get_receipts_by_sale(
        self,
        db: Session,
        sale_id: int,
    ):
        return receipt_repository.get_by_sale_id(
            db,
            sale_id,
        )

    def create_receipt(
        self,
        db: Session,
        data: ReceiptCreate,
    ):
        if not sale_repository.get(
            db,
            data.sale_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid sale_id. Make sure the sale exists.",
            )

        existing = receipt_repository.get_by_number(
            db,
            data.receipt_number,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Receipt number already registered",
            )

        return receipt_repository.create(
            db,
            data.model_dump(),
        )

    def update_receipt(
        self,
        db: Session,
        receipt_id: int,
        data: ReceiptUpdate,
    ):
        receipt = self.get_receipt(
            db,
            receipt_id,
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "sale_id" in update_data:
            if not sale_repository.get(
                db,
                update_data["sale_id"],
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid sale_id. Make sure the sale exists.",
                )

        if "receipt_number" in update_data:
            existing = receipt_repository.get_by_number(
                db,
                update_data["receipt_number"],
            )

            if (
                existing
                and existing.receipt_id != receipt_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Receipt number already registered",
                )

        return receipt_repository.update(
            db,
            receipt,
            update_data,
        )

    def delete_receipt(
        self,
        db: Session,
        receipt_id: int,
    ):
        receipt = self.get_receipt(
            db,
            receipt_id,
        )

        return receipt_repository.delete(
            db,
            receipt,
        )


receipt_service = ReceiptService()