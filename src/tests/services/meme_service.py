import pytest

from services.meme_service import MemeServiceImp
from database.db import DataBase
from database import models

@pytest.fixture
def service():
    db = DataBase("sqlite://")
    db.create()
    serv = MemeServiceImp(db)
    return serv

@pytest.fixture
def big_service():
    db = DataBase("sqlite://")
    db.create()
    with db.get_session() as ses:
        ses.add_all(
            (models.Meme(title='test', author='test') for _ in range(100))
        )
        ses.commit()
    serv = MemeServiceImp(db)
    return serv


def test_create(service: MemeServiceImp):
    meme = service.create_meme('Joke', 'John')
    assert meme.title == 'Joke' and meme.author == 'John'
    
def test_get_meme(big_service: MemeServiceImp):
    meme = big_service.get_meme(1)
    assert meme.id == 1
    
def test_get_memes(big_service: MemeServiceImp):
    res, count = big_service.get_memes(1, 100)
    assert len(res) == 100
    assert count == 100
    
def test_update_meme(big_service: MemeServiceImp):
    new_title = 'Awesome title'
    new_author = 'Ben'
    mem = big_service.update_meme(1, new_title, new_author)
    assert mem.title == new_title and mem.author == new_author
    
def test_delete_meme(big_service: MemeServiceImp):
    big_service.delete_meme(1)
    
    