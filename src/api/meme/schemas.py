from pydantic import BaseModel


class MemeSchema(BaseModel):
    id: int
    name: str


class ListMemeSchema(BaseModel):
    page_number: int
    page_size: int
    count: int
    memes: list[MemeSchema]


class CreateMemeSchema(BaseModel):
    name: str


class UpdateMemeSchema(BaseModel): ...
