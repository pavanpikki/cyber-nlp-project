from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings.
    Values can be overridden by environment variables.
    """
    # API metadata
    API_TITLE: str = "Cyber Threat Intelligence API"
    API_DESCRIPTION: str = "An API for extracting CTI from text using NLP."
    API_VERSION: str = "0.1.0"

    # Logging configuration
    LOG_LEVEL: str = "INFO"

    # NLP Service configuration
    SPACY_MODEL: str = "en_core_web_sm"

# Create a single, importable instance of the settings
settings = Settings()