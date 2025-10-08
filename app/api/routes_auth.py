from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.user_service import UserService
from app.dependencies.services import get_user_service
from app.schemas.user import UserCreate, UserRead, Token, LoginRequest
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(
    payload: UserCreate, 
    user_service: UserService = Depends(get_user_service)
):
    """Register a new user"""
    return user_service.create_user(payload)


@router.post("/login", response_model=Token)
def login(
    payload: LoginRequest, 
    user_service: UserService = Depends(get_user_service)
):
    """Login user and return access token"""
    user = user_service.authenticate_user(payload.email, payload.password)
    if not user:
        from app.exceptions.custom_exceptions import InvalidCredentialsError
        raise InvalidCredentialsError()

    token = create_access_token(subject=user.email, is_admin=user.is_admin)
    return Token(access_token=token)
