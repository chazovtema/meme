from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base


class DataBase:
    def __init__(self, engine_url: str) -> None:
        self.engine = create_engine(engine_url)
        self.sessionmaker = sessionmaker(self.engine, expire_on_commit=False)

    def create(self):
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.sessionmaker()
