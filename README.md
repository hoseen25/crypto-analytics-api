# 📈 Real-Time Cryptocurrency Analytics API

A high-performance, production-ready backend system designed to fetch, validate, and process live financial data streams from public Web APIs, serving aggregated data trends through a fast RESTful API.

---

## 🚀 Key Features & Highlights

* **Automated Live Data Ingestion:** Background workers that stream and process live crypto market data.
* **Production-Grade Resilience:** Built-in mechanisms to handle API rate-limiting (429), network timeouts, and data anomalies gracefully.
* **Optimized Data Layer:** Relational database schema with optimized indexing and complex SQL aggregations for time-series crypto trends.
* **High-Performance API:** FastAPI-driven REST API utilizing asynchronous routing for lightning-fast query responses.
* **Secure & Scalable:** Fully containerized environment using Docker, strict environment variable segregation, and clean MVC architecture.

---

## 🛠️ Tech Stack

* **Backend Framework:** Python, FastAPI (Uvicorn)
* **Database & ORM:** PostgreSQL / SQLite, SQLAlchemy
* **Validation & Environment:** Pydantic, Python-Dotenv
* **DevOps & Infrastructure:** Linux (Ubuntu), Git, GitHub

---

## 📐 System Architecture & Data Flow



1. **Ingestion Layer:** Background tasks periodically fetch raw financial metrics from external Crypto Web APIs.
2. **Resilience & Validation Layer:** Data passes through Pydantic validators. Network exceptions, timeouts, and API rate-limits are caught and handled via automated retry backoffs.
3. **Storage & Aggregation Layer:** Clean data is upserted into the relational database. Complex SQL queries aggregate 24h volumes and moving averages efficiently.
4. **Delivery Layer:** FastAPI endpoints serve cached or highly-optimized queries back to the client in milliseconds.

---

## 🔒 Production Best Practices Implemented

### 1. Zero-Secrets Leakage (Security First)
No hardcoded credentials. All database URIs, API keys, and server configurations are dynamically loaded from an ignored `.env` file using `python-dotenv`.

### 2. Defensive Programming & Error Recovery
Network operations are wrapped with robust try-except blocks handling:
* `requests.exceptions.HTTPError` (specifically watching for Rate Limits).
* `KeyError / ValidationError` to filter out corrupted API payloads before touching the DB.

### 3. Database Integrity
Using SQLAlchemy sessions context-managers to guarantee that database connections are always closed safely, preventing memory leaks or hanging connection pools in production.

---

## 🏁 Getting Started

### Prerequisites
* Python 3.10+
* Virtual Environment tool (`venv`)

### Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/hoseen25/crypto-analytics-api.git](https://github.com/hoseen25/crypto-analytics-api.git)
   cd crypto-analytics-api
