# SaaS Analytics Platform Architecture

This document describes the full technical architecture for the **SaaS Usage & Subscription Analytics Platform**. It is designed to be GitHub‑ready, simple to understand, and professional enough for your portfolio.

---

## 1. High‑Level Overview

The system ingests analytics events from external SaaS applications, validates them, stores raw events, processes them asynchronously, computes metrics, and exposes aggregated insights through dashboard APIs.

**Core components:**

* **Event Ingestion API** – Receives events from client apps.
* **Authentication Layer** – Validates project API keys.
* **Raw Events Store** – Stores all incoming events.
* **Message Queue** – Decouples ingestion from processing.
* **Background Workers** – Process events into aggregated metrics.
* **Computed Metrics Store** – Optimized for analytics queries.
* **Dashboard API** – Serves metrics to frontend dashboard.

---

## 2. Flow Diagram (Text Representation)

```
Client → API Gateway → Validator → Raw Events → Queue
                                        ↓
                                Background Workers
                                        ↓
                                Metrics Tables
                                        ↓
                                 Dashboard API
```

---

## 3. Component Breakdown

### **3.1 Event Ingestion API**

* Exposes a `/track` endpoint for incoming events.
* Accepts event types:

  * Feature usage events
  * Subscription lifecycle events
  * User activity events
* Requests include project API keys.
* Returns a success response immediately to ensure low latency.

### **3.2 Authentication Layer**

* Every project receives an API key upon creation.
* Incoming requests include the key in headers.
* API key determines **tenant isolation**.

### **3.3 Validation & Normalization**

* Event schema is validated on ingestion.
* Invalid events are dropped or flagged.
* Timestamps normalized to UTC.
* Missing optional fields handled gracefully.

### **3.4 Raw Events Storage**

* All validated events are stored in a `raw_events` table.
* This acts as a **source of truth**.
* Enables reprocessing if worker logic changes.

---

## 4. Asynchronous Processing

### **4.1 Why a Queue?**

* Prevents ingestion API from slowing down.
* Allows scalable processing.
* Supports retries on worker failure.

### **4.2 Background Workers**

Workers are separated by domain to keep logic clean:

#### **Feature Worker**

* Processes feature_viewed, feature_used, feature_completed
* Updates:

  * Daily feature usage counts
  * Unique users per feature

#### **Subscription Worker**

* Processes subscription_created, subscription_cancelled, plan_upgraded
* Updates:

  * Active subscriptions
  * Churn
  * Trial-to-paid conversions

#### **Activity Worker**

* Processes user_logged_in, session_started
* Computes:

  * DAU / WAU
  * Returning vs new users
  * Session statistics

---

## 5. Data Storage Model

### **5.1 Raw Layer**

* `raw_events` table keeps everything.
* Supports replay and reprocessing.

### **5.2 Computed Layer**

Workers aggregate results into summary tables such as:

* `daily_active_users`
* `feature_usage_daily`
* `subscription_metrics_daily`

### **Why two layers?**

* Raw = durable, flexible.
* Computed = fast queries for dashboards.

This follows a **mini data‑warehouse pattern**.

---

## 6. Dashboard API Layer

The Dashboard API fetches aggregated metrics and powers charts.

Endpoints include:

* `/dashboard/overview`
* `/dashboard/features`
* `/dashboard/subscriptions`

Each endpoint pulls from **computed tables**, not raw events.

This ensures:

* Consistent performance
* Fast responses
* Clean separation of concerns

---

## 7. Scaling Considerations

### **7.1 Horizontal Scaling**

* API servers can scale independently.
* Workers can scale per domain (feature, subscription, activity).

### **7.2 Queue Durability**

* Queue ensures events are never lost.
* Allows back-pressure handling under high traffic.

### **7.3 Multi-Tenant Isolation**

* All tables include a `project_id` field.
* Prevents cross-tenant data leakage.

---

## 8. Tech Stack (suggested)

* **Backend Framework:** FastAPI
* **Database:** PostgreSQL
* **Queue:** Redis Streams or RabbitMQ
* **Worker Engine:** Celery, RQ, or custom consumer loop
* **Hosting:** Render, Railway, Fly.io, or Docker Compose

---

## 9. Summary

This architecture:

* Is production-grade but portfolio-friendly.
* Demonstrates familiarity with real SaaS analytics.
* Shows event-driven thinking and domain separation.
* Provides a clean structure that recruiters will respect.

This document should be placed in `/docs/architecture.md` in your GitHub repository.

