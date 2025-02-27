from typing import Annotated

from app.backend.db import get_db
from app.models.category import Category
from app.models.product import Product
from app.routers.auth import get_current_user
from app.schemas import CreateProduct
from fastapi import APIRouter, Depends, HTTPException
from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession


from sqlalchemy import select, insert, union_all
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


@prod_router.get('/category/{category_slug}')
async def product_by_category(db: Annotated[AsyncSession, Depends(get_db)], category_slug: str):

    get_main_cat = select(Category).where(Category.slug == category_slug)
    main_cat = await db.scalar(get_main_cat)

    if main_cat:
        get_subcategories = select(Category).filter_by(id=main_cat.id)
        subcategories = await db.scalars(get_subcategories)
        subcategories = subcategories.all()
        subcategories.append(main_cat)

        return [cat.products for cat in subcategories]
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no category found'

        )


@prod_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_product(db: Annotated[AsyncSession, Depends(get_db)], new_product: CreateProduct,
                         get_user: Annotated[dict, Depends(get_current_user)]):

    if get_user.get('is_admin') or get_user.get('is_supplier'):
        query = insert(Product).values(
            name=new_product.name,
            slug=slugify(new_product.name),
            description=new_product.description,
            price=new_product.price,
            image_url=new_product.image_url,
            stock=new_product.stock,
            category_id=new_product.category,
            rating=0,
            supplier_id=get_user.get('id')
        )
        await db.execute(query)
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You must be admin user or supplier for this'
        )


@prod_router.put('/{product_slug}')
async def update_product(db: Annotated[AsyncSession, Depends(get_db)], product_slug: str,
                         update_product_model: CreateProduct, get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user.get('is_admin') or get_user.get('is_supplier'):
        product_update = await db.scalar(select(Product).where(Product.slug == product_slug))
        if product_update is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='There is no product found'
            )
        category = await db.scalar(select(Category).where(Category.id == update_product_model.category))
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='There is no category found'
            )

        product_update.name = update_product_model.name
        product_update.description = update_product_model.description
        product_update.price = update_product_model.price
        product_update.image_url = update_product_model.image_url
        product_update.stock = update_product_model.stock
        product_update.category_id = update_product_model.category
        product_update.slug = slugify(update_product_model.name)

        await db.commit()

        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Product update is successful'
        }


@prod_router.delete('/{product_slug}')
async def delete_product(db: Annotated[AsyncSession, Depends(get_db)], product_slug: str):
    product_delete = await db.scalar(select(Product).where(Product.slug == product_slug))
    if product_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no product found'
        )

    product_delete.is_active = False
    await db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Product delete is successful'
    }
