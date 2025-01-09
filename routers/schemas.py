from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

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
class UserPostDisplay(BaseDisplay):
    id: int
    username: str

# For post display
class CommentPostDisplay(BaseDisplay):
    id: int
    text: str
    username: str
    timestamp: datetime

class PostDisplay(BaseDisplay):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    timestamp: datetime
    user: UserPostDisplay
    comments: List[CommentPostDisplay]

class UserAuth(BaseModel):
    id: int
    username: str
    email: str

class CommentBase(BaseModel):
    username: str
    text: str
    post_id: int

class CommentDisplay(BaseDisplay):
    id: int
    text: str
    username: str
    timestamp: datetime
    post_id: int