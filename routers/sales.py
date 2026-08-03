from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException
from schemas.sales import SaleCreate, SaleRead, SaleUpdate
from services.sales import sales_service
from database import get_db
import traceback

router = APIRouter(prefix="/sales", tags=["sales"])

@router.get("/", response_model=list[SaleRead])
def list_sales(db: Session = Depends(get_db)):
    try:
        return sales_service.list_sales(db)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"GET / sales failed: {str(e)}")

@router.get("/{sale_id}", response_model=SaleRead)
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    try:
        return sales_service.get_sale(db, sale_id)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"GET /{sale_id} sales failed: {str(e)}")

@router.post("/", response_model=SaleRead, status_code=status.HTTP_201_CREATED)
def create_sale(data: SaleCreate, db: Session = Depends(get_db)):
    try:
        return sales_service.create_sale(db, data)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"POST / sales failed: {str(e)}")

@router.put("/{sale_id}", response_model=SaleRead)
def update_sale(sale_id: int, data: SaleUpdate, db: Session = Depends(get_db)):
    try:
        return sales_service.update_sale(db, sale_id, data)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"PUT /{sale_id} sales failed: {str(e)}")

@router.delete("/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    try:
        sales_service.delete_sale(db, sale_id)
        return None
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"DELETE /{sale_id} sales failed: {str(e)}")
