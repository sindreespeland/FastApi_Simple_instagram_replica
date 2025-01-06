from routers.schemas import UserBase
from sqlalchemy.ext.asyncio import AsyncSession
from .models import DbUser
from db.hashing import Hash

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