from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore
from pydantic import PostgresDsn

class Config(BaseSettings):
    
    model_config = SettingsConfigDict(env_file='src/.env')
    
    database_url: str
    s3_host: str
    s3_username: str
    s3_password: str
    
    
CONFIG = Config()