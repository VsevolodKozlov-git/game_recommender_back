import os


class Settings: # type: ignore
    def get_url(self) -> str:
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD", "postgres")
        db = os.getenv("POSTGRES_DB", "postgres")
        server = os.getenv("POSTGRES_SERVER", "db")
        port = os.getenv("POSTGRES_PORT", "5432")
        return f"postgresql+asyncpg://{user}:{password}@{server}:{port}/{db}"

settings = Settings()