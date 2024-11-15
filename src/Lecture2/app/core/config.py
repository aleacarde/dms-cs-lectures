import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Settings(BaseSettings):
    API_V1_PATH: str = "/api/v1"
    PROJECT_NAME: str = "Dallas Makerspace Calendar Backend"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "A web application for scheduling classes and events."
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Keycloak Configuration
    KEYCLOAK_SERVER_URL: str = os.getenv("KEYCLOAK_SERVER_URL")
    KEYCLOAK_REALM: str = os.getenv("KEYCLOAK_REALM")
    KEYCLOAK_ISSUER: str = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}"
    KEYCLOAK_CLIENT_ID: str = os.getenv("KEYCLOAK_CLIENT_ID")
    CACHE_TTL_DURATION: int = os.getenv("CACHE_TTL_DURATION")

    # Database settings
    SQLALCHEMY_DATABASE_URI: str = os.getenv("SQLALCHEMY_DATABASE_URI")

    class Config:
        case_sensitive: bool = True

settings = Settings()