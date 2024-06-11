from pydantic import BaseModel


class Base(BaseModel): ...


class Meme(Base):
    id: int
    title: str
    author: str


class ListMeme(Base):
    page_number: int
    page_size: int
    count: int
    memes: list[Meme]


class CreateMeme(Base):
    title: str
    author: str


class UpdateMeme(Base):
    
    title: str | None = None
    author: str | None = None
