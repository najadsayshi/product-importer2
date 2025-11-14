import os
from celery import Celery
from celery.utils.log import get_task_logger
from .crud import bulk_upsert_products, update_job_progress
from .database import engine, SessionLocal
from .utils import stream_csv_rows

logger = get_task_logger(__name__)

# Celery application
celery_app = Celery(
    "app",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
)

# Route this task to imports queue
celery_app.conf.task_routes = {
    "process_csv_import": {"queue": "imports"},
}

@celery_app.task(bind=True, name="process_csv_import", queue="imports")
def process_csv_import(self, job_id: str, filepath: str, batch_size: int = 1000):
    db = SessionLocal()
    try:
        # Count total rows
        total = 0
        with open(filepath, "r", encoding="utf-8") as f:
            for _ in f:
                total += 1
        total = max(total - 1, 0)

        update_job_progress(db, job_id, processed=0, total=total, status="RUNNING")

        batch = []
        processed = 0

        for row in stream_csv_rows(filepath):

            sku = (row.get("sku") or row.get("SKU") or "").strip()
            if not sku:
                continue

            rec = {
                "sku": sku,
                "sku_lower": sku.lower(),
                "name": row.get("name") or row.get("title") or None,
                "description": row.get("description") or None,
                "price": float(row.get("price") or 0) if row.get("price") else None,
                "active": True,
            }

            batch.append(rec)

            if len(batch) >= batch_size:
                n = bulk_upsert_products(engine, batch)
                processed += n
                update_job_progress(db, job_id, processed=processed)
                batch = []

        if batch:
            n = bulk_upsert_products(engine, batch)
            processed += n
            update_job_progress(db, job_id, processed=processed)

        update_job_progress(db, job_id, processed=processed, status="SUCCESS")

    except Exception as e:
        update_job_progress(
            db,
            job_id,
            processed=processed if "processed" in locals() else 0,
            status="FAILED",
            errors=[str(e)],
        )
        logger.exception("Import failed")

    finally:
        db.close()
