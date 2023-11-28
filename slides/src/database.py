from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text
from config import settings

engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=False,
    # pool_size=5,
    # max_overflow=10
)

with engine.connect() as conn:
    res = conn.execute(text("SELECT 1,2,3 union select 4,5,6"))
    print(f"{res.first()=}")