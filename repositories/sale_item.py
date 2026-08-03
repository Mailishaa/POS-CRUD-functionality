from sqlalchemy.orm import Session
from models.sale_item import SaleItem

class SaleItemRepository:
    def __init__(self):
        self.model = SaleItem

    def get(self, db: Session, sale_item_id: int):
        return db.get(self.model, sale_item_id)

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def get_by_sale_id(self, db: Session, sale_id: int):
        return db.query(self.model).filter(self.model.sale_id == sale_id).all()

    def create(self, db: Session, data: dict):
        sale_item = self.model(**data)
        db.add(sale_item)
        db.commit()
        db.refresh(sale_item)
        return sale_item

    def update(self, db: Session, db_obj: SaleItem, data: dict):
        for field, value in data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: SaleItem):
        db.delete(db_obj)
        db.commit()
        return db_obj

sale_item_repository = SaleItemRepository()
