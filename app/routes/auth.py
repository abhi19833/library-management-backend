from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.response import success_response

from app.deps import get_db
from app.models.users import User
from app.schemas.user import UserCreate, UserLogin
from app.utils.password import hash_password, verify_password
from app.utils.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        email=user.email,
        password=hash_password(user.password),
        role_id=3
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return success_response(
    message="User registered successfully"
)
    
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
        
    token = create_access_token({
    "user_id": db_user.id,
    "role": db_user.role.name
})

    return success_response(
    message="Login successful",
    data={
        "access_token": token,
        "token_type": "bearer"
    }
)

