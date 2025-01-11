from routers.schemas import PostBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from .models import DbPost
from datetime import datetime
from fastapi import HTTPException, status

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

async def get_post_with_user_and_comments(db: AsyncSession, post_id: int) -> DbPost:
    result = await db.execute(
        select(DbPost)
        .options(
            selectinload(DbPost.user),
            selectinload(DbPost.comments)
        )
        .where(DbPost.id == post_id)
    )
    post = result.scalar_one_or_none()
    return post

async def get_all(db: AsyncSession):
    result = await db.execute(
        select(DbPost)
        .options(
            selectinload(DbPost.user),      # Eagerly load user relationship
            selectinload(DbPost.comments)   # Eagerly load comments relationship
        )
    )
    posts = result.scalars().all()
    return posts


async def delete_post(db: AsyncSession, id: int, user_id: int):
    result = await db.execute(select(DbPost).where(DbPost.id == id))
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    if post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this post"
        )
    
    await db.delete(post)
    await db.flush()
    await db.commit()

