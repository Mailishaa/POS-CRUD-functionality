from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.users import user_repository
from app.schemas.users import UserCreate, UserUpdate
from app.core.security import hash_password


class UserService:

    def list_users(self, db: Session):
        return user_repository.get_all(db)

    def get_user(self, db: Session, user_id: int):
        user = user_repository.get(db, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user

    def create_user(self, db: Session, data: UserCreate):
        if user_repository.get_by_username(db, data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )

        if user_repository.get_by_email(db, data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        user_data = data.model_dump()

        plain_password = user_data.pop("password")
        user_data["password_hash"] = hash_password(plain_password)

        return user_repository.create(db, user_data)

    def update_user(
        self,
        db: Session,
        user_id: int,
        data: UserUpdate,
    ):
        user = self.get_user(db, user_id)

        user_data = data.model_dump(exclude_unset=True)

        if "password" in user_data:
            plain_password = user_data.pop("password")

            if plain_password:
                user_data["password_hash"] = hash_password(
                    plain_password
                )

        if "username" in user_data:
            existing = user_repository.get_by_username(
                db,
                user_data["username"],
            )

            if existing and existing.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already registered",
                )

        if "email" in user_data:
            existing = user_repository.get_by_email(
                db,
                user_data["email"],
            )

            if existing and existing.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )

        return user_repository.update(
            db,
            user,
            user_data,
        )

    def delete_user(self, db: Session, user_id: int):
        user = self.get_user(db, user_id)

        return user_repository.delete(db, user)


user_service = UserService()