# Pulse Metric - SaaS Feature & Subscription Analytics Platform

A lightweight, event‑driven analytics backend for SaaS companies.
It helps teams understand **which features users actually use** and **how subscriptions change over time**.

This project is intentionally built to be:

* **Professional** (clean architecture, queues, workers, metrics)
* **Scalable‑looking** (event-driven ingestion + async processing)
* **Easy to deploy** (Redis + FastAPI + PostgreSQL)

---

# 🚀 What This Platform Does

This analytics backend allows SaaS products to send events such as:

* **Feature Usage Events** – whenever a user interacts with any feature.
* **Subscription Events** – when a user starts, cancels, upgrades, or downgrades a subscription.

The system ingests these events, processes them asynchronously via a worker, and aggregates metrics daily.

Your client SaaS apps can then query metrics like:

* Most-used features
* Feature usage over time
* Daily active users (feature‑based)
* New subscriptions
* Cancellations
* Upgrades & downgrades
* Net subscription growth

---

# 🧱 Architecture Overview

The project uses a simple but production‑inspired architecture:

```
 Client SaaS App → Ingest API → Redis Queue → Worker → PostgreSQL → Metrics API
```

### Key Components

* **FastAPI – Ingest API**
  Receives events, validates them, and pushes them into Redis.

* **Redis Streams – Event Queue**
  Buffers and stores events for async processing.

* **Worker (Python)**
  Consumes events, stores raw logs, and updates daily aggregated metrics.

* **PostgreSQL**
  Stores projects, event logs, and aggregated daily metrics.

* **Metrics API**
  Serves dashboard-friendly analytics.

For a deeper breakdown, see: [➡️ docs/architecture.md](docs/architecture.md)

---

# 📊 Metrics the System Produces

### **Feature Metrics**

* Feature usage counts (daily/weekly/monthly)
* Feature popularity ranking
* Daily active users (based on feature usage)
* Peak usage times

### **Subscription Metrics**

* New subscriptions
* Cancellations
* Upgrades
* Downgrades
* Active subscriptions
* Daily subscription change summaries
* Net subscription growth


---

# 🔧 Tech Stack

* **FastAPI** (APIs)
* **Python** workers
* **Redis Streams** (queue)
* **PostgreSQL** (storage)
* **Pydantic** (validation)
* **Docker** (for deploying multi-service setup)

---

# 📁 Project Structure (For now)

```
root
│
├── app/
│   ├── api/
│   ├── workers/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   └── utils/
│
├── docs/
│   ├── architecture.md
│   ├── event_payloads.md (optional)
│   ├── database_schema.md (optional)
│   └── queue_design.md (optional)
│
├── tests/
└── README.md
```

---

# 📝 Example Event Integration

### **1. Feature Usage Event**

Your client calls:

```json
POST /v1/events
{
  "type": "feature_used",
  "project_id": "proj_123",
  "user_id": "user_42",
  "feature": "export_pdf",
  "timestamp": "2026-03-01T10:22:44Z"
}
```

### **2. Subscription Event**

```json
POST /v1/events
{
  "type": "subscription_changed",
  "project_id": "proj_123",
  "user_id": "user_42",
  "from_plan": "basic",
  "to_plan": "pro",
  "timestamp": "2026-03-01T11:29:00Z"
}
```

---

# 🧪 Running Locally

```
uvicorn app.main:app --reload
```

If using Redis + worker:

```
redis-server
python worker.py
```

---


# 📬 Future Enhancements

* JavaScript SDK for sending events
* Rate limiting and quotas
* Single-tenant / multi-tenant mode
* Cohort analysis
* Funnels
* Trigger-based alerts (Slack/email)

---

# 📄 License

MIT License


