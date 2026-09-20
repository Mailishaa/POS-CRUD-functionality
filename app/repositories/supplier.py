from sqlalchemy.orm import Session
from app.models.supplier import Supplier

class SupplierRepository:
    def __init__(self):
        self.model = Supplier

    def get(self, db: Session, supplier_id: int):
        return db.get(self.model, supplier_id)

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def create(self, db: Session, data: dict):
        supplier = self.model(**data)
        db.add(supplier)
        db.commit()
        db.refresh(supplier)
        return supplier

    def update(self, db: Session, db_obj: Supplier, data: dict):
        for field, value in data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Supplier):
        db.delete(db_obj)
        db.commit()
        return db_obj

supplier_repository = SupplierRepository()
