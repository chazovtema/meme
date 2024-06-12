import base64
from typing import Any

from pydantic import BaseModel, Base64Bytes, Base64Str, field_serializer


class Base(BaseModel):
    ...

class BaseMeme(Base):
    
    ...

class Meme(BaseMeme):
    id: int
    title: str
    author: str
    image: bytes
    
    @field_serializer('image')
    def serialize_image(self, image: bytes):
        return base64.b64encode(image).decode('ascii')



class ListMeme(Base):
    page_number: int
    page_size: int
    count: int
    memes: list[Meme]


class CreateMeme(BaseMeme):
    title: str
    author: str
    image: Base64Bytes


class UpdateMeme(BaseMeme):
    title: str | None = None
    author: str | None = None
    image: Base64Bytes | None = None
