# 🚀 Acme Product Importer

A high-performance, scalable CSV Product Importer built with **FastAPI**, **Celery**, **Redis**, **PostgreSQL**, and **Docker**.  
Supports importing **500,000+ products**, real-time progress updates, CRUD UI, webhooks, and cloud deployment.

---

## ✨ Features

### 📂 CSV Upload (500k+ Records)
- Upload large CSV files through the UI  
- Streams file efficiently (no memory overload)  
- Overwrites duplicates automatically (case-insensitive SKU)  
- Background processing using Celery  

### 📊 Real-Time Import Progress
- Track progress via job ID  
- Progress bar + status messages (Parsing, Processing, Completed, Failed)  
- Error visibility and retry support  

### 🛒 Product Management UI
- View all products  
- Search & filter (SKU, name, description, active)  
- Pagination  
- Create / Update / Delete  
- Clean, minimal UI  

### 🗑️ Bulk Delete
- Delete all products at once  
- Includes confirmation dialog  
- Shows success/failure alerts  

### 🔔 Webhook Management
- Add, edit, delete webhooks  
- Select event types  
- Enable/disable  
- Test webhook and see response  

### 🐳 Fully Containerized🔌 API Endpoints
Upload CSV

POST /upload
Check Job Progress

GET /jobs/{job_id}
Product CRUD

GET /products
POST /products
PUT /products/{id}
DELETE /products/{id}
Bulk Delete

POST /products/delete_all
Webhooks

Full CRUD + Test endpoints
☁️ Deployment (Render Example)

You need:

    Web Service (Docker)

    Worker Service (Docker)

    Redis Instance

    PostgreSQL Instance

Required Environment Variables

DATABASE_URL=<render-postgres-url>
CELERY_BROKER_URL=redis://<redis-host>:6379/1
CELERY_RESULT_BACKEND=redis://<redis-host>:6379/2

Web Service Start Command

uvicorn app.main:app --host 0.0.0.0 --port 8000

Worker Service Start Command

celery -A app.tasks.celery_app worker --loglevel=info -Q imports,webhooks

🚀 Performance Notes

    CSV streamed line-by-line to prevent memory overload

    Bulk upserts for database efficiency

    Celery worker ensures non-blocking requests

    Scalable architecture suitable for high-load environments


- Dockerized backend, worker, Redis, and PostgreSQL  
- Easy local development and cloud deployment  

---

## 🛠 Tech Stack

| Component      | Technology |
|----------------|-----------|
| Backend API    | FastAPI |
| Async Worker   | Celery |
| Broker         | Redis |
| Database       | PostgreSQL |
| ORM            | SQLAlchemy |
| Frontend       | HTML + JS |
| Deployment     | Docker / Render |

---

## 📁 Project Structure

acme-product-importer/
├── backend/
│ ├── app/
│ ├── requirements.txt
│ ├── Dockerfile
├── frontend/
│ ├── index.html
├── docker-compose.yml
├── .env.example
└── README.md


---

## ⚙️ Local Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/acme-product-importer.git

cd acme-product-importer
```
2.Create env file
```bash
cp .env.example .env
```

3.start apps
docker compose up --build
4.open browser
http://localhost:8000

example format for CSV
sku,name,description,price
SKU001,Product A,Description A,10.99
SKU002,Product B,Description B,14.50

🔌 API Endpoints
Upload CSV

POST /upload

Check Job Progress

GET /jobs/{job_id}

Product CRUD

GET /products
POST /products
PUT /products/{id}
DELETE /products/{id}

Bulk Delete

POST /products/delete_all

Webhooks

Full CRUD + Test endpoints

☁️ Deployment 
Live App: https://product-importer2.onrender.com/

📄 Sample CSV

You can download the products.csv file from the project root to test the import flow.

🔧 Creating a Custom CSV
1. Download script.py from the project root.

2. Open the file and modify the line:
```python  ```
TOTAL_ROWS = 499999
``` ```
Set it to any integer value you prefer.
3. Run the script to generate a CSV file with that number of rows.

You need:

Web Service (Docker)

Worker Service (Docker)

Redis Instance

PostgreSQL Instance

Required Environment Variables

