from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.lead import Lead


class LeadRepository(BaseRepository[Lead]):
    """Repository for Lead operations"""
    
    def __init__(self, db: Session):
        super().__init__(Lead, db)
    
    def get_by_email(self, email: str) -> Optional[Lead]:
        """Get lead by email"""
        return self.get_by_field("email", email)
    
    def get_by_phone(self, phone: str) -> Optional[Lead]:
        """Get lead by phone"""
        return self.get_by_field("phone", phone)
    
    def get_recent_leads(self, limit: int = 50) -> List[Lead]:
        """Get recent leads ordered by creation date"""
        return self.db.query(Lead).order_by(
            Lead.created_at.desc()
        ).limit(limit).all()
