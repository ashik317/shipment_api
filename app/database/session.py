from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from ..config import database_settings, DATABASE_URL


engine = create_async_engine(
    url=database_settings.POSTGRES_URL,
    echo=True,
)

async def create_db_tables():
    async with engine.begin() as connection:
        from app.database import models
        await connection.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async_session = sessionmaker(
        bind=engine, expire_on_commit=False, class_=AsyncSession
    )
    async with engine.begin() as Session:
        yield Session