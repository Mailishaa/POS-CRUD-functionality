from sqlalchemy.orm import Session
from models.category import Category

class CategoryRepository:
    def __init__(self):
        self.model = Category

    def get(self, db: Session, category_id: int):
        return db.get(self.model, category_id)

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def get_active(self, db: Session):
        return db.query(self.model).filter(self.model.is_active == True).all()

    def create(self, db: Session, data: dict):
        category = self.model(**data)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    def update(self, db: Session, db_obj: Category, data: dict):
        for field, value in data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Category):
        db.delete(db_obj)
        db.commit()
        return db_obj

category_repository = CategoryRepository()
