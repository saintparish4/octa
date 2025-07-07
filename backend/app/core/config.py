from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "OCTA"
    debug: bool = False
    
    # Database settings
    database_url: str = "postgresql://postgres:postgres@localhost:5432/postgres"
    
    # Neo4j settings
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "networkpass"
    
    # Redis settings
    redis_url: str = "redis://localhost:6379"
    
    class Config:
        env_file = ".env"

settings = Settings() 