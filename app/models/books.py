from sqlalchemy import Column, Integer, String
from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    quantity = Column(Integer)
    department = Column(String, nullable=False)  
    category = Column(String)
    published_year = Column(Integer)
    status = Column(String, default="available") 
