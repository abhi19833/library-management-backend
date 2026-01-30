from pydantic import BaseModel

class PaymentCreate(BaseModel):
    fine_id: int
