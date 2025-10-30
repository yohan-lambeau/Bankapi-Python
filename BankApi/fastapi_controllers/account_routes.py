# fastapi_controllers/account_routes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from BankApi.repository.database import SessionLocal
from BankApi.models.account_model import Account

router = APIRouter(prefix="/api", tags=["accounts"])

# ----- Schémas -----
class AccountBase(BaseModel):
    account_number: str
    balance: float

class AccountCreate(BaseModel):
    account_number: str
    balance: float

class AccountRead(AccountBase):
    id: int
    client_id: int

    class Config:
        from_attributes = True

# ----- Dépendance DB -----
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----- Routes -----
@router.get("/accounts", response_model=List[AccountRead])
def get_all_accounts(db: Session = Depends(get_db)):
    return db.query(Account).all()

@router.get("/account/{account_id}", response_model=AccountRead)
def get_account_by_id(account_id: int, db: Session = Depends(get_db)):
    account = db.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.post("/create_account", response_model=AccountRead, status_code=201)
def create_account(payload: AccountCreate, db: Session = Depends(get_db)):
    account = Account(**payload.dict())
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

@router.delete("/delete_account/{account_id}", status_code=204)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    account = db.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    db.delete(account)
    db.commit()
    return