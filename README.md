# E-commerce Catalog API – FastAPI + MongoDB (Document Data Model)

Production-grade reference implementation for **Part 2** of the series: *5 Data Models, 5 Use Cases, 5 Vendors*.

**Use case:** E-commerce product catalog with flexible attributes, variants, and search. 
**Stack:** FastAPI, PyMongo, Docker, mongo-express, Gunicorn.

---

## 🔧 Features
- Document-first modeling (MongoDB) with nested variants & attributes
- Clean FastAPI structure + PyMongo client pooling
- Full-text search + faceted filtering via aggregation
- Unique product IDs and essential secondary indexes
- Docker Compose with MongoDB + mongo-express UI
- Health checks and production server (Gunicorn+Uvicorn)

---

## 🚀 Quickstart
```bash
cp .env.example .env
# optionally tweak ports and origins in .env

docker compose up --build -d
# API → http://localhost:8000/docs
# Mongo Express → http://localhost:8082
```

Seed the DB (optional):
```bash
# in a separate shell
docker exec -it mongo mongosh \
  -u catalog_user -p catalog_pass \
  --eval 'db = db.getSiblingDB("catalog"); db.products.insertMany(JSON.parse(cat("/seed/products.json")))'
```

---

## 🧱 API Endpoints
- `GET /healthz` – liveness probe
- `POST /products/` – create product
- `GET /products/{product_id}` – fetch product
- `PUT /products/{product_id}` – upsert product
- `DELETE /products/{product_id}` – delete product
- `GET /products/search` – full-text + filters + facets

**Search examples:**
```
/products/search?q=headphones&category=audio&min_price=50&max_price=200&limit=10
/products/search?brand=SoundMax
```

---

## 🗄️ Indexes
Created via `scripts/init-mongo.js` at container startup:
- `product_id` unique
- `categories` (multikey)
- `brand`
- `price`
- text index on `name, description, brand`

---

## 🧪 Local Smoke Tests
```bash
# after compose is up
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q tests/test_products.py  # uses http://localhost:8000
```

---

## 🏗️ Design Notes (Why Document Model Here?)
- Product attributes vary widely (size/color/specs). JSON documents avoid schema churn.
- Variants are naturally nested, minimizing joins and round-trips.
- Text search + category filters map cleanly to indexes and aggregation pipelines.

**When NOT to use a document model:** strong cross-document transactions, heavy relational constraints, or complex reporting requiring joins across many entities.

---

## 🔒 Production Tips
- Configure proper auth/roles in MongoDB (this demo uses a simple user)
- Add rate limiting & request validation on public endpoints
- Consider read replicas and pinned reads for analytics
- Backup & PITR: use MongoDB backups or cloud snapshots

---

## 🧭 Next Steps in the Series
Part 1: Relational – Banking Ledger (PostgreSQL)
Part 2: **Document – E-commerce Catalog (MongoDB)** ← this repo
Part 3: Graph – Recommendations & Fraud Rings (Neo4j)
Part 4: Time-Series – Metrics/IoT (InfluxDB)
Part 5: Key-Value – Caching & Sessions (Redis)
