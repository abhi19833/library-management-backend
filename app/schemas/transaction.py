from pydantic import BaseModel

class IssueBook(BaseModel):
    member_id: int
    book_id: int

class ReturnBook(BaseModel):
    transaction_id: int

class RenewBook(BaseModel):
    transaction_id: int
