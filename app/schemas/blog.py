from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class BlogPostBase(BaseModel):
    slug: str
    author_id: int
    published_date: Optional[datetime] = None
    
    # Multilingual titles
    title_tr: Optional[str] = None
    title_en: Optional[str] = None
    title_fr: Optional[str] = None
    
    # Multilingual content
    content_tr: Optional[str] = None
    content_en: Optional[str] = None
    content_fr: Optional[str] = None
    
    # Multilingual descriptions
    description_tr: Optional[str] = None
    description_en: Optional[str] = None
    description_fr: Optional[str] = None
    
    # Images
    featured_image_url: Optional[str] = None  # Ana resim URL'i
    gallery_urls: Optional[List[str]] = None  # Galeri resimleri


class BlogPostCreate(BlogPostBase):
    pass


class BlogPostUpdate(BaseModel):
    slug: Optional[str] = None
    author_id: Optional[int] = None
    published_date: Optional[datetime] = None
    
    # Multilingual titles
    title_tr: Optional[str] = None
    title_en: Optional[str] = None
    title_fr: Optional[str] = None
    
    # Multilingual content
    content_tr: Optional[str] = None
    content_en: Optional[str] = None
    content_fr: Optional[str] = None
    
    # Multilingual descriptions
    description_tr: Optional[str] = None
    description_en: Optional[str] = None
    description_fr: Optional[str] = None
    
    # Images
    featured_image_url: Optional[str] = None  # Ana resim URL'i
    gallery_urls: Optional[List[str]] = None  # Galeri resimleri


class BlogPostRead(BlogPostBase):
    id: int

    model_config = {
        "from_attributes": True
    }


class PaginatedBlogPosts(BaseModel):
    items: List[BlogPostRead]
    total: int
    page: int
    size: int
