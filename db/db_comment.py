from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from datetime import datetime
from fastapi import HTTPException, status
from db.models import DbComment, DbPost
from routers.schemas import CommentBase

async def create_comment(db: AsyncSession, request: CommentBase):
    new_comment = DbComment(
        text = request.text,
        username = request.username,
        post_id = request.post_id,
        timestamp = datetime.now()
    )

    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return new_comment

async def get_all(db: AsyncSession, post_id: int):
    result = await db.execute(select(DbComment).where(DbComment.post_id == post_id))
    comments = result.scalars().all()
    return comments