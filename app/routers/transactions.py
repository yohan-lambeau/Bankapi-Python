"""Transaction endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.database import get_db
from app.models.models import Account, User, Transaction, TransactionType
from app.schemas.schemas import TransactionCreate, TransactionResponse

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/{account_id}", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    account_id: int,
    transaction: TransactionCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a transaction for an account."""
    # Get user from database
    user = db.query(User).filter(User.username == current_user["username"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get account
    account = db.query(Account).filter(
        Account.id == account_id,
        Account.user_id == user.id
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    # Validate transaction type
    try:
        trans_type = TransactionType(transaction.transaction_type.lower())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid transaction type. Must be: deposit, withdrawal, or transfer"
        )
    
    # Check balance for withdrawals
    if trans_type == TransactionType.WITHDRAWAL:
        if account.balance < transaction.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient balance"
            )
        account.balance -= transaction.amount
    elif trans_type == TransactionType.DEPOSIT:
        account.balance += transaction.amount
    
    # Create transaction
    db_transaction = Transaction(
        account_id=account_id,
        transaction_type=trans_type,
        amount=transaction.amount,
        description=transaction.description
    )
    
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@router.get("/{account_id}", response_model=List[TransactionResponse])
def get_transactions(
    account_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all transactions for an account."""
    # Get user from database
    user = db.query(User).filter(User.username == current_user["username"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get account
    account = db.query(Account).filter(
        Account.id == account_id,
        Account.user_id == user.id
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    transactions = db.query(Transaction).filter(
        Transaction.account_id == account_id
    ).order_by(Transaction.created_at.desc()).all()
    
    return transactions
