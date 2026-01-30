from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models.fines import Fine
from app.utils.response import success_response
from app.utils.jwt import get_current_user

router = APIRouter(prefix="/fines", tags=["Fines"])


@router.get("/transaction/{transaction_id}")
def get_fine_by_transaction(transaction_id: int, db: Session = Depends(get_db),user = Depends(get_current_user)):
    if user["role"] not in ["admin", "librarian"]:
      raise HTTPException(403)

    fine = db.query(Fine).filter(
        Fine.transaction_id == transaction_id
    ).first()

    if not fine:
        raise HTTPException(status_code=404, detail="Fine not found")

    return success_response(
        message="Fine fetched successfully",
        data={
            "fine_id": fine.id,
            "transaction_id": fine.transaction_id,
            "amount": fine.amount,
            "paid": fine.paid
        }
    )
