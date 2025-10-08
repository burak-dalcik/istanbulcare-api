from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.blog import BlogPost


class BlogRepository(BaseRepository[BlogPost]):
    """Repository for BlogPost operations"""
    
    def __init__(self, db: Session):
        super().__init__(BlogPost, db)
    
    def get_by_slug(self, slug: str) -> Optional[BlogPost]:
        """Get blog post by slug"""
        return self.get_by_field("slug", slug)
    
    def get_published_posts(self, skip: int = 0, limit: int = 10) -> List[BlogPost]:
        """Get published blog posts with pagination"""
        return self.db.query(BlogPost).filter(
            BlogPost.published_date.isnot(None)
        ).order_by(
            BlogPost.published_date.desc()
        ).offset(skip).limit(limit).all()
    
    def get_posts_by_author(self, author_id: int) -> List[BlogPost]:
        """Get posts by author ID"""
        return self.get_many_by_field("author_id", author_id)
    
    def slug_exists(self, slug: str, exclude_id: Optional[int] = None) -> bool:
        """Check if slug exists, optionally excluding a specific ID"""
        query = self.db.query(BlogPost).filter(BlogPost.slug == slug)
        if exclude_id:
            query = query.filter(BlogPost.id != exclude_id)
        return query.first() is not None
