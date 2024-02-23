from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_host: str='localhost'
    db_user: str='postgres'
    db_upwd: str='postgres'
    db_name: str='postgres'
    secret_key: str='d6299c61f7cd453f495681c4792f660fce02bca6d0bb9bdf13557df29ae307b4'
    algorithm: str='HS256'
    access_token_expire_minutes: int=30

    class Config:
        env_file = '.env'

settings = Settings()