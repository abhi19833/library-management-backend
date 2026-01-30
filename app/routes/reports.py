from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models.transaction import Transaction
from app.utils.jwt import get_current_user

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/issued")
def issued_books(db: Session = Depends(get_db),user = Depends(get_current_user)):
    if user["role"] != "admin":
      raise HTTPException(403)

    return db.query(Transaction).filter(Transaction.status == "issued").all()
    
@router.get("/returned")
def returned_books(db: Session = Depends(get_db),user = Depends(get_current_user) ):
    if user["role"] != "admin":
      raise HTTPException(403)

    return db.query(Transaction).filter(Transaction.status == "returned").all()
