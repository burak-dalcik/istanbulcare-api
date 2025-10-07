from sqlalchemy import Boolean, Integer, String, Text, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    title_tr: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description_tr: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_tr: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Service details
    price: Mapped[float | None] = mapped_column(Float, nullable=True)
    duration: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    # Image fields for React admin panel
    featured_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)  # Ana resim URL'i
    gallery_urls: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)  # Galeri resimleri (array of URLs)
