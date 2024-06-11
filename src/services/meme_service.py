from typing import Protocol
from abc import abstractmethod

from sqlalchemy import select, func


from .models.memes import Meme
from database.db import DataBase
from database import models


class MemeService(Protocol):
    @abstractmethod
    def create_meme(self, title: str, author: str) -> Meme: ...

    @abstractmethod
    def get_meme(self, meme_id: int) -> Meme: ...

    @abstractmethod
    def get_memes(
        self, batch_number: int, batch_count: int
    ) -> tuple[list[Meme], int]: ...

    @abstractmethod
    def delete_meme(self, id: int): ...

    @abstractmethod
    def update_meme(
        self, id: int, title: str | None = None, author: str | None = None
    ) -> Meme: ...


class MemeServiceImp(MemeService):
    def __init__(self, database: DataBase) -> None:
        self.db = database

    def create_meme(self, title: str, author: str) -> Meme:
        with self.db.get_session() as ses:
            mem = models.Meme(title=title, author=author)
            ses.add(mem)
            ses.commit()
            return Meme.model_validate(mem, from_attributes=True)

    def get_meme(self, meme_id: int) -> Meme:
        with self.db.get_session() as ses:
            res = ses.scalar(select(models.Meme))
            if not res:
                raise ValueError(f"No such meme with id {meme_id}")
            return Meme.model_validate(res, from_attributes=True)

    def get_memes(self, batch_number: int, batch_count: int) -> list[Meme]:
        with self.db.get_session() as ses:
            offset = batch_count * (batch_number - 1)
            query = select(models.Meme).limit(batch_count).offset(offset)
            res = ses.scalars(query)
            count = ses.execute(select(func.count()).select_from(models.Meme))
            return [Meme.model_validate(i, from_attributes=True) for i in res], next(count)[0]

    def update_meme(
        self, id: int, title: str | None = None, author: str | None = None
    ) -> Meme:
        with self.db.get_session() as ses:
            mem = ses.scalar(select(models.Meme).where(models.Meme.id == id))
            if not mem:
                raise ValueError(f"No such meme with id {id}")
            if title:
                mem.title = title
            if author:
                mem.author = author
            ses.commit()
            return Meme.model_validate(mem, from_attributes=True)

    def delete_meme(self, id: int):
        with self.db.get_session() as ses:
            mem = ses.scalar(select(models.Meme).where(models.Meme.id == id))
            if not mem:
                raise ValueError(f"No such meme with id {id}")
            ses.delete(mem)
            ses.commit()
