import pytest

from fastapi.testclient import TestClient

from api import meme_rt
from api.meme.dependensies import get_meme_service
from services import MemeService

from app import app_factory
from services.models.memes import Meme


def __create_app():
    class MockMemeService(MemeService):
        def create_meme(self, title: str, author: str) -> Meme:
            return Meme(id=1, title=title, author=author)

        def get_meme(self, meme_id: int) -> Meme:
            return Meme(id=meme_id, title="test", author="test")

        def get_memes(
            self, batch_number: int, batch_count: int
        ) -> tuple[list[Meme], int]:
            start_ind = (batch_number - 1) * batch_count
            start_ind += 1
            memes = [
                Meme(id=start_ind + i, title="test", author="test")
                for i in range(batch_count)
            ]
            return memes, batch_count

        def update_meme(
            self, id: int, title: str | None = None, author: str | None = None
        ) -> Meme:
            if not title:
                title = "test"
            if not author:
                author = "test"
            return Meme(id=id, title=title, author=author)

        def delete_meme(self, id: int):
            return

    app = app_factory([meme_rt])
    app.dependency_overrides[get_meme_service] = lambda: MockMemeService()
    return app


@pytest.fixture
def client():
    app = __create_app()
    cl = TestClient(app)
    return cl


def test_get_meme_by_id(client: TestClient):
    resp = client.get("/memes/1")
    assert resp.status_code == 200


def test_get_memes(client: TestClient):
    resp = client.get("/memes/", params={"page_number": 1, "page_size": 10})
    assert resp.status_code == 200


def test_create_meme(client: TestClient):
    data = {"title": "Tapok", "author": "John"}
    resp = client.post("/memes", json=data)
    assert resp.status_code == 201
    resp_body: dict = resp.json()
    resp_body.pop("id", None)
    assert data == resp_body


def test_update_meme(client: TestClient):
    data = {"title": "new_title", "author": "new_author"}
    resp = client.put("/memes/1", json=data)
    assert resp.status_code == 200
    resp_body: dict = resp.json()
    resp_body.pop("id", None)
    assert resp_body == data


def test_delete_meme(client: TestClient):
    resp = client.delete("/memes/1")
    assert resp.status_code == 200
