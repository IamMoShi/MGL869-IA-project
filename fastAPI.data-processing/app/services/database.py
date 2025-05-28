from datetime import datetime, timedelta, timezone
from typing import Sequence

from app.models.image import Image as DBImage
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_images_since(
    db: AsyncSession, days: int = 0, weeks: int = 0, months: int = 0
) -> Sequence[DBImage]:
    """Return the images created for a certain period of time."""

    now = datetime.now(timezone.utc).replace(tzinfo=None)

    # Calculate time delta
    if months:
        delta = timedelta(days=months * 30 + weeks * 7 + days)
    else:
        delta = timedelta(days=days, weeks=weeks)

    threshold_date = now - delta

    # Build and run the async query
    stmt = (
        select(DBImage)
        .where(DBImage.created_at >= threshold_date)
        .order_by(DBImage.created_at.desc())
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_latest_images(
    db: AsyncSession, limit: int = 1000
) -> Sequence[DBImage]:
    """Return the latest images."""
    stmt = select(DBImage).order_by(DBImage.created_at.desc()).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_random_images(db: AsyncSession, limit: int = 500):
    stmt = select(DBImage).order_by(func.random()).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()
