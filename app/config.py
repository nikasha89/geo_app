# app/config.py
from pydantic import BaseSettings, Field

title_app = "API - GeoApp"
description_app = "API - GIS - GeoAPP"
version_app = "3.8.0"


def get_srid():
    return 4326


class Settings(BaseSettings):
    db_url: str = Field(..., env='DATABASE_URL')


settings = Settings()
