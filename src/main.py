import uvicorn
from app import app_factory
from api import meme_rt

if __name__=='__main__':
    app = app_factory([meme_rt])
    uvicorn.run(app)