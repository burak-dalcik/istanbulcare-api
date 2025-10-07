from fastapi import APIRouter, Depends, HTTPException, Query, status, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import uuid
from pathlib import Path

from app.db.session import get_db
from app.models.service import Service
from app.models.blog import BlogPost
from app.models.lead import Lead
from app.models.header import HeaderColumn, ComboboxItem
from app.schemas.service import ServiceListItem, ServiceRead
from app.schemas.blog import PaginatedBlogPosts, BlogPostRead, BlogPostCreate
from app.schemas.lead import LeadCreate, LeadRead
from app.schemas.header import HeaderColumnListItem, ComboboxItemRead

router = APIRouter(prefix="/api/v1", tags=["public"]) 


@router.get("/services", response_model=list[ServiceListItem])
def list_services(db: Session = Depends(get_db)):
    services = db.query(Service).filter(Service.is_active == True).order_by(Service.id.desc()).all()
    return services


@router.get("/services/{slug}", response_model=ServiceRead)
def get_service(slug: str, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.slug == slug, Service.is_active == True).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


@router.get("/blog/posts", response_model=PaginatedBlogPosts)
def list_blog_posts(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    lang: str = Query("en", description="Language code (tr, en, fr)"),
    db: Session = Depends(get_db),
):
    """Get paginated blog posts with language support"""
    query = db.query(BlogPost).order_by(BlogPost.published_date.desc().nullslast(), BlogPost.id.desc())
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return PaginatedBlogPosts(items=items, total=total, page=page, size=size)


@router.get("/blog/posts/{slug}", response_model=BlogPostRead)
def get_blog_post(
    slug: str, 
    lang: str = Query("en", description="Language code (tr, en, fr)"),
    db: Session = Depends(get_db)
):
    """Get single blog post by slug with language support"""
    post = db.query(BlogPost).filter(BlogPost.slug == slug).first()
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return post


@router.post("/blog/posts", response_model=BlogPostRead, status_code=status.HTTP_201_CREATED)
def create_blog_post(payload: BlogPostCreate, db: Session = Depends(get_db)):
    """Create a new blog post"""
    # Check if slug already exists
    if db.query(BlogPost).filter(BlogPost.slug == payload.slug).first():
        raise HTTPException(status_code=400, detail="Post slug already exists")
    
    # Create new blog post
    blog_post = BlogPost(**payload.model_dump())
    db.add(blog_post)
    db.commit()
    db.refresh(blog_post)
    return blog_post


@router.post("/leads", response_model=LeadRead, status_code=status.HTTP_201_CREATED)
def create_lead(payload: LeadCreate, db: Session = Depends(get_db)):
    lead = Lead(**payload.model_dump())
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


# Header Columns (Public - No Authentication Required)
@router.get("/header/columns", response_model=list[HeaderColumnListItem])
def get_header_columns(lang: str = Query("en", description="Language code (tr, en)"), db: Session = Depends(get_db)):
    """Get all active header columns for frontend navigation with language support"""
    columns = db.query(HeaderColumn).filter(HeaderColumn.is_active == True).order_by(HeaderColumn.order, HeaderColumn.id).all()
    return columns


@router.get("/header/columns/{slug}/combobox-items", response_model=list[ComboboxItemRead])
def get_combobox_items(slug: str, lang: str = Query("en", description="Language code (tr, en)"), db: Session = Depends(get_db)):
    """Get combobox items for a specific header column with language support"""
    header_column = db.query(HeaderColumn).filter(HeaderColumn.slug == slug, HeaderColumn.is_active == True).first()
    if not header_column:
        raise HTTPException(status_code=404, detail="Header column not found")
    
    items = db.query(ComboboxItem).filter(
        ComboboxItem.header_column_id == header_column.id,
        ComboboxItem.is_active == True
    ).order_by(ComboboxItem.order, ComboboxItem.id).all()
    
    return items


# Image Upload Endpoints
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def validate_image_file(file: UploadFile):
    """Validate uploaded image file"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    return file_ext


@router.post("/images/upload")
async def upload_image(file: UploadFile = File(...)):
    """Upload a single image file"""
    # Validate file
    file_ext = validate_image_file(file)
    
    # Check file size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 5MB")
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Return file info
    return {
        "filename": unique_filename,
        "original_filename": file.filename,
        "url": f"/api/v1/images/{unique_filename}",
        "size": len(content)
    }


@router.post("/images/upload-multiple")
async def upload_multiple_images(files: list[UploadFile] = File(...)):
    """Upload multiple image files"""
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 files allowed")
    
    uploaded_files = []
    
    for file in files:
        # Validate file
        file_ext = validate_image_file(file)
        
        # Check file size
        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=f"File {file.filename} too large. Maximum size is 5MB")
        
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = UPLOAD_DIR / unique_filename
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(content)
        
        uploaded_files.append({
            "filename": unique_filename,
            "original_filename": file.filename,
            "url": f"/api/v1/images/{unique_filename}",
            "size": len(content)
        })
    
    return {
        "uploaded_files": uploaded_files,
        "total_files": len(uploaded_files)
    }


@router.get("/images/{filename}")
async def get_image(filename: str):
    """Serve uploaded image files"""
    file_path = UPLOAD_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(file_path)


@router.delete("/images/{filename}")
async def delete_image(filename: str):
    """Delete an uploaded image file"""
    file_path = UPLOAD_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    
    try:
        os.remove(file_path)
        return {"message": f"Image {filename} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")


@router.get("/images")
async def list_images():
    """List all uploaded images"""
    if not UPLOAD_DIR.exists():
        return {"images": []}
    
    images = []
    for file_path in UPLOAD_DIR.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in ALLOWED_EXTENSIONS:
            stat = file_path.stat()
            images.append({
                "filename": file_path.name,
                "url": f"/api/v1/images/{file_path.name}",
                "size": stat.st_size,
                "created_at": stat.st_ctime
            })
    
    # Sort by creation time (newest first)
    images.sort(key=lambda x: x["created_at"], reverse=True)
    
    return {"images": images}
