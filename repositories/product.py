from sqlalchemy.orm import Session
from models.product import Product

class ProductRepository:
    def __init__(self):
        self.model = Product

    def get(self, db: Session, product_id: int):
        return db.get(self.model, product_id)

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def get_by_category(self, db: Session, category_id: int):
        return db.query(self.model).filter(self.model.category_id == category_id).all()

    def create(self, db: Session, data: dict):
        product = self.model(**data)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    def update(self, db: Session, db_obj: Product, data: dict):
        for field, value in data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Product):
        db.delete(db_obj)
        db.commit()
        return db_obj

product_repository = ProductRepository()
