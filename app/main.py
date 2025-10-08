from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import Base, engine
from app.api.routes_public import router as public_router
from app.api.routes_admin import router as admin_router
from app.api.routes_auth import router as auth_router
from app.exceptions.handlers import (
    custom_exception_handler,
    http_exception_handler,
    general_exception_handler
)
from app.exceptions.custom_exceptions import BaseCustomException
import app.models  # noqa: F401 ensure models are imported for table creation

app = FastAPI(
    title="Istanbul Care API - Public Endpoints",
    description="Simple public API for blog posts and content management",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
app.add_exception_handler(BaseCustomException, custom_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


# Include routers
app.include_router(public_router)
app.include_router(admin_router)
app.include_router(auth_router)
