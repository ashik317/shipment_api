from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from ..config import DATABASE_URL


engine = create_async_engine(
    url=DATABASE_URL,  # ← fix here
    echo=True,
)

async def create_db_tables():
    async with engine.begin() as connection:
        from app.database import models
        await connection.run_sync(SQLModel.metadata.create_all)


async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_session():
    async with async_session() as session:
        yield session