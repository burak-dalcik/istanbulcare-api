from typing import Generic, TypeVar, Type, Optional, List, Any, Dict
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository

ModelType = TypeVar("ModelType")
RepositoryType = TypeVar("RepositoryType", bound=BaseRepository)


class BaseService(Generic[ModelType, RepositoryType]):
    """Base service class providing common business logic operations"""
    
    def __init__(self, repository: RepositoryType):
        self.repository = repository
    
    def create(self, **kwargs) -> ModelType:
        """Create a new record with business logic validation"""
        return self.repository.create(**kwargs)
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Get record by ID"""
        return self.repository.get_by_id(id)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all records with pagination"""
        return self.repository.get_all(skip=skip, limit=limit)
    
    def update(self, id: int, **kwargs) -> Optional[ModelType]:
        """Update record by ID with business logic validation"""
        return self.repository.update(id, **kwargs)
    
    def delete(self, id: int) -> bool:
        """Delete record by ID with business logic validation"""
        return self.repository.delete(id)
    
    def exists(self, **kwargs) -> bool:
        """Check if record exists with given criteria"""
        return self.repository.exists(**kwargs)
    
    def count(self, **kwargs) -> int:
        """Count records with given criteria"""
        return self.repository.count(**kwargs)
    
    def validate_create_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Override in subclasses to add validation logic"""
        return data
    
    def validate_update_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Override in subclasses to add validation logic"""
        return data
    
    def before_create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Override in subclasses to add pre-create logic"""
        return data
    
    def after_create(self, obj: ModelType) -> ModelType:
        """Override in subclasses to add post-create logic"""
        return obj
    
    def before_update(self, obj: ModelType, data: Dict[str, Any]) -> Dict[str, Any]:
        """Override in subclasses to add pre-update logic"""
        return data
    
    def after_update(self, obj: ModelType) -> ModelType:
        """Override in subclasses to add post-update logic"""
        return obj
