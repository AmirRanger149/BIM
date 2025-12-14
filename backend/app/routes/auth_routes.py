from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app import models, schemas, auth
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=dict, status_code=201)
def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """ثبت‌نام کاربر جدید"""
    # بررسی وجود کاربر
    existing_user = auth.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="این ایمیل قبلا ثبت شده است"
        )
    
    # ایجاد کاربر
    db_user = auth.create_user(db, user)
    
    return {
        "success": True,
        "message": "ثبت‌نام با موفقیت انجام شد",
        "data": {
            "id": db_user.id,
            "email": db_user.email,
            "full_name": db_user.full_name
        }
    }


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """ورود کاربر"""
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ایمیل یا رمز عبور اشتباه است",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # ایجاد access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=schemas.User)
def read_users_me(
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """دریافت اطلاعات کاربر فعلی"""
    return current_user


@router.post("/change-password", response_model=dict)
def change_password(
    old_password: str,
    new_password: str,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """تغییر رمز عبور"""
    # بررسی رمز عبور قدیمی
    if not auth.verify_password(old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="رمز عبور فعلی اشتباه است"
        )
    
    # بروزرسانی رمز عبور
    current_user.hashed_password = auth.get_password_hash(new_password)
    db.commit()
    
    return {
        "success": True,
        "message": "رمز عبور با موفقیت تغییر کرد"
    }
