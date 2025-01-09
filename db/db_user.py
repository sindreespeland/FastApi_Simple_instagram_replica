from routers.schemas import UserBase
from sqlalchemy.ext.asyncio import AsyncSession
from .models import DbUser
from db.hashing import Hash
from fastapi import HTTPException, status
from sqlalchemy.future import select

async def create_user(db: AsyncSession, request: UserBase):
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(DbUser).where(DbUser.username == username))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with username {username} not found')
    
    return user