# from sqlalchemy.orm import Session
# from fastapi import HTTPException, status
# from repositories.sales import sale_repository

# from schemas.sales import SaleCreate, SaleUpdate

# class SaleService:
#     def list_sales(self, db: Session):
#         return sale_repository.get_all(db)

#     def get_sale(self, db: Session, sale_id: int):
#         sale = sale_repository.get(db, sale_id)
#         if not sale:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Sale transaction with id {sale_id} not found"
#             )
#         return sale

#     def create_sale(self, db: Session, data: SaleCreate):
#         if sale_repository.get_by_transaction_number(db, data.transaction_number):
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Transaction number already exists"
#             )
#         return sale_repository.create(db, data.model_dump())

#     def update_sale(self, db: Session, sale_id: int, data: SaleUpdate):
#         sale = self.get_sale(db, sale_id)
#         return sale_repository.update(db, sale, data.model_dump(exclude_unset=True))

#     def delete_sale(self, db: Session, sale_id: int):
#         sale = self.get_sale(db, sale_id)
#         return sale_repository.delete(db, sale)

# sale_service = SaleService()

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.sales import sale_repository
from schemas.sales import SaleCreate, SaleUpdate

class SaleService:
    def list_sales(self, db: Session):
        return sale_repository.get_all(db)

    def get_sale(self, db: Session, sale_id: int):
        sale = sale_repository.get(db, sale_id)
        if not sale:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sale with id {sale_id} not found"
            )
        return sale

    def create_sale(self, db: Session, data: SaleCreate):
        return sale_repository.create(db, data.model_dump())

    def update_sale(self, db: Session, sale_id: int, data: SaleUpdate):
        sale = self.get_sale(db, sale_id)
        return sale_repository.update(db, sale, data.model_dump(exclude_unset=True))

    def delete_sale(self, db: Session, sale_id: int):
        sale = self.get_sale(db, sale_id)
        return sale_repository.delete(db, sale)


sales_service = SaleService()
