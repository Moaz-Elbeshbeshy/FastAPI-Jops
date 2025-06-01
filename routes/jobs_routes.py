from fastapi import APIRouter, Depends, status
from schemas.job_schema import JobCreate, JobResponse
from controller.jobs_controller import (
    create_job,
    get_jobs,
    get_job,
    update_job,
    delete_job,
)
from db.database import get_db
from middleware.auth_middleware import get_current_user
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()


@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job_route(
    job: JobCreate,
    user_email: str = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    return await create_job(job, user_email, db)


@router.get("/", response_model=list[JobResponse])
async def get_jobs_route(
    user_email: str = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    return await get_jobs(user_email, db)


@router.get("/{job_id}", response_model=JobResponse)
async def get_job_route(
    job_id: str,
    user_email: str = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    return await get_job(job_id, user_email, db)


@router.put("/{job_id}", response_model=JobResponse)
async def update_job_route(
    job_id: str,
    job: JobCreate,
    user_email: str = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    return await update_job(job_id, job, user_email, db)


@router.delete("/{job_id}")
async def delete_job_route(
    job_id: str,
    user_email: str = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    return await delete_job(job_id, user_email, db)
