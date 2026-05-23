import os
from typing import Optional

class Settings:
    def __init__(self):
        self.DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./database.db")

settings = Settings()
