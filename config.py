import os
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'upload')
SRT_DIR = os.path.join(BASE_DIR, 'srt')

class Settings(BaseSettings):
    HUGGINGFACE_TOKEN: str
    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()