from fastapi import APIRouter, Depends, Query, status, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import uuid
from pathlib import Path

from app.db.session import get_db
from app.services.blog_service import BlogService
from app.services.user_service import ServiceService, LeadService
from app.dependencies.services import get_blog_service, get_service_service, get_lead_service
from app.models.header import HeaderColumn, ComboboxItem
from app.schemas.service import ServiceListItem, ServiceRead
from app.schemas.blog import PaginatedBlogPosts, BlogPostRead, BlogPostCreate
from app.schemas.lead import LeadCreate, LeadRead
from app.schemas.header import HeaderColumnListItem, ComboboxItemRead

router = APIRouter(prefix="/api/v1", tags=["public"]) 


@router.get("/services", response_model=list[ServiceListItem])
def list_services(service_service: ServiceService = Depends(get_service_service)):
    """Get all active services"""
    return service_service.get_active_services()


@router.get("/services/{slug}", response_model=ServiceRead)
def get_service(slug: str, service_service: ServiceService = Depends(get_service_service)):
    """Get service by slug"""
    return service_service.get_service_by_slug(slug)


@router.get("/blog/posts", response_model=PaginatedBlogPosts)
def list_blog_posts(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    lang: str = Query("en", description="Language code (tr, en, fr)"),
    blog_service: BlogService = Depends(get_blog_service),
):
    """Get paginated blog posts with language support"""
    result = blog_service.get_published_posts(page=page, size=size)
    return PaginatedBlogPosts(
        items=result["items"], 
        total=result["total"], 
        page=result["page"], 
        size=result["size"]
    )


@router.get("/blog/posts/{slug}", response_model=BlogPostRead)
def get_blog_post(
    slug: str, 
    lang: str = Query("en", description="Language code (tr, en, fr)"),
    blog_service: BlogService = Depends(get_blog_service)
):
    """Get single blog post by slug with language support"""
    return blog_service.get_post_by_slug(slug)


@router.post("/blog/posts", response_model=BlogPostRead, status_code=status.HTTP_201_CREATED)
def create_blog_post(
    payload: BlogPostCreate, 
    blog_service: BlogService = Depends(get_blog_service)
):
    """Create a new blog post"""
    return blog_service.create_post(payload)


@router.post("/leads", response_model=LeadRead, status_code=status.HTTP_201_CREATED)
def create_lead(
    payload: LeadCreate, 
    lead_service: LeadService = Depends(get_lead_service)
):
    """Create a new lead"""
    return lead_service.create_lead(payload)


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
