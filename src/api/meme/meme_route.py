from typing import Annotated, TypeAlias

from pydantic import Field

from fastapi import APIRouter, Response
from services.models import memes

from services.meme_service import MemeService
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
def get_meme(
    meme_id: MEME_ID, meme_service: MEME_SERVICE
) -> memes.Meme:
    return meme_service.get_meme(meme_id)


@rt.post("/memes", status_code=201)
def create_meme(
    meme_data: memes.CreateMeme, meme_service:  MEME_SERVICE
) -> memes.Meme:
    return meme_service.create_meme(meme_data.title, meme_data.author)


@rt.put("/memes/{meme_id}")
def update_meme(
    meme_id: MEME_ID, data: memes.UpdateMeme, meme_service: MEME_SERVICE
) -> memes.Meme:
    return meme_service.update_meme(meme_id, title=data.title, author=data.author)


@rt.delete("/memes/{meme_id}")
def delete_meme(meme_id: MEME_ID, meme_service: MEME_SERVICE):
    meme_service.delete_meme(meme_id)
    return Response()
