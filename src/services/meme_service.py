from typing import Protocol
from abc import abstractmethod

from sqlalchemy import select, func


from .models.memes import Meme
from database.db import DataBase
from database import models

from file_storage import FileStorage


class MemeService(Protocol):
    @abstractmethod
    def create_meme(self, title: str, author: str, image: bytes) -> Meme: ...

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
        self,
        id: int,
        title: str | None = None,
        author: str | None = None,
        image: bytes | None = None,
    ) -> Meme: ...


class MemeServiceImp(MemeService):
    def __init__(self, database: DataBase, file_storage: FileStorage) -> None:
        self.db = database
        self.file_storage = file_storage

    def create_meme(self, title: str, author: str, image: bytes) -> Meme:
        with self.db.get_session() as ses:
            mem = models.Meme(title=title, author=author)
            ses.add(mem)
            ses.flush()
            self.file_storage.upload_file(str(mem.id), image)
            ses.commit()
            mem.image = image  # type: ignore # for validating
            model = Meme.model_validate(mem, from_attributes=True)
            return model

    def get_meme(self, meme_id: int) -> Meme:
        with self.db.get_session() as ses:
            res = ses.scalar(select(models.Meme))
            if not res:
                raise ValueError(f"No such meme with id {meme_id}")
            image = self.file_storage.get_file(str(meme_id))
            res.image = image  # type: ignore # for validating
            return Meme.model_validate(res, from_attributes=True)

    def get_memes(self, batch_number: int, batch_count: int) -> tuple[list[Meme], int]:
        with self.db.get_session() as ses:
            offset = batch_count * (batch_number - 1)
            query = select(models.Meme).limit(batch_count).offset(offset)
            res = ses.scalars(query)
            count = ses.execute(select(func.count()).select_from(models.Meme))
            memes = []
            for i in res:
                image = self.file_storage.get_file(str(i.id))
                i.image = image  # type: ignore # for validating
                memes.append(Meme.model_validate(i, from_attributes=True))
            return (
                memes,
                next(count)[0],
            )

    def update_meme(
        self,
        id: int,
        title: str | None = None,
        author: str | None = None,
        image: bytes | None = None,
    ) -> Meme:
        with self.db.get_session() as ses:
            mem = ses.scalar(select(models.Meme).where(models.Meme.id == id))
            if not mem:
                raise ValueError(f"No such meme with id {id}")
            if title:
                mem.title = title
            if author:
                mem.author = author
            if image is not None:
                self.file_storage.upload_file(str(id), image)
            mem.image = self.file_storage.get_file(str(id))  # type: ignore # for validating
            ses.commit()
            return Meme.model_validate(mem, from_attributes=True)

    def delete_meme(self, id: int):
        with self.db.get_session() as ses:
            mem = ses.scalar(select(models.Meme).where(models.Meme.id == id))
            if not mem:
                raise ValueError(f"No such meme with id {id}")
            ses.delete(mem)
            self.file_storage.delete_file(str(id))
            ses.commit()
