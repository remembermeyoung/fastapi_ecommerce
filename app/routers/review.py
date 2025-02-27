from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from select import select
from sqlalchemy import insert, update, func, cast
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.backend.db import get_db
from app.models.product import Product
from app.models.rating import Rating
from app.models.review import Review
from app.routers.auth import get_current_user
from app.schemas import ReviewSchema

review_router = APIRouter(prefix='/review', tags=['product'])


@review_router.get('/')
async def all_reviews(db: Annotated[AsyncSession, Depends(get_db)]):
    reviews = await db.scalars(select(Review).filter_by(is_active=True))
    if reviews:
        return reviews.all()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='There are no reviews')


@review_router.post('/{product_slug}')
async def add_review(db: Annotated[AsyncSession, Depends(get_db)],
                     get_user: Annotated[dict, Depends(get_current_user)],
                     product_slug: str, review: ReviewSchema):
    if get_user.get('id'):
        product = await db.scalar(select(Product).filter_by(slug=product_slug))
        if product:
            rating_model = Rating(grade=review.rating, user_id=get_user.get('id'), product_id=product.id)
            db.add(rating_model)
            await db.flush()

            await db.execute(insert(Review).values(
                user_id=get_user.get('id'),
                product_id=product.id,
                rating_id=rating_model.id,
                comment=review.comment
            ))

            new_rating = await db.scalar(
                select(func.avg(Rating.grade).label('new_rating')).
                filter_by(product_id=product.id).
                group_by(Rating.product_id)
            )

            await db.execute(update(Product).values(
                rating=new_rating
            ))

            await db.commit()

        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='There is no product')
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='You are not authorized for this actions')
# - add_review - Метод добавления отзыва и рейтинга об определенном товаре. Разрешен доступ только пользователям.
# В результате добавления отзыва, рейтинг товара должен быть пересчитан (поле rating модели Product)



# - delete_reviews - Метод удаления отзыва и рейтинга об определенном товаре.
# Доступ разрешен только администратору. При удалении поле is_active должно изменяться на False для  отзыва и рейтинга.