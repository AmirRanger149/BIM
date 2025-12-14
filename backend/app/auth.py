from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app import models, schemas

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """بررسی صحت پسورد"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """هش کردن پسورد"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """ایجاد access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_user_by_email(db: Session, email: str):
    """دریافت کاربر با ایمیل"""
    return db.query(models.User).filter(models.User.email == email).first()


def authenticate_user(db: Session, email: str, password: str):
    """احراز هویت کاربر"""
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    """دریافت کاربر فعلی از token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="اطلاعات احراز هویت نامعتبر است",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    """بررسی فعال بودن کاربر"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="کاربر غیرفعال است")
    return current_user


async def get_current_admin_user(
    current_user: models.User = Depends(get_current_active_user)
) -> models.User:
    """بررسی ادمین بودن کاربر"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="شما دسترسی ادمین ندارید"
        )
    return current_user


def create_user(db: Session, user: schemas.UserCreate, is_admin: bool = False) -> models.User:
    """ایجاد کاربر جدید"""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        is_admin=is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
