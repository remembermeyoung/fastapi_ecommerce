from typing import List

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.backend.db import Base, str50, pk


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[pk]
    name: Mapped[str50]
    slug: Mapped[str] = mapped_column(String, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=True)

    products: Mapped[List['Product']] = relationship(back_populates='category')
