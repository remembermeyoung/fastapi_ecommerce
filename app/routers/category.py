from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import insert, select, update
from slugify import slugify

from app.backend.db_depends import get_db
from app.schemas import CreateCategory
from app.models.category import Category
from app.models.products import Product
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/categories', tags=['category'])


@router.get('/')
async def get_all_categories(db: Annotated[AsyncSession, Depends(get_db)]):

    categories = await db.scalars(select(Category).where(Category.is_active == True))
    return categories.all()


@router.post('/')
async def create_category(db: Annotated[AsyncSession, Depends(get_db)], 
                          create_category: CreateCategory):
    
    await db.execute(insert(Category).values(name=create_category.name,
                                       parent_id=create_category.parent_id,
                                       slug=slugify(create_category.name)))
    await db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}
    

@router.put('/')
async def update_category(db: Annotated[AsyncSession, Depends(get_db)], 
                          category_id: int, 
                          update_category: CreateCategory):
    
    category = await db.scalar(select(Category).where(Category.id == category_id))
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='There is no category found')

    await db.execute(update(Category).where(Category.id == category_id).values(
            name=update_category.name,
            slug=slugify(update_category.name),
            parent_id=update_category.parent_id))


    await db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Category update is successful'}


@router.delete('/')
async def delete_category(db: Annotated[AsyncSession, Depends(get_db)], category_id: int):

    category = await db.scalar(select(Category).where(Category.id == category_id))
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='There is no category found')
    await db.execute(update(Category).where(Category.id == category_id).values(is_active=False))
    await db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Category delete is successful'}
