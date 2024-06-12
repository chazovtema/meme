from functools import lru_cache
from typing import Annotated
from fastapi import Depends

from services.meme_service import MemeServiceImp, MemeService
from database.db import DataBase
from file_storage import MinioStorage
from config import CONFIG


def get_meme_service():
    db = DataBase(CONFIG.database_url)
    db.create()
    file_storage = MinioStorage(
        CONFIG.s3_host, CONFIG.s3_username, CONFIG.s3_password, "memes"
    )
    return MemeServiceImp(db, file_storage)

service = get_meme_service() # creating service

MEME_SERVICE = Annotated[MemeService, Depends(lambda: service)]
