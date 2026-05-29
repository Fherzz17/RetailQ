from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATABASE_URL = f"sqlite:///{BASE_DIR / 'retailiq.db'}"


def get_database_url() -> str:
    return os.getenv("RETAILIQ_DATABASE_URL", DEFAULT_DATABASE_URL)

