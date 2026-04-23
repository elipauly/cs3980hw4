from beanie import Document
from pydantic import BaseModel
from typing import Optional

class User(Document):
    username: str
    password: str

    class Settings:
        name = "users"