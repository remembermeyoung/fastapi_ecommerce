from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.backend.db import Base
from sqlalchemy import String, Boolean
from app.backend.db import pk, str50


class User(Base):
    __tablename__ = 'users'

    id: Mapped[pk]
    first_name: Mapped[str50]
    last_name: Mapped[str50]
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_supplier: Mapped[bool] = mapped_column(Boolean, default=False)
    is_customer: Mapped[bool] = mapped_column(Boolean, default=True)

    products: Mapped[List['Product']] = relationship(back_populates='user')
    