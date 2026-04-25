from beanie import Document
from pydantic import BaseModel
from typing import Optional

class Food(Document):
    title: str
    descr: Optional[str] = None
    category: str
    owner: str

    class Settings:
        name = "foods"  # MongoDB collection name

class TodoRequest(BaseModel):
    title: str
    desc: Optional[str] = None
    category: str