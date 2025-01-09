from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from routers.schemas import PostBase, PostDisplay
from db.database import get_db
from db import db_post
from typing import List
import random
import string
import aiofiles
from routers.schemas import UserAuth
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/post',
    tags=['post']
)

IMAGE_URL_TYPES = ['absolute', 'relative']

@router.post('', response_model=PostDisplay)
async def create_post(request: PostBase, db: AsyncSession = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    if not request.image_url_type in IMAGE_URL_TYPES:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Paramater image_url_type can only take values: "absolute" or "relative"')
    
    new_post = await db_post.create_post(db, request)

    post_with_user = await db_post.get_post_with_user_and_comments(db, new_post.id)

    return post_with_user

@router.get('/all', response_model=List[PostDisplay])
async def all_post(db: AsyncSession = Depends(get_db)):
    return await db_post.get_all(db)

@router.post('/image')
async def upload_image(image: UploadFile = File(...), current_user: UserAuth = Depends(get_current_user)):
    letters = string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(10))
    new = f"_{rand_str}."
    filename = new.join(image.filename.rsplit('.', 1))
    path = f"images/{filename}"

    async with aiofiles.open(path, 'wb') as buffer:
        while chunk := await image.read(1024 * 1024):
            await buffer.write(chunk)

    return {
        'filename': path
    }

@router.delete('/{id}')
async def delete_post(id: int, db: AsyncSession = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return await db_post.delete_post(db, id, current_user.id)