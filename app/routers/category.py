from fastapi import APIRouter, Depends
from slugify import slugify
from sqlalchemy import insert
from sqlalchemy.orm import Session
from starlette import status
from typing import Annotated
from app.backend.db import get_db
from app.models.category import Category
from app.schemas import CreateCategory

router = APIRouter(prefix='/categories', tags=['category'])


@router.get('/')
async def get_all_categories():
    pass


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_category(db: Annotated[Session, Depends(get_db)], new_cat: CreateCategory):
    await db.execute(insert(Category).values(name=new_cat.name,
                                             parent_id=new_cat.parent_id,
                                             slug=slugify(new_cat.name)))
    await db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.put('/')
async def update_category():
    pass


@router.delete('/')
async def delete_category():
    pass
