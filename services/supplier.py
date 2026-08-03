from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.supplier import supplier_repository
from schemas.supplier import SupplierCreate, SupplierUpdate

class SupplierService:
    def list_suppliers(self, db: Session):
        return supplier_repository.get_all(db)

    def get_supplier(self, db: Session, supplier_id: int):
        supplier = supplier_repository.get(db, supplier_id)
        if not supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Supplier with id {supplier_id} not found"
            )
        return supplier

    def create_supplier(self, db: Session, data: SupplierCreate):
        return supplier_repository.create(db, data.model_dump())

    def update_supplier(self, db: Session, supplier_id: int, data: SupplierUpdate):
        supplier = self.get_supplier(db, supplier_id)
        return supplier_repository.update(db, supplier, data.model_dump(exclude_unset=True))

    def delete_supplier(self, db: Session, supplier_id: int):
        supplier = self.get_supplier(db, supplier_id)
        return supplier_repository.delete(db, supplier)

supplier_service = SupplierService()
