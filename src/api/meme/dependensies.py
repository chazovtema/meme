from functools import lru_cache
from typing import Annotated
from fastapi import Depends

from services.meme_service import MemeServiceImp, MemeService
from database.db import DataBase
from config import CONFIG

@lru_cache
def get_meme_service():
    db = DataBase(CONFIG.database_url)
    db.create()
    return MemeServiceImp(db)

MEME_SERVICE = Annotated[MemeService, Depends(get_meme_service)]