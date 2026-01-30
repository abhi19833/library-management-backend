from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    quantity: int
    department: str
    category: str
    published_year: int
    quantity: int
    status: str