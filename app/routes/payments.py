from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models.payments import Payment
from app.models.fines import Fine
from app.schemas.payment import PaymentCreate
from app.utils.response import success_response
from app.utils.audit import log_action   

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/")
def make_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    fine = db.query(Fine).filter(
        Fine.id == data.fine_id,
        Fine.paid == False
    ).first()

    if not fine:
        raise HTTPException(status_code=400, detail="Invalid or already paid fine")

    payment = Payment(
        fine_id=fine.id,
        amount=fine.amount
    )

    fine.paid = True

    db.add(payment)
    db.commit()
    db.refresh(payment)

    log_action(
        db=db,
        action="PAY",
        entity="Fine",
        entity_id=fine.id
    )

    return success_response(
        message="Fine paid successfully",
        data={
            "payment_id": payment.id,
            "amount_paid": payment.amount
        }
    )
