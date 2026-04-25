from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from .config import database_settings, DATABASE_URL


engine = create_async_engine(
    url=DATABASE_URL,  # ← use DATABASE_URL directly
    echo=True,
)

async def create_db_tables():
    async with engine.begin() as connection:
        from .models import Shipment
        await connection.run_sync(SQLModel.metadata.create_all)


async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session():
    async with async_session() as session:
        yield session