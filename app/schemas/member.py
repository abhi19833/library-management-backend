from pydantic import BaseModel, EmailStr

class MemberCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
