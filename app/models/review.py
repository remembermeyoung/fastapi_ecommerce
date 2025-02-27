from datetime import datetime as dt

from sqlalchemy import ForeignKey, String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.backend.db import Base, pk


class Review(Base):
    __tablename__ = 'reviews'
    id: Mapped[pk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    rating_id: Mapped[int] = mapped_column(ForeignKey('rating.id'))
    comment: Mapped[str] = mapped_column(Text)
    comment_date: Mapped[dt] = mapped_column(default=dt.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped['User'] = relationship(back_populates='reviews')
    category: Mapped['Product'] = relationship(back_populates='reviews')
    rating: Mapped['Rating'] = relationship(back_populates='reviews')
