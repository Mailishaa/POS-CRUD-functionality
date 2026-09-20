from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.supplier import Supplier
from app.repositories.product import product_repository
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:

    def list_product(self, db: Session):
        return product_repository.get_all(db)

    def get_product(self, db: Session, product_id: int):
        product = product_repository.get(db, product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        return product

    def _validate_relationships(
        self,
        db: Session,
        category_id: int | None,
        supplier_id: int | None,
    ):
        if category_id is not None:
            category = db.get(Category, category_id)

            if category is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Category not found",
                )

        if supplier_id is not None:
            supplier = db.get(Supplier, supplier_id)

            if supplier is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Supplier not found",
                )

    def create_product(self, db: Session, data: ProductCreate):
        if data.barcode is not None:
            existing = product_repository.get_by_barcode(
                db,
                data.barcode,
            )

            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Barcode already registered",
                )

        self._validate_relationships(
            db,
            data.category_id,
            data.supplier_id,
        )

        product = product_repository.create(
            db,
            {
                "barcode": data.barcode,
                "item_name": data.product_name,
                "cost_price": data.cost_price,
                "selling_price": data.unit_price,
                "stock_quantity": data.stock_qty,
                "category_id": data.category_id,
                "supplier_id": data.supplier_id,
                "is_active": data.is_active,
            },
        )

        return product

    def update_product(
        self,
        db: Session,
        product_id: int,
        data: ProductUpdate,
    ):
        product = self.get_product(db, product_id)

        values = data.model_dump(exclude_unset=True)

        if "barcode" in values and values["barcode"] is not None:
            existing = product_repository.get_by_barcode(
                db,
                values["barcode"],
            )

            if existing and existing.product_id != product_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Barcode already registered",
                )

        self._validate_relationships(
            db,
            values.get("category_id", product.category_id),
            values.get("supplier_id", product.supplier_id),
        )

        mapped = {}

        if "barcode" in values:
            mapped["barcode"] = values["barcode"]

        if "product_name" in values:
            mapped["item_name"] = values["product_name"]

        if "unit_price" in values:
            mapped["selling_price"] = values["unit_price"]

        if "stock_qty" in values:
            mapped["stock_quantity"] = values["stock_qty"]

        if "category_id" in values:
            mapped["category_id"] = values["category_id"]

        if "supplier_id" in values:
            mapped["supplier_id"] = values["supplier_id"]

        if "cost_price" in values:
            mapped["cost_price"] = values["cost_price"]

        if "is_active" in values:
            mapped["is_active"] = values["is_active"]

        return product_repository.update(
            db,
            product,
            mapped,
        )

    def delete_product(self, db: Session, product_id: int):
        product = self.get_product(db, product_id)

        product_repository.delete(
            db,
            product,
        )


product_service = ProductService()