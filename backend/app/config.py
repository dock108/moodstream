from pydantic import BaseSettings


class Settings(BaseSettings):
    gpt_api_key: str | None = None
    tmdb_api_key: str | None = None
    allowed_origins: str = "http://localhost:3000"

    class Config:
        env_file = ".env"

    @property
    def origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.allowed_origins.split(",")
            if origin.strip()
        ]


settings = Settings()
