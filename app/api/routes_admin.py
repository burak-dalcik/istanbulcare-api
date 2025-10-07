from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Authentication disabled for React development
# from app.core.security import get_current_user, require_admin
from app.db.session import get_db
from app.models.user import User
from app.models.service import Service
from app.models.blog import BlogPost
from app.models.lead import Lead
from app.models.header import HeaderColumn, ComboboxItem
from app.schemas.service import ServiceCreate, ServiceUpdate, ServiceRead
from app.schemas.blog import BlogPostCreate, BlogPostUpdate, BlogPostRead
from app.schemas.lead import LeadRead
from app.schemas.header import HeaderColumnCreate, HeaderColumnUpdate, HeaderColumnRead, ComboboxItemCreate, ComboboxItemUpdate, ComboboxItemRead

router = APIRouter(
    prefix="/admin", 
    tags=["admin"],
    responses={401: {"description": "Unauthorized"}}
)


# Services
@router.post("/services", response_model=ServiceRead, status_code=status.HTTP_201_CREATED)
def create_service(payload: ServiceCreate, db: Session = Depends(get_db)):
    if db.query(Service).filter(Service.slug == payload.slug).first():
        raise HTTPException(status_code=400, detail="Service slug already exists")
    obj = Service(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/services/{id}", response_model=ServiceRead)
def update_service(id: int, payload: ServiceUpdate, db: Session = Depends(get_db)):
    obj = db.query(Service).filter(Service.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Service not found")
    data = payload.model_dump(exclude_unset=True)
    if "slug" in data:
        exists = db.query(Service).filter(Service.slug == data["slug"], Service.id != id).first()
        if exists:
            raise HTTPException(status_code=400, detail="Service slug already exists")
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/services/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(id: int, db: Session = Depends(get_db)):
    obj = db.query(Service).filter(Service.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Service not found")
    db.delete(obj)
    db.commit()
    return None


# Blog Posts
@router.post("/blog/posts", response_model=BlogPostRead, status_code=status.HTTP_201_CREATED)
def create_post(payload: BlogPostCreate, db: Session = Depends(get_db)):
    if db.query(BlogPost).filter(BlogPost.slug == payload.slug).first():
        raise HTTPException(status_code=400, detail="Post slug already exists")
    obj = BlogPost(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/blog/posts", response_model=list[BlogPostRead])
def list_posts(db: Session = Depends(get_db)):
    items = db.query(BlogPost).order_by(BlogPost.published_date.desc().nullslast(), BlogPost.id.desc()).all()
    return items


@router.get("/blog/posts/{id}", response_model=BlogPostRead)
def get_post(id: int, db: Session = Depends(get_db)):
    obj = db.query(BlogPost).filter(BlogPost.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Post not found")
    return obj


@router.put("/blog/posts/{id}", response_model=BlogPostRead)
def update_post(id: int, payload: BlogPostUpdate, db: Session = Depends(get_db)):
    obj = db.query(BlogPost).filter(BlogPost.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Post not found")
    data = payload.model_dump(exclude_unset=True)
    if "slug" in data:
        exists = db.query(BlogPost).filter(BlogPost.slug == data["slug"], BlogPost.id != id).first()
        if exists:
            raise HTTPException(status_code=400, detail="Post slug already exists")
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/blog/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    obj = db.query(BlogPost).filter(BlogPost.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(obj)
    db.commit()
    return None


# Leads
@router.get("/leads", response_model=list[LeadRead])
def list_leads(db: Session = Depends(get_db)):
    items = db.query(Lead).order_by(Lead.created_at.desc()).all()
    return items


# Header Columns
@router.post("/header/columns", response_model=HeaderColumnRead, status_code=status.HTTP_201_CREATED)
def create_header_column(payload: HeaderColumnCreate, db: Session = Depends(get_db)):
    if db.query(HeaderColumn).filter(HeaderColumn.slug == payload.slug).first():
        raise HTTPException(status_code=400, detail="Header column slug already exists")
    obj = HeaderColumn(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/header/columns", response_model=list[HeaderColumnRead])
def list_header_columns(db: Session = Depends(get_db)):
    items = db.query(HeaderColumn).order_by(HeaderColumn.order, HeaderColumn.id).all()
    return items


@router.put("/header/columns/{id}", response_model=HeaderColumnRead)
def update_header_column(id: int, payload: HeaderColumnUpdate, db: Session = Depends(get_db)):
    obj = db.query(HeaderColumn).filter(HeaderColumn.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Header column not found")
    data = payload.model_dump(exclude_unset=True)
    if "slug" in data:
        exists = db.query(HeaderColumn).filter(HeaderColumn.slug == data["slug"], HeaderColumn.id != id).first()
        if exists:
            raise HTTPException(status_code=400, detail="Header column slug already exists")
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/header/columns/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_header_column(id: int, db: Session = Depends(get_db)):
    obj = db.query(HeaderColumn).filter(HeaderColumn.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Header column not found")
    db.delete(obj)
    db.commit()
    return None


# Combobox Items
@router.post("/header/combobox-items", response_model=ComboboxItemRead, status_code=status.HTTP_201_CREATED)
def create_combobox_item(payload: ComboboxItemCreate, db: Session = Depends(get_db)):
    # Check if header column exists
    header_column = db.query(HeaderColumn).filter(HeaderColumn.id == payload.header_column_id).first()
    if not header_column:
        raise HTTPException(status_code=404, detail="Header column not found")
    
    # Check if slug already exists for this header column
    if db.query(ComboboxItem).filter(ComboboxItem.slug == payload.slug, ComboboxItem.header_column_id == payload.header_column_id).first():
        raise HTTPException(status_code=400, detail="Combobox item slug already exists for this header column")
    
    obj = ComboboxItem(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/header/combobox-items", response_model=list[ComboboxItemRead])
def list_combobox_items(header_column_id: int = None, db: Session = Depends(get_db)):
    query = db.query(ComboboxItem)
    if header_column_id:
        query = query.filter(ComboboxItem.header_column_id == header_column_id)
    items = query.order_by(ComboboxItem.order, ComboboxItem.id).all()
    return items


@router.put("/header/combobox-items/{id}", response_model=ComboboxItemRead)
def update_combobox_item(id: int, payload: ComboboxItemUpdate, db: Session = Depends(get_db)):
    obj = db.query(ComboboxItem).filter(ComboboxItem.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Combobox item not found")
    data = payload.model_dump(exclude_unset=True)
    if "slug" in data:
        exists = db.query(ComboboxItem).filter(ComboboxItem.slug == data["slug"], ComboboxItem.header_column_id == obj.header_column_id, ComboboxItem.id != id).first()
        if exists:
            raise HTTPException(status_code=400, detail="Combobox item slug already exists for this header column")
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/header/combobox-items/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_combobox_item(id: int, db: Session = Depends(get_db)):
    obj = db.query(ComboboxItem).filter(ComboboxItem.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Combobox item not found")
    db.delete(obj)
    db.commit()
    return None
