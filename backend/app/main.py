from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import shutil
import uuid
import os
from pathlib import Path

from . import database, crud, models, schemas, tasks, events

app = FastAPI(title="Acme Product Importer")

# Mount frontend
app.mount("/static", StaticFiles(directory="/app/frontend"), name="static")

# SSE router for progress
app.include_router(events.router)

@app.on_event("startup")
def startup():
    crud.create_tables(database.engine)
    os.makedirs("/tmp/uploads", exist_ok=True)

@app.get("/")
def index():
    return HTMLResponse(open("/app/frontend/index.html", "r", encoding="utf-8").read())


# ============================
# FIXED UPLOAD ENDPOINT
# ============================
@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())
    dest = Path(f"/tmp/uploads/{job_id}.csv")

    # Save uploaded file correctly
    with open(dest, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # DB job
    db = next(database.get_db())
    crud.create_import_job(db, job_id=job_id, filename=str(dest))

    # Queue task
    tasks.process_csv_import.delay(job_id, str(dest))


    return {"job_id": job_id}

@app.get("/jobs/{job_id}")
def job_status(job_id: str, db: Session = Depends(database.get_db)):
    job = crud.get_import_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "job_id": job.job_id,
        "filename": job.filename,
        "status": job.status,
        "progress": job.progress,
        "processed": job.processed,
        "total": job.total,
    }


@app.get("/products")
def list_products(
    skip: int = 0,
    limit: int = 50,
    filter: str = "",
    db: Session = Depends(database.get_db)
):
    filters = {}
    if filter:
        filters['sku'] = filter
        filters['name'] = filter

    items, total = crud.get_products(db, skip=skip, limit=limit, filters=filters)
    return {"items": items, "total": total}


@app.post("/products")
def create_product(p: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    return crud.create_product(db, p)


@app.put("/products/{product_id}")
def update_product(product_id: int, p: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    prod = crud.update_product(db, product_id, p)
    if not prod:
        raise HTTPException(status_code=404, detail="Not found")
    return prod


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(database.get_db)):
    ok = crud.delete_product(db, product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Not found")
    return {"deleted": ok}


@app.post("/products/delete_all")
def delete_all_products(db: Session = Depends(database.get_db)):
    n = crud.delete_all_products(db)
    return {"deleted": n}
