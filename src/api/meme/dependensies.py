from functools import lru_cache
from typing import Annotated
from fastapi import Depends

from services.meme_service import MemeServiceImp, MemeService
from database.db import DataBase

@lru_cache
def get_meme_service():
    db = DataBase('sqlite://')
    db.create()
    return MemeServiceImp(db)

MEME_SERVICE = Annotated[MemeService, Depends(get_meme_service)]