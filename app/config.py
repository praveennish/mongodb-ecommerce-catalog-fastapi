from pydantic import BaseModel, AnyHttpUrl
from typing import List
import os

class Settings(BaseModel):
   app_name: str = os.getenv("APP_NAME", "ecommerce-catalog-api")
   app_env: str = os.getenv("APP_ENV", "development")
   host: str = os.getenv("HOST", "0.0.0.0")
   port: int = int(os.getenv("PORT", 8000))

   mongo_uri:str = os.getenv("MONGO_URI", "mongodb://mongo:27017")
   mongo_db:str = os.getenv("MONGO_DB", "catalog_api")
   mongo_min_pool_size: int = int(os.getenv("MONGO_MIN_POOL_SIZE", 1))
   mongo_max_pool_size: int = int(os.getenv("MONGO_MAX_POOL_SIZE", 10)) 

   cors_origins: List[str] = os.getenv("CORS_ORIGINS", "").split(",") if os.getenv("CORS_ORIGINS") else []
   
settings = Settings()