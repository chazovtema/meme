from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base


class DataBase:
    def __init__(self, engine_url: str) -> None:
        self._engine = create_engine(engine_url)
        self._sessionmaker = sessionmaker(self._engine, expire_on_commit=False)

    def create(self):
        Base.metadata.create_all(self._engine)

    def get_session(self):
        return self._sessionmaker()
