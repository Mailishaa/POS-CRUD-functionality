from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.users import user_repository
from schemas.users import UserCreate, UserUpdate
import hashlib

class UserService:
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def list_users(self, db: Session):
        return user_repository.get_all(db)

    def get_user(self, db: Session, user_id: int):
        user = user_repository.get(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        return user

    def create_user(self, db: Session, data: UserCreate):
        user_data = data.model_dump()
        if "password" in user_data:
            plain_password = user_data.pop("password")
            user_data["password_hash"] = self._hash_password(plain_password)
        return user_repository.create(db, user_data)

    def update_user(self, db: Session, user_id: int, data: UserUpdate):
        user = self.get_user(db, user_id)
        user_data = data.model_dump(exclude_unset=True)
        if "password" in user_data and user_data["password"]:
            plain_password = user_data.pop("password")
            user_data["password_hash"] = self._hash_password(plain_password)
        return user_repository.update(db, user, user_data)

    def delete_user(self, db: Session, user_id: int):
        user = self.get_user(db, user_id)
        return user_repository.delete(db, user)

user_service = UserService()
