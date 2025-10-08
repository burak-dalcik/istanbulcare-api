from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from app.services.base_service import BaseService
from app.repositories.user_repository import UserRepository
from app.repositories.service_repository import ServiceRepository
from app.repositories.lead_repository import LeadRepository
from app.models.user import User
from app.models.service import Service
from app.models.lead import Lead
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.service import ServiceCreate, ServiceUpdate
from app.schemas.lead import LeadCreate
from app.exceptions.custom_exceptions import (
    UserNotFoundError,
    UserEmailExistsError,
    ServiceNotFoundError,
    ServiceSlugExistsError,
    ValidationError
)
from app.core.security import get_password_hash


class UserService(BaseService[User, UserRepository]):
    """Service for User business logic"""
    
    def __init__(self, db: Session):
        repository = UserRepository(db)
        super().__init__(repository)
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user with validation"""
        # Check if email already exists
        if self.repository.email_exists(user_data.email):
            raise UserEmailExistsError(user_data.email)
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Prepare data
        user_dict = user_data.model_dump()
        user_dict["password_hash"] = hashed_password
        del user_dict["password"]  # Remove plain password
        
        # Create user
        user = self.repository.create(**user_dict)
        return user
    
    def get_user_by_email(self, email: str) -> User:
        """Get user by email"""
        user = self.repository.get_by_email(email)
        if not user:
            raise UserNotFoundError(email)
        return user
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        try:
            user = self.get_user_by_email(email)
            from app.core.security import verify_password
            if verify_password(password, user.password_hash):
                return user
        except UserNotFoundError:
            pass
        return None
    
    def update_user(self, user_id: int, update_data: UserUpdate) -> User:
        """Update user with validation"""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"id {user_id}")
        
        # Check email uniqueness if email is being updated
        update_dict = update_data.model_dump(exclude_unset=True)
        if "email" in update_dict and self.repository.email_exists(update_dict["email"], exclude_id=user_id):
            raise UserEmailExistsError(update_dict["email"])
        
        # Hash password if being updated
        if "password" in update_dict:
            update_dict["password_hash"] = get_password_hash(update_dict["password"])
            del update_dict["password"]
        
        # Update user
        updated_user = self.repository.update(user_id, **update_dict)
        return updated_user


class ServiceService(BaseService[Service, ServiceRepository]):
    """Service for Service business logic"""
    
    def __init__(self, db: Session):
        repository = ServiceRepository(db)
        super().__init__(repository)
    
    def create_service(self, service_data: ServiceCreate) -> Service:
        """Create a new service with validation"""
        # Check if slug already exists
        if self.repository.slug_exists(service_data.slug):
            raise ServiceSlugExistsError(service_data.slug)
        
        # Validate and prepare data
        validated_data = self.validate_create_data(service_data.model_dump())
        prepared_data = self.before_create(validated_data)
        
        # Create service
        service = self.repository.create(**prepared_data)
        return self.after_create(service)
    
    def get_service_by_slug(self, slug: str) -> Service:
        """Get service by slug"""
        service = self.repository.get_by_slug(slug)
        if not service:
            raise ServiceNotFoundError(slug)
        return service
    
    def get_active_services(self) -> List[Service]:
        """Get all active services"""
        return self.repository.get_active_services()
    
    def update_service(self, service_id: int, update_data: ServiceUpdate) -> Service:
        """Update service with validation"""
        service = self.repository.get_by_id(service_id)
        if not service:
            raise ServiceNotFoundError(f"id {service_id}")
        
        # Check slug uniqueness if slug is being updated
        update_dict = update_data.model_dump(exclude_unset=True)
        if "slug" in update_dict and self.repository.slug_exists(update_dict["slug"], exclude_id=service_id):
            raise ServiceSlugExistsError(update_dict["slug"])
        
        # Validate and prepare data
        validated_data = self.validate_update_data(update_dict)
        prepared_data = self.before_update(service, validated_data)
        
        # Update service
        updated_service = self.repository.update(service_id, **prepared_data)
        return self.after_update(updated_service)


class LeadService(BaseService[Lead, LeadRepository]):
    """Service for Lead business logic"""
    
    def __init__(self, db: Session):
        repository = LeadRepository(db)
        super().__init__(repository)
    
    def create_lead(self, lead_data: LeadCreate) -> Lead:
        """Create a new lead with validation"""
        # Validate and prepare data
        validated_data = self.validate_create_data(lead_data.model_dump())
        prepared_data = self.before_create(validated_data)
        
        # Create lead
        lead = self.repository.create(**prepared_data)
        return self.after_create(lead)
    
    def get_recent_leads(self, limit: int = 50) -> List[Lead]:
        """Get recent leads"""
        return self.repository.get_recent_leads(limit)
    
    def validate_create_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate lead creation data"""
        # Add custom validation logic here
        if "email" in data and "@" not in data["email"]:
            raise ValidationError("Invalid email format")
        
        if "phone" in data and len(data["phone"]) < 10:
            raise ValidationError("Phone number must be at least 10 characters")
        
        return data
