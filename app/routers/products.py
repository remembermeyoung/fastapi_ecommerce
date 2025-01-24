from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from slugify import slugify
from sqlalchemy import insert, select, update
from app.models.products import Product
from app.backend.db_depends import get_db
from app.schemas import CreateProduct
from typing import Annotated
from sqlalchemy.orm import Session

router = APIRouter(prefix='/products', tags=['products'])


@router.get('/')
async def all_products(
    db: Annotated[Session, Depends(get_db)]
):
    query = select(Product).where(Product.is_active == True, Product.stock > 0)
    products = db.scalars(query).all()
    if products is None:
        return JSONResponse({'message': 'There are no product'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return products


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_product(
    db: Annotated[Session, Depends(get_db)],
    new_product: CreateProduct
    ):
    query = insert(Product).values(
        name = new_product.name,
        slug = slugify(new_product.name),
        description = new_product.description,
        price = new_product.price,
        image_url = new_product.image_url,
        stock = new_product.stock,
        rating = 0.0,
        category_id = new_product.category
    )
    db.execute(query)
    db.commit()
    return({
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
        })

@router.get('/{category_slug}')
async def product_by_category(category_slug: str):
    pass


@router.get('/detail/{product_slug}')
async def product_detail(
    product_slug: str,
    db: Annotated[Session, Depends(get_db)]
    ):
    query = select(Product).filter_by(slug=product_slug)
    products = db.scalars(query).all()
    if products is None:
        return JSONResponse({'message': 'There are no product'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return products


@router.put('/{product_slug}')
async def update_product(
    product_slug: str,
    upadte_product: CreateProduct,
    db: Annotated[Session, Depends(get_db)]
    ):
    query = select(Product).filter_by(slug=product_slug)
    product = db.scalar(query)
    if product is None:
        return JSONResponse({'message': 'There is no product found'}, 
                            status=status.HTTP_404_NOT_FOUND)
    else:
        query = update(Product).filter_by(slug=product_slug).values(
            name = upadte_product.name,
            slug = slugify(upadte_product.name),
            description = upadte_product.description,
            price = upadte_product.price,
            image_url = upadte_product.image_url,
            stock = upadte_product.stock,
            category_id = upadte_product.category
        )
        db.execute(query)
        db.commit()
        return(
            {'status_code': status.HTTP_200_OK,
             'transaction': 'Product update is successful'}
        )


@router.delete('/')
async def delete_product(product_id: int):
    pass
