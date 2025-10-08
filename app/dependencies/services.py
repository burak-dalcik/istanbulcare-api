from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import get_db
from app.services.blog_service import BlogService
from app.services.user_service import UserService, ServiceService, LeadService


def get_blog_service(db: Session = Depends(get_db)) -> BlogService:
    """Get BlogService instance"""
    return BlogService(db)


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Get UserService instance"""
    return UserService(db)


def get_service_service(db: Session = Depends(get_db)) -> ServiceService:
    """Get ServiceService instance"""
    return ServiceService(db)


def get_lead_service(db: Session = Depends(get_db)) -> LeadService:
    """Get LeadService instance"""
    return LeadService(db)
