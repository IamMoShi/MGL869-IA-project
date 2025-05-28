from pydantic_settings import BaseSettings


# pylint: disable=too-few-public-methods
class Settings(BaseSettings):
    """Settings class."""

    MODEL_PATH: str = "models/model.pt"
    DEBUG: bool = False

    # pylint: disable=too-few-public-methods
    class Config:
        """Config class."""

        env_file = ".env"


settings = Settings()
