from typing import Annotated

from app.backend.db import get_db
from app.models.category import Category
from app.models.product import Product
from app.schemas import CreateProduct
from fastapi import APIRouter, Depends, HTTPException
from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession


from sqlalchemy import select, insert, union_all
from sqlalchemy.orm import selectinload
from starlette import status

prod_router = APIRouter(prefix='/products', tags=['product'])


@prod_router.get('/')
async def all_products(db: Annotated[AsyncSession, Depends(get_db)]):
    query = select(Product).filter(
        Product.is_active == True & Product.stock > 0
    )
    products = await db.scalars(query)
    if products:
        return products.all()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='There are no products')


@prod_router.get('/{product_slug}')
async def product_detail(db: Annotated[AsyncSession, Depends(get_db)], product_slug: str):
    query = select(Product).filter_by(slug=product_slug)
    product = await db.scalar(query)
    if product:
        return product.all()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='There is no product')


@prod_router.get('/{product_slug}')
async def product_by_category(db: Annotated[AsyncSession, Depends(get_db)], category_slug: str):

    get_subcat = select(Category.id).where(Category.parent_id.in_(
        select(Category.id.where(Category.slug == category_slug))))

    get_subcategories = select(Category).where(
        Category.id.in_(get_subcat))

    get_category = select(Category).where(Category.slug == category_slug)

    query = union_all(get_category, get_subcategories).options(selectinload(Category.products))

    result = await db.scalars(query)
    return result.all()


@prod_router.post('/', status_code=status.HTTP_201_CREATED)
async def all_products(db: Annotated[AsyncSession, Depends(get_db)], new_product: CreateProduct):
    query = insert(Product).values(
        name=new_product.name,
        slug=slugify(new_product.name),
        description=new_product.description,
        price=new_product.price,
        image_url=new_product.image_url,
        stock=new_product.stock,
        category_id=new_product.category,
        rating=0
    )
    await db.execute(query)
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }
