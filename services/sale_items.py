from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.sale_item import sale_item_repository
from schemas.sale_item import SaleItemCreate, SaleItemUpdate

class SaleItemService:
    def list_sale_items(self, db: Session):
        return sale_item_repository.get_all(db)

    def get_sale_item(self, db: Session, sale_item_id: int):
        item = sale_item_repository.get(db, sale_item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sale item with id {sale_item_id} not found"
            )
        return item

    def get_items_by_sale(self, db: Session, sale_id: int):
        return sale_item_repository.get_by_sale_id(db, sale_id)

    def create_sale_item(self, db: Session, data: SaleItemCreate):
        return sale_item_repository.create(db, data.model_dump())

    def update_sale_item(self, db: Session, sale_item_id: int, data: SaleItemUpdate):
        item = self.get_sale_item(db, sale_item_id)
        return sale_item_repository.update(db, item, data.model_dump(exclude_unset=True))

    def delete_sale_item(self, db: Session, sale_item_id: int):
        item = self.get_sale_item(db, sale_item_id)
        return sale_item_repository.delete(db, item)

sale_item_service = SaleItemService()
