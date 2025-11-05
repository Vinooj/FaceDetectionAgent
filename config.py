"""Configuration settings for Face Detection and Identification Application."""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass


@dataclass
class ServerConfig:
    """MCP Server configuration."""
    host: str = os.getenv("MCP_HOST", "127.0.0.1")
    port: int = int(os.getenv("MCP_PORT", 8000))
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    workers: int = int(os.getenv("MCP_WORKERS", 1))
    
    @property
    def url(self) -> str:
        """Get server URL."""
        return f"http://{self.host}:{self.port}"


@dataclass
class StreamlitConfig:
    """Streamlit configuration."""
    port: int = int(os.getenv("STREAMLIT_PORT", 8501))
    address: str = os.getenv("STREAMLIT_ADDRESS", "127.0.0.1")
    debug: bool = os.getenv("STREAMLIT_DEBUG", "False").lower() == "true"
    
    @property
    def url(self) -> str:
        """Get Streamlit URL."""
        return f"http://{self.address}:{self.port}"


@dataclass
class OllamaConfig:
    """Ollama configuration."""
    host: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    model: str = os.getenv("OLLAMA_MODEL", "qwen3-vl:235b-cloud")
    timeout: int = int(os.getenv("OLLAMA_TIMEOUT", 300))
    
    @property
    def is_available(self) -> bool:
        """Check if Ollama is available."""
        try:
            import requests
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False


@dataclass
class PathConfig:
    """Path configuration."""
    root_dir: Path = Path(__file__).parent
    temp_dir: Path = Path(os.getenv("TEMP_DIR", "/tmp/face_detection"))
    log_dir: Path = Path(os.getenv("LOG_DIR", "logs"))
    
    def __post_init__(self):
        """Create necessary directories."""
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)


@dataclass
class DetectionConfig:
    """Face detection configuration."""
    min_confidence: float = float(os.getenv("MIN_CONFIDENCE", 0.5))
    min_face_size: int = int(os.getenv("MIN_FACE_SIZE", 20))
    gpu_enabled: bool = os.getenv("GPU_ENABLED", "False").lower() == "true"
    
    # RetinaFace specific settings
    model_name: str = os.getenv("DETECTION_MODEL", "resnet50")
    nms_threshold: float = float(os.getenv("NMS_THRESHOLD", 0.4))


@dataclass
class IdentificationConfig:
    """Face identification configuration."""
    model_name: str = os.getenv("IDENTIFICATION_MODEL", "qwen3-vl:235b-cloud")
    confidence_threshold: float = float(os.getenv("ID_CONFIDENCE", 0.7))
    max_retries: int = int(os.getenv("MAX_RETRIES", 3))
    retry_delay: int = int(os.getenv("RETRY_DELAY", 2))


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = os.getenv("LOG_LEVEL", "INFO")
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    enable_file: bool = os.getenv("LOG_TO_FILE", "True").lower() == "true"
    enable_console: bool = os.getenv("LOG_TO_CONSOLE", "True").lower() == "true"


@dataclass
class AppConfig:
    """Main application configuration."""
    # Sub-configurations
    server: ServerConfig = None
    streamlit: StreamlitConfig = None
    ollama: OllamaConfig = None
    paths: PathConfig = None
    detection: DetectionConfig = None
    identification: IdentificationConfig = None
    logging: LoggingConfig = None
    
    # Application settings
    app_name: str = "Face Detection and Identification"
    version: str = "0.1.0"
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    def __post_init__(self):
        """Initialize sub-configurations if not provided."""
        if self.server is None:
            self.server = ServerConfig()
        if self.streamlit is None:
            self.streamlit = StreamlitConfig()
        if self.ollama is None:
            self.ollama = OllamaConfig()
        if self.paths is None:
            self.paths = PathConfig()
        if self.detection is None:
            self.detection = DetectionConfig()
        if self.identification is None:
            self.identification = IdentificationConfig()
        if self.logging is None:
            self.logging = LoggingConfig()
    
    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment == "development"
    
    @property
    def is_testing(self) -> bool:
        """Check if running in testing."""
        return self.environment == "testing"


# Global configuration instance
_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """Get or create the global configuration."""
    global _config
    if _config is None:
        _config = AppConfig()
    return _config


def reset_config() -> None:
    """Reset the global configuration (useful for testing)."""
    global _config
    _config = None


# Convenience functions
def get_server_config() -> ServerConfig:
    """Get server configuration."""
    return get_config().server


def get_streamlit_config() -> StreamlitConfig:
    """Get Streamlit configuration."""
    return get_config().streamlit


def get_ollama_config() -> OllamaConfig:
    """Get Ollama configuration."""
    return get_config().ollama


def get_paths_config() -> PathConfig:
    """Get paths configuration."""
    return get_config().paths


def get_detection_config() -> DetectionConfig:
    """Get detection configuration."""
    return get_config().detection


def get_identification_config() -> IdentificationConfig:
    """Get identification configuration."""
    return get_config().identification


def get_logging_config() -> LoggingConfig:
    """Get logging configuration."""
    return get_config().logging


# Example usage
if __name__ == "__main__":
    config = get_config()
    
    print(f"App: {config.app_name} v{config.version}")
    print(f"Environment: {config.environment}")
    print(f"MCP Server: {config.server.url}")
    print(f"Streamlit: {config.streamlit.url}")
    print(f"Ollama: {config.ollama.host}")
    print(f"Ollama Available: {config.ollama.is_available}")
    print(f"Temp Directory: {config.paths.temp_dir}")
    print(f"Log Directory: {config.paths.log_dir}")
    print(f"Detection Min Confidence: {config.detection.min_confidence}")
    print(f"Identification Model: {config.identification.model_name}")
