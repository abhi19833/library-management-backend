from sqlalchemy import Column, Integer, Boolean, ForeignKey
from app.database import Base

class Fine(Base):
    __tablename__ = "fines"

    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"))
    amount = Column(Integer, nullable=False)
    paid = Column(Boolean, default=False)  # ✅ ADD THIS
