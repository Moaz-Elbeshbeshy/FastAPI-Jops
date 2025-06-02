from fastapi import APIRouter, status, Depends, Response
from motor.motor_asyncio import AsyncIOMotorDatabase
from schemas.product_schema import ProductCreateSchema, ProductResponseSchema
from typing import Union, List
from middleware.auth_middleware import get_current_user
from db.database import get_db
from controller.products_controller import (
    create_product,
    get_products,
    get_product,
    update_product,
    delete_product,
)


router = APIRouter()


@router.post(
    "/",
    response_model=Union[ProductResponseSchema, List[ProductResponseSchema]],
    status_code=status.HTTP_201_CREATED,
)
async def create_product_route(
    products: Union[ProductCreateSchema, List[ProductCreateSchema]],
    user_email: str = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    return await create_product(products, user_email, db)


@router.get("/", response_model=list[ProductResponseSchema])
async def get_products_route(
    response: Response,
    user_email: str = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    products = await get_products(user_email, db)
    response.headers["x-Total-Count"] = str(len(products))
    return products


@router.get("/{product_id}", response_model=ProductResponseSchema)
async def get_product_route(
    product_id: str,
    user_email: str = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    return await get_product(product_id, user_email, db)


@router.put("/{product_id}", response_model=ProductResponseSchema)
async def update_product_route(
    product_id: str,
    product: ProductCreateSchema,
    user_email: str = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    return await update_product(product_id, product, user_email, db)


@router.delete("/{product_id}")
async def delete_product_route(
    product_id: str,
    user_email: str = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    return await delete_product(product_id, user_email, db)
