import datetime
from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    id: str
    title: str
    content: str
    publisher: str
    category: str
    image_url: str
    created_at: datetime.datetime


class Post(PostCreate):

    class Conifg:
        orm_mode = True


