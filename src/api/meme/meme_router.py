from typing import Annotated, TypeAlias

from pydantic import Field

from fastapi import APIRouter, Response
from . import schemas

rt = APIRouter(prefix="/memes")

MEME_ID: TypeAlias = Annotated[int, Field(gt=0)]


@rt.get("")
async def get_memes(
    page_number: Annotated[int, Field(gt=0)] = 1,
    page_size: Annotated[int, Field(gt=0, le=100)] = 1,
) -> schemas.ListMemeSchema:
    return schemas.ListMemeSchema(
        page_number=page_number, page_size=page_size, count=10, memes=[]
    )


@rt.get("/{meme_id}")
async def get_meme(meme_id: MEME_ID) -> schemas.MemeSchema:
    return schemas.MemeSchema(id=meme_id, name="Joke")


@rt.post("")
async def create_meme(meme_data: schemas.MemeSchema) -> schemas.MemeSchema:
    return schemas.MemeSchema(id=1, name="test")


@rt.put("/{meme_id}")
async def update_meme(
    meme_id: MEME_ID, data: schemas.UpdateMemeSchema
) -> schemas.MemeSchema:
    return schemas.MemeSchema(id=1, name="test")


@rt.put("/{meme_id}")
async def delete_meme(meme_id: MEME_ID):
    return Response()
