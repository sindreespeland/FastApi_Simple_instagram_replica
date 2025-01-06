from pydantic import BaseModel
from datetime import datetime

class BaseDisplay(BaseModel):
    class Config():
        from_attributes = True



class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserDisplay(BaseDisplay):
    id: int
    username: str
    email: str

class PostBase(BaseModel):
    image_url: str
    image_url_type: str
    caption: str
    creator_id: int

# For post display
class UserPostDisplay(BaseModel):
    id: int
    username: str

class PostDisplay(BaseDisplay):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    timestamp: datetime
    user: UserPostDisplay