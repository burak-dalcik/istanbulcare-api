from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.service import Service


class ServiceRepository(BaseRepository[Service]):
    """Repository for Service operations"""
    
    def __init__(self, db: Session):
        super().__init__(Service, db)
    
    def get_by_slug(self, slug: str) -> Optional[Service]:
        """Get service by slug"""
        return self.get_by_field("slug", slug)
    
    def get_active_services(self) -> List[Service]:
        """Get all active services"""
        return self.get_many_by_field("is_active", True)
    
    def slug_exists(self, slug: str, exclude_id: Optional[int] = None) -> bool:
        """Check if slug exists, optionally excluding a specific ID"""
        query = self.db.query(Service).filter(Service.slug == slug)
        if exclude_id:
            query = query.filter(Service.id != exclude_id)
        return query.first() is not None
