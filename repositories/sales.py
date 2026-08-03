from sqlalchemy.orm import Session
from models.sales import Sale

class SaleRepository:
    def __init__(self):
        self.model = Sale

    def get(self, db: Session, sale_id: int):
        return db.get(self.model, sale_id)

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def create(self, db: Session, data: dict):
        sale = self.model(**data)
        db.add(sale)
        db.commit()
        db.refresh(sale)
        return sale

    def update(self, db: Session, db_obj: Sale, data: dict):
        for field, value in data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Sale):
        db.delete(db_obj)
        db.commit()
        return db_obj

sale_repository = SaleRepository()
