from fastapi import HTTPException, status
from schemas.job_schema import JobCreate, JobResponse
from models.job_model import Job
from db.database import get_db
from bson import ObjectId
from datetime import datetime, UTC


async def create_job(job: JobCreate, user_email: str, db):
    user = await db.users.find_one({"email": user_email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    job_dict = job.dict()
    job_dict["user_id"] = str(user["_id"])
    job_dict["created_at"] = datetime.now(UTC)
    job_dict["updated_at"] = None

    result = await db.jobs.insert_one(job_dict)
    job_dict["id"] = str(result.inserted_id)

    return JobResponse(**job_dict)


async def get_jobs(user_email: str, db):
    user = await db.users.find_one({"email": user_email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    jobs = []
    async for job in db.jobs.find({"user_id": str(user["_id"])}):
        job["id"] = str(job["_id"])
        del job["_id"]
        jobs.append(JobResponse(**job))
    return jobs


async def get_job(job_id: str, user_email: str, db):
    try:
        job = await db.jobs.find_one({"_id": ObjectId(job_id)})
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
            )

        user = await db.users.find_one({"email": user_email})
        if job["user_id"] != str(user["_id"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this job",
            )

        job["id"] = str(job["_id"])
        del job["_id"]
        return JobResponse(**job)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid job ID"
        )


async def update_job(job_id: str, job_update: JobCreate, user_email: str, db):
    try:
        job = await db.jobs.find_one({"_id": ObjectId(job_id)})
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
            )

        user = await db.users.find_one({"email": user_email})
        if job["user_id"] != str(user["_id"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this job",
            )

        update_data = job_update.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.now(UTC)

        await db.jobs.update_one({"_id": ObjectId(job_id)}, {"$set": update_data})

        updated_job = await db.jobs.find_one({"_id": ObjectId(job_id)})
        updated_job["id"] = str(updated_job["_id"])
        del updated_job["_id"]

        return JobResponse(**updated_job)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid job ID"
        )


async def delete_job(job_id: str, user_email: str, db):
    try:
        job = await db.jobs.find_one({"_id": ObjectId(job_id)})
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
            )

        user = await db.users.find_one({"email": user_email})
        if job["user_id"] != str(user["_id"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this job",
            )

        await db.jobs.delete_one({"_id": ObjectId(job_id)})
        return {"message": "Job deleted successfully"}
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid job ID"
        )
