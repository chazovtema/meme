from fastapi import FastAPI, APIRouter

import api

app = FastAPI()
for rt in api.__dict__.values():
    if isinstance(rt, APIRouter):
        app.include_router(rt)