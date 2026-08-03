from sqlalchemy.orm import Session
from models.users import User

class UserRepository:
    def __init__(self):
        self.model = User

    def get(self, db: Session, user_id: int):
        return db.get(self.model, user_id)

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def get_by_username(self, db: Session, username: str):
        return db.query(self.model).filter(self.model.username == username).first()

    def create(self, db: Session, data: dict):
        user = self.model(**data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(self, db: Session, db_obj: User, data: dict):
        for field, value in data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: User):
        db.delete(db_obj)
        db.commit()
        return db_obj

user_repository = UserRepository()
