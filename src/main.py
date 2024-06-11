import uvicorn
from app import app_factory
from api import meme_route_factory
from services.meme_service import MemeServiceImp

if __name__=='__main__':
    meme_rt = meme_route_factory(MemeServiceImp())
    app = app_factory([meme_rt])
    uvicorn.run(app)