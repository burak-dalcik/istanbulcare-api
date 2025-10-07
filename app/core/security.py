from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User

# Use pbkdf2_sha256 to avoid platform-specific bcrypt issues
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = HTTPBearer(auto_error=False)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(subject: str, is_admin: bool, expires_minutes: Optional[int] = None) -> str:
    expire_delta = timedelta(minutes=expires_minutes or settings.access_token_expire_minutes)
    expire = datetime.now(timezone.utc) + expire_delta
    to_encode = {"sub": subject, "is_admin": is_admin, "exp": expire}
    return jwt.encode(to_encode, settings.secret_key, algorithm="HS256")


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Accept token from multiple places:
    # 1) Authorization: Bearer <token> (preferred)
    # 2) Authorization: <token> (raw token)
    # 3) X-Token: <token>
    # 4) token query parameter
    raw_auth_header = request.headers.get("Authorization")
    x_token = request.headers.get("X-Token")
    query_token = request.query_params.get("token")

    token_value: Optional[str] = None

    if credentials and credentials.credentials:
        token_value = credentials.credentials
    elif raw_auth_header:
        parts = raw_auth_header.split()
        if len(parts) == 1:
            # Authorization: <token>
            token_value = parts[0]
        elif len(parts) == 2 and parts[0].lower() == "bearer":
            token_value = parts[1]
    elif x_token:
        token_value = x_token
    elif query_token:
        token_value = query_token

    if not token_value:
        raise credentials_exception

    try:
        payload = jwt.decode(token_value, settings.secret_key, algorithms=["HS256"]) 
        sub: str = payload.get("sub")
        if sub is None:
            raise credentials_exception
        is_admin = bool(payload.get("is_admin", False))
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == sub).first()
    if user is None:
        raise credentials_exception

    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return user
