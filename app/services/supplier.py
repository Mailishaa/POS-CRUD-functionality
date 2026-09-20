from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.supplier import supplier_repository
from app.schemas.supplier import SupplierCreate, SupplierUpdate


class SupplierService:

    def list_suppliers(self, db: Session):
        return supplier_repository.get_all(db)

    def get_supplier(
        self,
        db: Session,
        supplier_id: int,
    ):
        supplier = supplier_repository.get(
            db,
            supplier_id,
        )

        if not supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supplier not found",
            )

        return supplier

    def create_supplier(
        self,
        db: Session,
        data: SupplierCreate,
    ):
        supplier_data = data.model_dump()

        supplier_data["phone_number"] = supplier_data.pop(
            "phone"
        )

        return supplier_repository.create(
            db,
            supplier_data,
        )

    def update_supplier(
        self,
        db: Session,
        supplier_id: int,
        data: SupplierUpdate,
    ):
        supplier = self.get_supplier(
            db,
            supplier_id,
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "phone" in update_data:
            update_data["phone_number"] = update_data.pop(
                "phone"
            )

        return supplier_repository.update(
            db,
            supplier,
            update_data,
        )

    def delete_supplier(
        self,
        db: Session,
        supplier_id: int,
    ):
        supplier = self.get_supplier(
            db,
            supplier_id,
        )

        return supplier_repository.delete(
            db,
            supplier,
        )


supplier_service = SupplierService()