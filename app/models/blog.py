from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.session import Base


class BlogPost(Base):
    __tablename__ = "blog_posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)

    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    author: Mapped["User"] = relationship("User", back_populates="posts")

    published_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    title_tr: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title_fr: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    content_tr: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_fr: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    description_tr: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_fr: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Image fields for React admin panel
    featured_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)  # Ana resim URL'i
    gallery_urls: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)  # Galeri resimleri (array of URLs)
