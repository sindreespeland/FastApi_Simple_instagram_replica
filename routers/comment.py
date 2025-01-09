from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from routers.schemas import CommentBase, CommentDisplay
from db.database import get_db
from db import db_comment
from routers.schemas import UserAuth
from auth.oauth2 import get_current_user
from typing import List

router = APIRouter(
    prefix='/comment',
    tags=['comment']
)

@router.post('', response_model=CommentDisplay)
async def create_comment(request: CommentBase, db: AsyncSession = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return await db_comment.create_comment(db, request)
    

@router.get('/all/{post_id}', response_model=List[CommentDisplay])
async def all_comments(post_id: int, db: AsyncSession = Depends(get_db)):
    return await db_comment.get_all(db, post_id)