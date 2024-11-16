from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

engine = create_async_engine(os.getenv('DATABASE_URL'), echo=True)
async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
