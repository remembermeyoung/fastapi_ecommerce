from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.backend.db import Base, str50, pk


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[pk]
    name: Mapped[str50]
    slug = Column(String, unique=True, index=True)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)
    image_url: Mapped[str] = mapped_column(String)
    stock: Mapped[int] = mapped_column(Integer)
    rating: Mapped[float] = mapped_column(Float)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    supplier_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped['User'] = relationship(back_populates='products')
    category: Mapped['Category'] = relationship(back_populates='products')
    reviews: Mapped[List['Review']] = relationship(back_populates='products')
    ratings: Mapped[List['Rating']] = relationship(back_populates='products')


