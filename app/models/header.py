from sqlalchemy import Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class HeaderColumn(Base):
    __tablename__ = "header_columns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name_tr: Mapped[str] = mapped_column(String(255), nullable=False)  # "Saç Ekimi", "Hizmetler" etc.
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)  # "Hair Transplant", "Services" etc.
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)  # "hair-transplant", "services"
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # Sıralama için
    type: Mapped[str] = mapped_column(String(50), default="link", nullable=False)  # "link", "dropdown", "combobox"
    url: Mapped[str | None] = mapped_column(String(500), nullable=True)  # Link için URL
    has_combobox: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)  # Combobox var mı?
    
    # Relationships
    combobox_items: Mapped[list["ComboboxItem"]] = relationship("ComboboxItem", back_populates="header_column", cascade="all, delete-orphan")


class ComboboxItem(Base):
    __tablename__ = "combobox_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    header_column_id: Mapped[int] = mapped_column(Integer, ForeignKey("header_columns.id"), nullable=False, index=True)
    name_tr: Mapped[str] = mapped_column(String(255), nullable=False)  # "DHI Saç Ekimi", "FUE Saç Ekimi" etc.
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)  # "DHI Hair Transplant", "FUE Hair Transplant" etc.
    slug: Mapped[str] = mapped_column(String(255), nullable=False)  # "dhi-hair-transplant", "fue-hair-transplant"
    url: Mapped[str | None] = mapped_column(String(500), nullable=True)  # Link URL'i
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # Sıralama için
    
    # Relationships
    header_column: Mapped["HeaderColumn"] = relationship("HeaderColumn", back_populates="combobox_items")
