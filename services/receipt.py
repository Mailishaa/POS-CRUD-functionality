from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.receipt import receipt_repository
from schemas.receipt import ReceiptCreate, ReceiptUpdate

class ReceiptService:
    def list_receipts(self, db: Session):
        return receipt_repository.get_all(db)

    def get_receipt(self, db: Session, receipt_id: int):
        receipt = receipt_repository.get(db, receipt_id)
        if not receipt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Receipt with id {receipt_id} not found"
            )
        return receipt

    def get_receipts_by_sale(self, db: Session, sale_id: int):
        return receipt_repository.get_by_sale_id(db, sale_id)

    def create_receipt(self, db: Session, data: ReceiptCreate):
        return receipt_repository.create(db, data.model_dump())

    def update_receipt(self, db: Session, receipt_id: int, data: ReceiptUpdate):
        receipt = self.get_receipt(db, receipt_id)
        return receipt_repository.update(db, receipt, data.model_dump(exclude_unset=True))

    def delete_receipt(self, db: Session, receipt_id: int):
        receipt = self.get_receipt(db, receipt_id)
        return receipt_repository.delete(db, receipt)

receipt_service = ReceiptService()
