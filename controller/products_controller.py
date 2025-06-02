from fastapi import HTTPException, status
from datetime import datetime, UTC
from schemas.product_schema import ProductCreate, ProductResponse


async def create_product(product: ProductCreate, user_email: str, db):
    user = await db.users.find_one({"email": user_email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    product_dict = product.model_dump()
    product_dict["user_id"] = str(user["_id"])
    product_dict["created_at"] = datetime.now(UTC)
    product_dict["updated_at"] = None

    result = await db.products.insert_one(product_dict)
    product_dict["id"] = str(result.inserted_id)

    return ProductResponse(**product_dict)


async def get_products(user_email: str, db):
    return "Here are All the products"


async def get_product(product_id: str, user_email: str, db):
    return "Single product"


async def update_product(product_id: str, user_email: str, db):
    return "Modified product"


async def delete_product(product_id: str, user_email: str, db):
    return "Deleted produt"
