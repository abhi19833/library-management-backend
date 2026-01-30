from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models.members import Member
from app.schemas.member import MemberCreate
from app.utils.response import success_response
from app.utils.audit import log_action  
from app.utils.jwt import get_current_user

router = APIRouter(prefix="/members", tags=["Members"])


@router.post("/")
def create_member(member: MemberCreate, db: Session = Depends(get_db), user = Depends(get_current_user) ):
    if user["role"] not in ["admin", "librarian"]:
     raise HTTPException(403)

    existing = db.query(Member).filter(Member.email == member.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Member already exists")

    new_member = Member(
        name=member.name,
        email=member.email,
        phone=member.phone,
        role_id=1
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    log_action(
        db=db,
        action="CREATE",
        entity="Member",
        entity_id=new_member.id
    )

    return success_response(
        message="Member created successfully",
        data=new_member
    )


@router.get("/search")
def search_members(query: str, db: Session = Depends(get_db)):
    if user["role"] not in ["admin", "librarian"]:
      raise HTTPException(403)

    members = db.query(Member).filter(
        Member.name.ilike(f"%{query}%")
    ).all()

    return success_response(
        message="Members fetched successfully",
        data=members
    )
