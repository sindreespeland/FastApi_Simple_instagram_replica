from fastapi import APIRouter, Depends
from routers.schemas import UserDisplay, UserBase
from db import db_user
from db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.post('', response_model=UserDisplay)
async def create_user(request: UserBase, db: AsyncSession = Depends(get_db)):
    return await db_user.create_user(db, request)