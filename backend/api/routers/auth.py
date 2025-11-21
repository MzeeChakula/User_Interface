from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from api.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from sqlalchemy.orm import Session
from api.models.database import get_db
from api.models.user import UserDB, UserCreate, Token, User, PasswordResetRequest

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)

@router.post("/register", response_model=User)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user

    Requirements:
    - Email must be valid and not already registered
    - Password must be 8-72 characters long
    - Password must contain uppercase, lowercase, and numbers
    """
    try:
        # Check if user exists
        db_user = db.query(UserDB).filter(UserDB.email == user.email).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This email is already registered. Please log in instead or use a different email."
            )

        # Validate email format
        if "@" not in user.email or "." not in user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please enter a valid email address"
            )

        # Hash password (this also validates it)
        hashed_password = get_password_hash(user.password)

        new_user = UserDB(
            email=user.email,
            hashed_password=hashed_password,
            full_name=user.full_name,
            is_active=user.is_active
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed. Please try again later."
        )

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    """
    Login to get an access token

    Use your email as username and your password to log in.
    """
    # Find user by email
    user = db.query(UserDB).filter(UserDB.email == form_data.username).first()

    # Check if user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No account found with this email. Please sign up first.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if password is correct
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password. Please try again or reset your password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account has been deactivated. Please contact support.",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/reset-password")
async def reset_password(request: PasswordResetRequest, db: Session = Depends(get_db)):
    """
    Request a password reset
    """
    # Check if user exists (optional, depending on security policy)
    user = db.query(UserDB).filter(UserDB.email == request.email).first()
    
    # In a real app, we would generate a token and send an email.
    # For now, we just simulate success to support the UI flow.
    if user:
        # TODO: Send email with reset token
        pass
        
    return {"message": "If an account exists with this email, you will receive password reset instructions."}
