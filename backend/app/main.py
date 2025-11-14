from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.orm import Session
import shutil, uuid, os
from pathlib import Path
from . import database, crud, models, schemas, tasks, events
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Acme Product Importer")

# Mount frontend
app.mount("/static", StaticFiles(directory="/app/frontend"), name="static")

# include events router
app.include_router(events.router)

@app.on_event("startup")
def startup():
    # create DB tables
    crud.create_tables(database.engine)
    os.makedirs("/tmp/uploads", exist_ok=True)

@app.get("/")
def index():
    return HTMLResponse(open("/app/frontend/index.html", "r", encoding="utf-8").read())

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    # accept and save to /tmp/uploads
    job_id = str(uuid.uuid4())
    dest = Path(f"/tmp/uploads/{job_id}_{file.filename}")
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f.file if hasattr(file, "file") else file)
    # create import job
    db = next(database.get_db())
    job = crud.create_import_job(db, job_id=job_id, filename=str(dest))
    # enqueue Celery task
    tasks.process_csv_import.delay(job_id, str(dest))
    return {"job_id": job_id}


from fastapi import Body

@app.get("/products")
def list_products(skip: int = 0, limit: int = 50, filter: str = "", db: Session = Depends(database.get_db)):
    filters = {}
    if filter:
        filters['sku'] = filter
        filters['name'] = filter
    items, total = crud.get_products(db, skip=skip, limit=limit, filters=filters)
    return {"items": items, "total": total}

@app.post("/products")
def create_product(p: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    prod = crud.create_product(db, p)
    return prod

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
