import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from routes.auth_routes import router as auth_router
from routes.products_routes import router as products_router
from db.database import connect_db, close_db
from core.config import settings


logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to the database
    await connect_db()
    yield
    # Shutdown: Close the database connection
    await close_db()


# Initialize the FastAPI application with custom metadata for the docs
app = FastAPI(
    title="Electronics_Store",
    description="A simple API for user authentication and managing products",
    version="1.0.1",
    openapi_tags=[
        {"name": "auth", "description": "Operations related to user authentication"},
        {"name": "products", "description": "Operations related to products listings"},
    ],
    lifespan=lifespan,
)

# Security middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(products_router, prefix="/api/v1/products", tags=["products"])


@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <h1>Products API</h1>
    <a href='/docs'>Documentation</a>
    """
