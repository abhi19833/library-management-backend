from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    fine_id = Column(Integer, ForeignKey("fines.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    paid_at = Column(DateTime, server_default=func.now())
