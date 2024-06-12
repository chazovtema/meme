from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn

class Config(BaseSettings):
    
    model_config = SettingsConfigDict(env_file='src/.env')
    
    database_url: str
    
    
CONFIG = Config()