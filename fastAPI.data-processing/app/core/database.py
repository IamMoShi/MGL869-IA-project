from app.core.config import settings
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# Creation of the Async engine
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)

# Create a sessionmaker async (CAUTION: async_ssessionmaker, not sessionmaker)
AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


# Fastapi dependence
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        return session
