from typing import Annotated, TypeAlias

from pydantic import Field

from fastapi import APIRouter, Response
from services.models import memes

from services.meme_service import MemeService


MEME_ID: TypeAlias = Annotated[int, Field(gt=0)]


def meme_route_factory(meme_service: MemeService):
    rt = APIRouter()

    @rt.get("/memes")
    async def get_memes(
        page_number: Annotated[int, Field(gt=0)] = 1,
        page_size: Annotated[int, Field(gt=0, le=100)] = 1,
    ) -> memes.ListMeme:
        res = meme_service.get_memes(page_number, page_size)
        return memes.ListMeme(
            page_number=page_number,
            page_size=page_size,
            count=(page_number + 1) * page_size,
            memes=[res],
        )

    @rt.get("/memes/{meme_id}")
    async def get_meme(meme_id: MEME_ID) -> memes.Meme:
        return meme_service.get_meme(meme_id)

    @rt.post("/memes")
    async def create_meme(meme_data: memes.CreateMeme) -> memes.Meme:
        return meme_service.create_meme(meme_data.title, meme_data.author)

    @rt.put("/memes/{meme_id}")
    async def update_meme(meme_id: MEME_ID, data: memes.UpdateMeme) -> memes.Meme:
        return meme_service.update_meme(meme_id, title=data.title, author=data.author)

    @rt.delete("/memes/{meme_id}")
    async def delete_meme(meme_id: MEME_ID):
        meme_service.delete_meme(meme_id)
        return Response()

    return rt
