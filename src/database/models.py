from typing import dataclass_transform, TypeVar

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

T = TypeVar("T")


@dataclass_transform(kw_only_default=True)
def nice_init(cls: type[T]) -> type[T]:
    return cls


class Base(DeclarativeBase): ...


@nice_init
class Meme(Base):
    
    __tablename__ = 'memes'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    author: Mapped[str] = mapped_column()
