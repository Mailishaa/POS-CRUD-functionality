from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.category import category_repository
from schemas.category import CategoryCreate, CategoryUpdate

class CategoryService:
    def list_categories(self, db: Session, active_only: bool = False):
        if active_only:
            return category_repository.get_active(db)
        return category_repository.get_all(db)

    def get_category(self, db: Session, category_id: int):
        category = category_repository.get(db, category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found"
            )
        return category

    def create_category(self, db: Session, data: CategoryCreate):
        if data.parent_category_id:
            self.get_category(db, data.parent_category_id)
        return category_repository.create(db, data.model_dump())

    def update_category(self, db: Session, category_id: int, data: CategoryUpdate):
        category = self.get_category(db, category_id)
        if data.parent_category_id:
            if data.parent_category_id == category_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="A category cannot be its own parent"
                )
            self.get_category(db, data.parent_category_id)
        return category_repository.update(db, category, data.model_dump(exclude_unset=True))

    def delete_category(self, db: Session, category_id: int):
        category = self.get_category(db, category_id)
        return category_repository.delete(db, category)

category_service = CategoryService()
