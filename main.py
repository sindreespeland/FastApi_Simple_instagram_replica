from fastapi import FastAPI
from db import models
from db.database import engine, Base
from routers import user, post
from fastapi.staticfiles import StaticFiles

async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield

    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(user.router)
app.include_router(post.router)
    
app.mount('/images', StaticFiles(directory='images'), name='images')
