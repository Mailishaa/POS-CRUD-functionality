
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.product import product_repository
from schemas.product import ProductCreate, ProductUpdate

def list_product(db: Session):
    """Retrieves all products from the data repository."""
    return product_repository.get_all(db)

def get_product(db: Session, product_id: int):
    """Retrieves a single product or returns a 404 error if missing."""
    product = product_repository.get(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )
    return product

def create_product(db: Session, data: ProductCreate):
    """Unpacks schema data models and passes them to the database repository."""
    product_data = data.model_dump()
    return product_repository.create(db, product_data)

def update_product(db: Session, product_id: int, data: ProductUpdate):
    """Finds an existing record and patches modification data."""
    product = get_product(db, product_id)
    update_data = data.model_dump(exclude_unset=True)
    return product_repository.update(db, product, update_data)

def delete_product(db: Session, product_id: int):
    """Removes a targeted product record permanently."""
    product = get_product(db, product_id)
    return product_repository.delete(db, product)
