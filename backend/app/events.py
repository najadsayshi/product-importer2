from fastapi import APIRouter, Depends
from .database import get_db
from .crud import get_job

router = APIRouter()

@router.get("/jobs/{job_id}")
def job_status(job_id: str, db=Depends(get_db)):
    job = get_job(db, job_id)
    if not job:
        return {"error": "not found"}
    return {
        "id": str(job.id),
        "filename": job.filename,
        "total_rows": job.total_rows,
        "processed_rows": job.processed_rows,
        "status": job.status,
        "errors": job.errors
    }
