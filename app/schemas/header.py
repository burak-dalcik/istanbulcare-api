from pydantic import BaseModel
from typing import Optional, List


class ComboboxItemBase(BaseModel):
    name_tr: str
    name_en: str
    slug: str
    url: Optional[str] = None
    is_active: bool = True
    order: int = 0


class ComboboxItemCreate(ComboboxItemBase):
    header_column_id: int


class ComboboxItemUpdate(BaseModel):
    name_tr: Optional[str] = None
    name_en: Optional[str] = None
    slug: Optional[str] = None
    url: Optional[str] = None
    is_active: Optional[bool] = None
    order: Optional[int] = None


class ComboboxItemRead(ComboboxItemBase):
    id: int
    header_column_id: int

    model_config = {
        "from_attributes": True
    }


class HeaderColumnBase(BaseModel):
    name_tr: str
    name_en: str
    slug: str
    is_active: bool = True
    order: int = 0
    type: str = "link"  # "link", "dropdown", "combobox"
    url: Optional[str] = None
    has_combobox: bool = False


class HeaderColumnCreate(HeaderColumnBase):
    pass


class HeaderColumnUpdate(BaseModel):
    name_tr: Optional[str] = None
    name_en: Optional[str] = None
    slug: Optional[str] = None
    is_active: Optional[bool] = None
    order: Optional[int] = None
    type: Optional[str] = None
    url: Optional[str] = None
    has_combobox: Optional[bool] = None


class HeaderColumnRead(HeaderColumnBase):
    id: int
    combobox_items: List[ComboboxItemRead] = []

    model_config = {
        "from_attributes": True
    }


class HeaderColumnListItem(BaseModel):
    id: int
    name_tr: str
    name_en: str
    slug: str
    is_active: bool
    order: int
    type: str
    url: Optional[str] = None
    has_combobox: bool

    model_config = {
        "from_attributes": True
    }
