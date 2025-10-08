from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from app.services.base_service import BaseService
from app.repositories.blog_repository import BlogRepository
from app.models.blog import BlogPost
from app.schemas.blog import BlogPostCreate, BlogPostUpdate
from app.exceptions.custom_exceptions import (
    BlogPostNotFoundError, 
    BlogPostSlugExistsError,
    ValidationError
)


class BlogService(BaseService[BlogPost, BlogRepository]):
    """Service for BlogPost business logic"""
    
    def __init__(self, db: Session):
        repository = BlogRepository(db)
        super().__init__(repository)
    
    def create_post(self, post_data: BlogPostCreate) -> BlogPost:
        """Create a new blog post with validation"""
        # Check if slug already exists
        if self.repository.slug_exists(post_data.slug):
            raise BlogPostSlugExistsError(post_data.slug)
        
        # Validate and prepare data
        validated_data = self.validate_create_data(post_data.model_dump())
        prepared_data = self.before_create(validated_data)
        
        # Create the post
        post = self.repository.create(**prepared_data)
        
        # Post-create logic
        return self.after_create(post)
    
    def get_post_by_slug(self, slug: str) -> BlogPost:
        """Get blog post by slug"""
        post = self.repository.get_by_slug(slug)
        if not post:
            raise BlogPostNotFoundError(slug)
        return post
    
    def get_published_posts(self, page: int = 1, size: int = 10) -> Dict[str, Any]:
        """Get published posts with pagination"""
        skip = (page - 1) * size
        posts = self.repository.get_published_posts(skip=skip, limit=size)
        total = self.repository.count()
        
        return {
            "items": posts,
            "total": total,
            "page": page,
            "size": size
        }
    
    def update_post(self, post_id: int, update_data: BlogPostUpdate) -> BlogPost:
        """Update blog post with validation"""
        post = self.repository.get_by_id(post_id)
        if not post:
            raise BlogPostNotFoundError(f"id {post_id}")
        
        # Check slug uniqueness if slug is being updated
        update_dict = update_data.model_dump(exclude_unset=True)
        if "slug" in update_dict and self.repository.slug_exists(update_dict["slug"], exclude_id=post_id):
            raise BlogPostSlugExistsError(update_dict["slug"])
        
        # Validate and prepare data
        validated_data = self.validate_update_data(update_dict)
        prepared_data = self.before_update(post, validated_data)
        
        # Update the post
        updated_post = self.repository.update(post_id, **prepared_data)
        
        # Post-update logic
        return self.after_update(updated_post)
    
    def delete_post(self, post_id: int) -> bool:
        """Delete blog post"""
        post = self.repository.get_by_id(post_id)
        if not post:
            raise BlogPostNotFoundError(f"id {post_id}")
        
        return self.repository.delete(post_id)
    
    def get_posts_by_author(self, author_id: int) -> List[BlogPost]:
        """Get posts by author"""
        return self.repository.get_posts_by_author(author_id)
    
    def validate_create_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate blog post creation data"""
        # Add custom validation logic here
        if "title" in data and len(data["title"]) < 3:
            raise ValidationError("Title must be at least 3 characters long")
        
        if "slug" in data and not data["slug"].replace("-", "").replace("_", "").isalnum():
            raise ValidationError("Slug must contain only alphanumeric characters, hyphens, and underscores")
        
        return data
    
    def validate_update_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate blog post update data"""
        # Add custom validation logic here
        if "title" in data and len(data["title"]) < 3:
            raise ValidationError("Title must be at least 3 characters long")
        
        if "slug" in data and not data["slug"].replace("-", "").replace("_", "").isalnum():
            raise ValidationError("Slug must contain only alphanumeric characters, hyphens, and underscores")
        
        return data
