from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Dict, Any
import psycopg2.extras
from sqlalchemy import text

def create_tables(engine):
    models.Base.metadata.create_all(bind=engine)

def create_import_job(db: Session, job_id: str, filename: str):
    job = models.ImportJob(id=job_id, filename=filename, status='PENDING')
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def update_job_progress(db: Session, job_id, processed, total=None, status=None, errors=None):
    job = db.query(models.ImportJob).filter(models.ImportJob.id == job_id).first()
    if not job:
        return
    if total is not None:
        job.total_rows = total
    job.processed_rows = processed
    if status:
        job.status = status
    if errors is not None:
        job.errors = errors
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def get_job(db: Session, job_id):
    return db.query(models.ImportJob).filter(models.ImportJob.id == job_id).first()

def bulk_upsert_products(engine, rows: List[Dict[str, Any]]):
    """
    rows: list of dicts with keys: sku, sku_lower, name, description, price, active
    uses psycopg2.extras.execute_values for bulk upsert
    """
    if not rows:
        return 0
    conn = engine.raw_connection()
    try:
        with conn.cursor() as cur:
            sql = """
            INSERT INTO products (sku, sku_lower, name, description, price, active)
            VALUES %s
            ON CONFLICT (sku_lower) DO UPDATE
            SET sku = EXCLUDED.sku,
                name = EXCLUDED.name,
                description = EXCLUDED.description,
                price = EXCLUDED.price,
                active = EXCLUDED.active,
                updated_at = now()
            """
            values = [
                (r.get('sku'), r.get('sku_lower'), r.get('name'), r.get('description'),
                 r.get('price'), r.get('active', True)) for r in rows
            ]
            psycopg2.extras.execute_values(cur, sql, values, template=None, page_size=1000)
        conn.commit()
        return len(rows)
    finally:
        conn.close()

# Basic product CRUD for UI
def get_products(db: Session, skip: int = 0, limit: int = 50, filters: dict = None):
    q = db.query(models.Product)
    if filters:
        if 'sku' in filters:
            q = q.filter(models.Product.sku.ilike(f"%{filters['sku']}%"))
        if 'name' in filters:
            q = q.filter(models.Product.name.ilike(f"%{filters['name']}%"))
        if 'description' in filters:
            q = q.filter(models.Product.description.ilike(f"%{filters['description']}%"))
        if 'active' in filters:
            q = q.filter(models.Product.active == filters['active'])
    total = q.count()
    items = q.order_by(models.Product.id).offset(skip).limit(limit).all()
    return items, total

def create_product(db: Session, p: schemas.ProductCreate):
    product = models.Product(
        sku=p.sku,
        sku_lower=p.sku.lower(),
        name=p.name,
        description=p.description,
        price=p.price,
        active=p.active
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def update_product(db: Session, product_id: int, p: schemas.ProductCreate):
    product = db.query(models.Product).get(product_id)
    if not product:
        return None
    product.sku = p.sku
    product.sku_lower = p.sku.lower()
    product.name = p.name
    product.description = p.description
    product.price = p.price
    product.active = p.active
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
    product = db.query(models.Product).get(product_id)
    if not product:
        return False
    db.delete(product)
    db.commit()
    return True

def delete_all_products(db: Session):
    n = db.query(models.Product).delete()
    db.commit()
    return n
