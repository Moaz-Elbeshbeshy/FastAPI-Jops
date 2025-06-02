from fastapi import HTTPException, status
from datetime import datetime, UTC
from schemas.product_schema import ProductCreateSchema, ProductResponseSchema
from typing import Union, List
from bson import ObjectId, errors as bson_errors
from pymongo import ReturnDocument


async def create_product(
    products: Union[ProductCreateSchema, List[ProductCreateSchema]], user_email: str, db
):
    user = await db.users.find_one({"email": user_email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if not isinstance(products, list):
        products = [products]

    print(products)
    now = datetime.now(UTC)
    product_dicts = []
    for product in products:
        data = product.model_dump()
        data["user_id"] = str(user["_id"])
        data["created_at"] = now
        data["updated_at"] = None
        product_dicts.append(data)

    # This returns an InsertManyResult object that contains a list of the _ids
    result = await db.products.insert_many(product_dicts)
    print(result)

    for i, _id in enumerate(result.inserted_ids):
        product_dicts[i]["id"] = str(_id)

    # Return response
    responses = [ProductResponseSchema(**p) for p in product_dicts]
    return responses[0] if len(responses) == 1 else responses


async def get_products(user_email: str, db):
    existing_user = await db.users.find_one({"email": user_email})
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    products = []
    async for product in db.products.find({"user_id": str(existing_user["_id"])}):
        product["id"] = str(product["_id"])
        del product["_id"]
        products.append(ProductResponseSchema(**product))
    return products


async def get_product(product_id: str, user_email: str, db):
    try:
        # Verify the id so we don't get internal server error, if id is too short or too long
        obj_id = ObjectId(product_id)
    except bson_errors.InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid product ID"
        )
    # Fetch product from DB
    product = await db.products.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found for ID {product_id}",
        )

    # verify user
    existing_user = await db.users.find_one({"email": user_email})
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Match product with user
    if product["user_id"] != str(existing_user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this product",
        )

    # without str you will get Invalid product ID error because ProductResponseSchema expect id of type str not ObjectId
    product["id"] = str(product["_id"])
    del product["_id"]
    return ProductResponseSchema(**product)


async def update_product(
    product_id: str, product_update: ProductCreateSchema, user_email: str, db
):
    try:
        # Verify the id so we don't get internal server error, if id is too short or too long
        obj_id = ObjectId(product_id)
    except bson_errors.InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid product ID"
        )
    # Fetch product from DB
    product = await db.products.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found for ID {product_id}",
        )

    # verify user
    existing_user = await db.users.find_one({"email": user_email})
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Match product with user
    if product["user_id"] != str(existing_user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this product",
        )

    update_data = product_update.model_dump()
    update_data["updated_at"] = datetime.now(UTC)

    # Why use $set? 1.It avoids overwriting the entire document. 2.You can update just the fields you want without affecting others. 3.Safer, efficient than replacing the whole document.
    updated_product = await db.products.find_one_and_update(
        {"_id": ObjectId(product_id)},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER,  # return the updated document after update
    )

    updated_product["id"] = str(updated_product["_id"])
    del updated_product["_id"]
    return ProductResponseSchema(**updated_product)


async def delete_product(product_id: str, user_email: str, db):
    try:
        # Verify the id so we don't get internal server error, if id is too short or too long
        obj_id = ObjectId(product_id)
    except bson_errors.InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid product ID"
        )
    # Fetch product from DB
    product = await db.products.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found for ID {product_id}",
        )

    # verify user
    existing_user = await db.users.find_one({"email": user_email})
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Match product with user
    if product["user_id"] != str(existing_user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this product",
        )

    await db.products.delete_one({"_id": ObjectId(product_id)})
    return {"message": "Product deleted successfully"}
