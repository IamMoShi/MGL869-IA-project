from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG: bool = False

    DATABASE_USER: str = Field(..., validation_alias="DATABASE_USER")
    DATABASE_PASSWORD: str = Field(..., validation_alias="DATABASE_PASSWORD")
    DATABASE_HOST: str = Field("localhost", validation_alias="DATABASE_HOST")
    DATABASE_PORT: int = Field(5432, validation_alias="DATABASE_PORT")
    DATABASE_NAME: str = Field(..., validation_alias="DATABASE_NAME")

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
