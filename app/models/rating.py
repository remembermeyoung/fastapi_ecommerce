from sqlalchemy import ForeignKey, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.backend.db import Base, pk


class Rating(Base):
    __tablename__ = 'rating'
    id: Mapped[pk]
    grade: Mapped[float] = mapped_column(Float)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped['User'] = relationship(back_populates='rating')
    product: Mapped['Product'] = relationship(back_populates='rating')
