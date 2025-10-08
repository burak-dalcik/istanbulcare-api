from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.user import User


class UserRepository(BaseRepository[User]):
    """Repository for User operations"""
    
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.get_by_field("email", email)
    
    def email_exists(self, email: str, exclude_id: Optional[int] = None) -> bool:
        """Check if email exists, optionally excluding a specific ID"""
        query = self.db.query(User).filter(User.email == email)
        if exclude_id:
            query = query.filter(User.id != exclude_id)
        return query.first() is not None
    
    def get_admins(self) -> List[User]:
        """Get all admin users"""
        return self.get_many_by_field("is_admin", True)
