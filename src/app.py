from fastapi import FastAPI, APIRouter

def app_factory(routes: list[APIRouter]):
    app = FastAPI()
    for rt in routes:
        app.include_router(rt)
    return app