import os
from typing import List, Union, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings using Pydantic v2"""
    
    # App Settings
    APP_NAME: str = Field(default="Doctor-G API")
    VERSION: str = Field(default="1.0.0")
    DEBUG: bool = Field(default=True)
    
    # Security
    SECRET_KEY: str = Field(
        default=""
    )
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(default=10080)  # 7 days
    
    # Database
    DATABASE_URL: str = Field(
        default=""
    )
    
    # API Settings
    API_V1_STR: str = Field(default="/api/v1")
    BACKEND_CORS_ORIGINS: Union[List[str], str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"]
    )
    
    # Groq API
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = Field(default="llama3-70b-8192")
    
    # File Upload
    MAX_UPLOAD_SIZE: int = Field(default=10485760)  # 10MB
    UPLOAD_DIR: str = Field(default="uploads")
    YOLO_MODEL_PATH: str = Field(default="models/lung_nodule_detector.pt")
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse CORS origins from string or list"""
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }
    
    @property
    def ALLOWED_EXTENSIONS(self) -> set:
        return {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".dcm"}


settings = Settings()

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)