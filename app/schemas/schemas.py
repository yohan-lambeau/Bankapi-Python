"""Pydantic schemas for API validation."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# User schemas
class UserBase(BaseModel):
    """Base user schema."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str = Field(..., min_length=6)


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Token schemas
class Token(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token payload data."""
    username: Optional[str] = None


# Account schemas
class AccountBase(BaseModel):
    """Base account schema."""
    account_type: str = Field(..., description="Type of account (checking, savings, etc.)")
    currency: str = Field(default="USD", max_length=3)


class AccountCreate(AccountBase):
    """Schema for creating an account."""
    pass


class AccountResponse(AccountBase):
    """Schema for account response."""
    id: int
    account_number: str
    balance: float
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Transaction schemas
class TransactionBase(BaseModel):
    """Base transaction schema."""
    amount: float = Field(..., gt=0)
    description: Optional[str] = None


class TransactionCreate(TransactionBase):
    """Schema for creating a transaction."""
    transaction_type: str = Field(..., description="Type: deposit, withdrawal, transfer")


class TransactionResponse(TransactionBase):
    """Schema for transaction response."""
    id: int
    account_id: int
    transaction_type: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Login schema
class LoginRequest(BaseModel):
    """Login request schema."""
    username: str
    password: str
