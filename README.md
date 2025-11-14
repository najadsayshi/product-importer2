🚀 Acme Product Importer

High-performance CSV product importer with FastAPI, Celery, Redis, PostgreSQL & Docker

This project implements a scalable backend system capable of importing 500,000+ product records from CSV while remaining responsive.
It includes:

File upload via UI

Real-time upload progress

Celery background processing

SQL-based product management UI

Webhook management

Fully containerized via Docker

📦 Features
✅ 1. Large CSV Upload (500k+ rows)

Upload CSV files through the UI

Real-time progress updates (polling)

Handles large files without blocking the server

Duplicate SKUs automatically overwritten (case-insensitive)

✅ 2. Background Processing (Celery + Redis)

File import runs asynchronously using a Celery worker

CSV parsed in streaming mode (no memory spike)

Progress updates stored & shown to the user

✅ 3. Product Management UI

View products (paginated)

Search by SKU, name, or description

Create / Update / Delete products

Delete-all option with confirmation

✅ 4. Webhooks UI

Add / Edit / Delete webhook URLs

Test webhook delivery

Supports event types & enable/disable

✅ 5. Fully Containerized

Docker Compose for local development

Uses Postgres + Redis services

🛠️ Tech Stack
Component	Technology
Backend API	FastAPI
Async Worker	Celery
Messaging	Redis
Database	PostgreSQL
ORM	SQLAlchemy
Frontend	HTML + JS (no framework required)
Deployment	Docker / Render
