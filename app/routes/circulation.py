from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.deps import get_db
from app.models.transaction import Transaction
from app.models.books import Book
from app.schemas.transaction import IssueBook, ReturnBook, RenewBook
from app.utils.response import success_response
from app.utils.audit import log_action  
from app.utils.jwt import get_current_user

router = APIRouter(prefix="/circulation", tags=["Circulation"])


@router.post("/issue")
def issue_book(
    data: IssueBook,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    if user["role"] not in ["admin", "librarian"]:
      raise HTTPException(403)

    book = db.query(Book).filter(Book.id == data.book_id).first()
    if not book or book.quantity <= 0:
        raise HTTPException(status_code=400, detail="Book not available")

    transaction = Transaction(
        member_id=data.member_id,
        book_id=data.book_id,
        issue_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=7)
    )

    book.quantity -= 1
    if book.quantity == 0:
        book.status = "issued"   

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    log_action(db, "ISSUE", "Transaction", transaction.id)

    return success_response(message="Book issued successfully")


PER_DAY_FINE = 2


@router.post("/return")
def return_book(
    data: ReturnBook,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    if user["role"] not in ["admin", "librarian"]:
      raise HTTPException(403)

    transaction = db.query(Transaction).filter(
        Transaction.id == data.transaction_id,
        Transaction.status == "issued"
    ).first()

    if not transaction:
        raise HTTPException(status_code=400, detail="Invalid transaction")

    book = db.query(Book).filter(Book.id == transaction.book_id).first()

    transaction.status = "returned"
    transaction.return_date = datetime.utcnow()

    book.quantity += 1
    book.status = "available"

    if transaction.return_date > transaction.due_date:
        late_days = (transaction.return_date - transaction.due_date).days
        fine_amount = late_days * PER_DAY_FINE

        fine = Fine(
            transaction_id=transaction.id,
            amount=fine_amount
        )
        db.add(fine)

    db.commit()

    return success_response(message="Book returned successfully")


@router.post("/renew")
def renew_book(
    data: RenewBook,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    transaction = db.query(Transaction).filter(
        Transaction.id == data.transaction_id,
        Transaction.status == "issued"
    ).first()

    if not transaction:
        raise HTTPException(status_code=400, detail="Cannot renew")

    transaction.status = "renewed"
    db.commit()

    log_action(
        db=db,
        action="RENEW",
        entity="Transaction",
        entity_id=transaction.id
    )

    return success_response(
        message="Book renewed successfully"
    )
