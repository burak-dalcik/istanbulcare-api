from pydantic import BaseModel
from typing import Optional, List


class ServiceBase(BaseModel):
    slug: str
    is_active: bool = True
    title_tr: Optional[str] = None
    title_en: Optional[str] = None
    description_tr: Optional[str] = None
    description_en: Optional[str] = None
    content_tr: Optional[str] = None
    content_en: Optional[str] = None
    price: Optional[float] = None
    duration: Optional[str] = None
    featured_image_url: Optional[str] = None  # Ana resim URL'i
    gallery_urls: Optional[List[str]] = None  # Galeri resimleri


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    slug: Optional[str] = None
    is_active: Optional[bool] = None
    title_tr: Optional[str] = None
    title_en: Optional[str] = None
    description_tr: Optional[str] = None
    description_en: Optional[str] = None
    content_tr: Optional[str] = None
    content_en: Optional[str] = None
    price: Optional[float] = None
    duration: Optional[str] = None
    featured_image_url: Optional[str] = None  # Ana resim URL'i
    gallery_urls: Optional[List[str]] = None  # Galeri resimleri


class ServiceListItem(BaseModel):
    slug: str
    title_tr: Optional[str] = None
    title_en: Optional[str] = None
    description_tr: Optional[str] = None
    description_en: Optional[str] = None
    price: Optional[float] = None
    duration: Optional[str] = None
    featured_image_url: Optional[str] = None  # Ana resim URL'i

    model_config = {
        "from_attributes": True
    }


class ServiceRead(ServiceBase):
    id: int

    model_config = {
        "from_attributes": True
    }
