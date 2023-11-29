import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine, text
from config import settings

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False,
)

session_factory = sessionmaker(sync_engine)
async_session_factory = async_sessionmaker(async_engine)

class Base(DeclarativeBase):
    pass

