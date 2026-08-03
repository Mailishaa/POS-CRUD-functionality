from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from schemas.sale_item import SaleItemCreate, SaleItemRead, SaleItemUpdate
from services.sale_items import sale_item_service
from database import get_db

router = APIRouter(prefix="/sale-items", tags=["sale-items"])

@router.get("/", response_model=list[SaleItemRead])
def list_sale_items(db: Session = Depends(get_db)):
    return sale_item_service.list_sale_items(db)

@router.get("/{sale_item_id}", response_model=SaleItemRead)
def get_sale_item(sale_item_id: int, db: Session = Depends(get_db)):
    return sale_item_service.get_sale_item(db, sale_item_id)

@router.get("/sale/{sale_id}", response_model=list[SaleItemRead])
def get_items_by_sale(sale_id: int, db: Session = Depends(get_db)):
    return sale_item_service.get_items_by_sale(db, sale_id)

@router.post("/", response_model=SaleItemRead, status_code=status.HTTP_201_CREATED)
def create_sale_item(data: SaleItemCreate, db: Session = Depends(get_db)):
    return sale_item_service.create_sale_item(db, data)

@router.put("/{sale_item_id}", response_model=SaleItemRead)
def update_sale_item(sale_item_id: int, data: SaleItemUpdate, db: Session = Depends(get_db)):
    return sale_item_service.update_sale_item(db, sale_item_id, data)

@router.delete("/{sale_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sale_item(sale_item_id: int, db: Session = Depends(get_db)):
    sale_item_service.delete_sale_item(db, sale_item_id)
    return None
