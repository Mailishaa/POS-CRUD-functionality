from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.sale_item import sale_item_repository
from app.repositories.sales import sale_repository
from app.repositories.product import product_repository
from app.schemas.sale_item import SaleItemCreate, SaleItemUpdate


class SaleItemService:

    def list_sale_items(self, db: Session):
        return sale_item_repository.get_all(db)

    def get_sale_item(
        self,
        db: Session,
        sale_item_id: int,
    ):
        item = sale_item_repository.get(
            db,
            sale_item_id,
        )

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sale item not found",
            )

        return item

    def get_items_by_sale(
        self,
        db: Session,
        sale_id: int,
    ):
        return sale_item_repository.get_by_sale_id(
            db,
            sale_id,
        )

    def create_sale_item(
        self,
        db: Session,
        data: SaleItemCreate,
    ):
        sale = sale_repository.get(
            db,
            data.sale_id,
        )

        product = product_repository.get(
            db,
            data.product_id,
        )

        if not sale or not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Invalid sale_id or product_id. "
                    "Make sure both exist."
                ),
            )

        item_data = data.model_dump()

        item_data["unit_price"] = item_data.pop(
            "item_price"
        )

        if item_data["total_price"] is None:
            item_data["total_price"] = (
                item_data["quantity"]
                * item_data["unit_price"]
                - item_data["discount_applied"]
                + item_data["tax_amount"]
            )

        return sale_item_repository.create(
            db,
            item_data,
        )

    def update_sale_item(
        self,
        db: Session,
        sale_item_id: int,
        data: SaleItemUpdate,
    ):
        item = self.get_sale_item(
            db,
            sale_item_id,
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "sale_id" in update_data:
            if not sale_repository.get(
                db,
                update_data["sale_id"],
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Invalid sale_id or product_id. "
                        "Make sure both exist."
                    ),
                )

        if "product_id" in update_data:
            if not product_repository.get(
                db,
                update_data["product_id"],
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Invalid sale_id or product_id. "
                        "Make sure both exist."
                    ),
                )

        if "item_price" in update_data:
            update_data["unit_price"] = update_data.pop(
                "item_price"
            )

        return sale_item_repository.update(
            db,
            item,
            update_data,
        )

    def delete_sale_item(
        self,
        db: Session,
        sale_item_id: int,
    ):
        item = self.get_sale_item(
            db,
            sale_item_id,
        )

        return sale_item_repository.delete(
            db,
            item,
        )


sale_item_service = SaleItemService()