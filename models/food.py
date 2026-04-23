from beanie import Document
from pydantic import BaseModel
from typing import Optional

class Food(Document):
    id: int
    title: str
    descr: Optional[str] = None
    category: str

    class Settings:
        name = "foods"  # MongoDB collection name