from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)

    issue_date = Column(DateTime, server_default=func.now())
    due_date = Column(DateTime) 
    return_date = Column(DateTime, nullable=True)
    status = Column(String, default="issued")  
