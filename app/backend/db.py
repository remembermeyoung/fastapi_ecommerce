import os
from typing import Annotated, AsyncGenerator
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column

from app.backend.config import settings as stg

DATABASE_URL = f"postgresql+asyncpg://{stg.DB_USER}:{stg.DB_PASSWORD}@{stg.DB_HOST}:{stg.DB_PORT}/{stg.DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    #аннотация у генератора Ген[что выдаёт yield, что при завершении генератора]
    async with async_session() as session:
        yield session


class Base(DeclarativeBase):
    pass


pk = Annotated[int, mapped_column(primary_key=True)]
str50 = Annotated[str, mapped_column(String(50))]
