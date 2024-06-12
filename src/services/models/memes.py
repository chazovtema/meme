from pydantic import BaseModel, Base64Bytes


class Base(BaseModel): ...


class Meme(Base):
    id: int
    title: str
    author: str
    image: Base64Bytes


class ListMeme(Base):
    page_number: int
    page_size: int
    count: int
    memes: list[Meme]


class CreateMeme(Base):
    title: str
    author: str
    image: Base64Bytes


class UpdateMeme(Base):
    
    title: str | None = None
    author: str | None = None
    image: Base64Bytes | None = None
