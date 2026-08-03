from sqlalchemy.orm import Session
from models.receipt import Receipt

class ReceiptRepository:
    def __init__(self):
        self.model = Receipt

    def get(self, db: Session, receipt_id: int):
        return db.get(self.model, receipt_id)

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def get_by_sale_id(self, db: Session, sale_id: int):
        return db.query(self.model).filter(self.model.sale_id == sale_id).all()

    def create(self, db: Session, data: dict):
        receipt = self.model(**data)
        db.add(receipt)
        db.commit()
        db.refresh(receipt)
        return receipt

    def update(self, db: Session, db_obj: Receipt, data: dict):
        for field, value in data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Receipt):
        db.delete(db_obj)
        db.commit()
        return db_obj

receipt_repository = ReceiptRepository()
