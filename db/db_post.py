from routers.schemas import PostBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from .models import DbPost
from datetime import datetime

async def create_post(db: AsyncSession, request: PostBase):
    new_post = DbPost(
        image_url = request.image_url,
        image_url_type = request.image_url_type,
        caption = request.caption,
        timestamp = datetime.now(),
        user_id = request.creator_id
    )

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)

    return new_post

async def get_post_with_user(db: AsyncSession, post_id: int) -> DbPost:
    result = await db.execute(
        select(DbPost).options(selectinload(DbPost.user)).where(DbPost.id == post_id)
    )
    post = result.scalar_one_or_none()
    return post

async def get_all(db: AsyncSession):
    result = await db.execute(select(DbPost).options(selectinload(DbPost.user)))
    posts = result.scalars().all()
    return posts