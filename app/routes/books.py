from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.response import success_response
from app.utils.audit import log_action
from app.deps import get_db
from app.models.books import Book
from app.schemas.book import BookCreate
from app.utils.jwt import get_current_user

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/")
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can add books")

    new_book = Book(
        title=book.title,
        author=book.author,
        quantity=book.quantity,
        department=book.department,
        category=book.category,
        published_year=book.published_year,
        status="available" 
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    log_action(
        db=db,
        action="CREATE",
        entity="Book",
        entity_id=new_book.id
    )

    return success_response(
        message="Book created successfully",
        data=new_book
    )

@router.get("/search")
def search_books(
    query: str,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    offset = (page - 1) * limit
    books = db.query(Book).filter(
        Book.title.ilike(f"%{query}%")
    ).offset(offset).limit(limit).all()

    return success_response(
        message="Books fetched successfully",
        data=books
    )
