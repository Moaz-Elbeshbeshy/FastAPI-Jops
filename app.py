import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from routes.auth_routes import router as auth_router
from routes.jobs_routes import router as jobs_router
from core.config import settings
from db.database import connect_db, close_db

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to the database
    await connect_db()
    yield
    # Shutdown: Close the database connection
    await close_db()


app = FastAPI(
    title="Jobs API",
    description="A simple API for user authentication and managing job listings",
    version="1.0.0",
    openapi_tags=[
        {"name": "auth", "description": "Operations related to user authentication"},
        {"name": "jobs", "description": "Operations related to job listings"},
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
app.include_router(jobs_router, prefix="/api/v1/jobs", tags=["jobs"])


@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <h1>Jobs API</h1>
    <a href="/docs">Documentation</a>
    """
