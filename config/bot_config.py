from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    telegram_token: SecretStr

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

config = Settings()
