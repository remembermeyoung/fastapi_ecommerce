from fastapi import APIRouter, Depends, HTTPException
from slugify import slugify
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import Annotated
from app.backend.db import get_db
from app.models.category import Category
from app.models.product import Product
from app.routers.auth import get_current_user
from app.schemas import CreateCategory

cat_router = APIRouter(prefix='/categories', tags=['category'])


@cat_router.get('/')
async def get_all_categories(db: Annotated[AsyncSession, Depends(get_db)]):
    query = select(Category).filter_by(is_active=True)
    categories = await db.scalars(query)
    result = categories.all()
    return result


@cat_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_category(db: Annotated[AsyncSession, Depends(get_db)], new_cat: CreateCategory,
                          get_user: Annotated[dict, Depends(get_current_user)]):

    if get_user.get('is_admin'):

        query = insert(Category).values(name=new_cat.name,
                                        parent_id=new_cat.parent_id,
                                        slug=slugify(new_cat.name))
        await db.execute(query)
        await db.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
        }
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You must be admin user for this')


@cat_router.put('/')
async def update_category(db: Annotated[AsyncSession, Depends(get_db)], category_id: int,
                          update_category: CreateCategory, get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user.get('is_admin'):
        category = await db.scalar(select(Category).where(Category.id == category_id))
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='There is no category found'
            )

        category.name = update_category.name
        category.slug = slugify(update_category.name)
        category.parent_id = update_category.parent_id
        await db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Category update is successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You must be admin user for this'
        )


@cat_router.delete('/')
async def delete_category(db: Annotated[AsyncSession, Depends(get_db)], category_id: int,
                          get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user.get('is_admin'):
        category = await db.scalar(select(Category).where(Category.id == category_id))
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='There is no category found'
            )
        category.is_active = False
        await db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Category delete is successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You must be admin user for this'
        )
