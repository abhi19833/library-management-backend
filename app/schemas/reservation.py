from pydantic import BaseModel

class ReservationCreate(BaseModel):
    member_id: int
    book_id: int
