from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Azure OpenAI
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_DEPLOYMENT: str
    AZURE_OPENAI_API_VERSION: str
    
    # Milvus - DISABLED (document search functionality removed)
    # MILVUS_HOST: str = "127.0.0.1"
    # MILVUS_PORT: int = 19530
    # MILVUS_DB: str = "documentdb"
    
    # Auth - will get real UUID from frontend later
    TEST_UUID: str = "00000000-0000-0000-0000-000000TEST"
    
    # Storage
    STORAGE_PATH: str = "./storage"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra env vars

settings = Settings()