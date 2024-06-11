from typing import Protocol
from abc import abstractmethod

from .models.memes import Meme


class MemeService(Protocol):
    # @abstractmethod
    def create_meme(self, title: str, author: str) -> Meme: ...

    # @abstractmethod
    def get_memes(self, batch_number: int, batch_count: int) -> list[Meme]: ...

    # @abstractmethod
    def delete_meme(self, id: int): ...

    # @abstractmethod
    def update_meme(
        self, id: int, name: str | None = None, author: str | None = None
    ) -> Meme: ...


class MemeServiceImp(MemeService): ...
