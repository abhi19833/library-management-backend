from pydantic import BaseModel

class FineCreate(BaseModel):
    transaction_id: int
    amount: int
