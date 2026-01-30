from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models.reservation import Reservation
from app.models.books import Book
from app.schemas.reservation import ReservationCreate
from app.utils.response import success_response
from app.utils.audit import log_action   

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.post("/")
def create_reservation(data: ReservationCreate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == data.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book.quantity > 0:
        raise HTTPException(
            status_code=400,
            detail="Book is available, reservation not required"
        )

    reservation = Reservation(
        member_id=data.member_id,
        book_id=data.book_id
    )
    book.status = "reserved"   
    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    log_action(
        db=db,
        action="CREATE",
        entity="Reservation",
        entity_id=reservation.id
    )

    return success_response(
        message="Book reserved successfully",
        data=reservation
    )


@router.post("/{reservation_id}/cancel")
def cancel_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id,
        Reservation.status == "active"
    ).first()

    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    reservation.status = "cancelled"
    db.commit()

    log_action(
        db=db,
        action="CANCEL",
        entity="Reservation",
        entity_id=reservation.id
    )

    return success_response(
        message="Reservation cancelled successfully"
    )
