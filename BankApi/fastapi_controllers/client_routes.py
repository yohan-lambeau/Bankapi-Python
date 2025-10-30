# fastapi_controllers/client_routes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import List

from BankApi.repository.database import SessionLocal
from BankApi.models import Client

router = APIRouter(prefix="/api", tags=["clients"])

# ----- Schémas -----
class ClientCreate(BaseModel):
    nom: str
    email: EmailStr

class ClientRead(BaseModel):
    id: int
    nom: str
    email: EmailStr

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
@router.get("/clients", response_model=List[ClientRead])
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()

@router.get("/client/{client_id}", response_model=ClientRead)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.post("/add_client", response_model=ClientRead, status_code=201)
def create_client(payload: ClientCreate, db: Session = Depends(get_db)):
    if db.query(Client).filter(Client.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    client = Client(nom=payload.nom, email=payload.email)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

@router.delete("/delete_client/{client_id}", status_code=204)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()
    return