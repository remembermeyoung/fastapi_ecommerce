from fastapi import APIRouter, Depends, HTTPException
from slugify import slugify
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import Annotated
from app.backend.db import get_db
from app.models.category import Category
from app.models.product import Product
from app.schemas import CreateCategory

router = APIRouter(prefix='/categories', tags=['category'])


@router.get('/')
async def get_all_categories(db: Annotated[AsyncSession, Depends(get_db)]):
    query = select(Category).filter_by(is_active=True)
    categories = await db.scalars(query)
    result = categories.all()
    return result


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_category(db: Annotated[AsyncSession, Depends(get_db)], new_cat: CreateCategory):
    query = insert(Category).values(name=new_cat.name,
                                    parent_id=new_cat.parent_id,
                                    slug=slugify(new_cat.name))
    await db.execute(query)
    await db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.put('/')
async def update_category(db: Annotated[AsyncSession, Depends(get_db)],
                          category_id: int, update_category: CreateCategory):
    select_query = select(Category).filter_by(id=category_id)
    category = await db.scalar(select_query)
    if category:
        category.name = update_category.name
        category.slug = slugify(update_category.name)
        category.parent_id = update_category.parent_id
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Category update is successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no category found'
        )


@router.delete('/')
async def delete_category(db: Annotated[AsyncSession, Depends(get_db)], category_id: int):
    select_query = select(Category).filter_by(id=category_id)
    category = await db.scalar(select_query)
    if category:
        category.is_active = False
        await db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Category delete is successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no category found'
        )
