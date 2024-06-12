from typing import Annotated, TypeAlias

from pydantic import Field

from fastapi import APIRouter, Response
from services.models import memes

from .dependensies import MEME_SERVICE

MEME_ID: TypeAlias = Annotated[int, Field(gt=0)]


rt = APIRouter()


@rt.get("/memes")
def get_memes(
    meme_service: MEME_SERVICE,
    page_number: Annotated[int, Field(gt=0)] = 1,
    page_size: Annotated[int, Field(gt=0, le=100)] = 10,
) -> memes.ListMeme:
    res, count = meme_service.get_memes(page_number, page_size)
    return memes.ListMeme(
        page_number=page_number,
        page_size=page_size,
        count=count,
        memes=res,
    )


@rt.get("/memes/{meme_id}")
def get_meme(meme_id: MEME_ID, meme_service: MEME_SERVICE) -> memes.Meme:
    try:
        return meme_service.get_meme(meme_id)
    except ValueError:
        return Response(f'No such meme with id {meme_id}', 404)


@rt.post("/memes", status_code=201)
def create_meme(meme_data: memes.CreateMeme, meme_service: MEME_SERVICE) -> memes.Meme:
    return meme_service.create_meme(meme_data.title, meme_data.author, meme_data.image)


@rt.put("/memes/{meme_id}")
def update_meme(
    meme_id: MEME_ID, data: memes.UpdateMeme, meme_service: MEME_SERVICE
) -> memes.Meme:
    try:
        return meme_service.update_meme(
            meme_id, title=data.title, author=data.author, image=data.image
        )
    except ValueError:
        return Response(f'No such meme with id {meme_id}', 404)


@rt.delete("/memes/{meme_id}")
def delete_meme(meme_id: MEME_ID, meme_service: MEME_SERVICE):
    try:
        meme_service.delete_meme(meme_id)
        return Response()
    except ValueError:
        return Response(f'No such meme with id {meme_id}', 404)
