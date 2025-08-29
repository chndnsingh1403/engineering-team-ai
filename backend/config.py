import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # LLM Configuration
    llm_provider: str = "openai"
    llm_model: str = "gpt-4-turbo-preview"
    llm_api_key: str
    llm_base_url: str = "https://api.openai.com/v1"
    
    # Demo/Mock Mode (when API quota is exceeded)
    mock_mode: bool = False
    
    # Backward compatibility
    openai_api_key: str = ""
    
    # Server Configuration
    host: str = "localhost" 
    port: int = 8000
    debug: bool = True
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000,http://localhost:3001,http://localhost:3002"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    upload_dir: str = "uploads"
    output_dir: str = "output"
    
    # Additional provider keys (optional)
    anthropic_api_key: str = ""
    azure_openai_endpoint: str = ""
    azure_openai_key: str = ""
    azure_openai_version: str = ""
    ollama_base_url: str = ""
    ollama_model: str = ""
    
    # Agent Configuration
    max_concurrent_agents: int = 5
    agent_timeout: int = 300
    
    # WebSocket Configuration
    ws_heartbeat_interval: int = 30

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # If openai_api_key is provided but llm_api_key is not, use openai_api_key
        if self.openai_api_key and not self.llm_api_key:
            self.llm_api_key = self.openai_api_key

    class Config:
        env_file = ".env"

settings = Settings()
