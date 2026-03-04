# Pulse Metric Architecture


## 🎯 Goal

A lightweight, production‑inspired analytics backend that helps SaaS companies track:

* **Feature usage** (any feature they define)
* **Subscription metrics** (active subscriptions, churn, upgrades, downgrades)

---
  
# 🧱 High-Level Architecture

```
                   +----------------------+
                   |   Client SaaS App    |
                   +----------+-----------+
                              |
                              | HTTPS
                              v
       +------------------------------------------------+
       |                API Gateway / Ingest            |
       | - Auth via API Key                             |
       | - Validate incoming event payload              |
       | - Fast response (202 Accepted)                 |
       +----------------------+-------------------------+
                              |
                              | Publish event
                              v
                 +---------------------------+
                 |     Event Queue (Redis)   |
                 +-------------+-------------+
                               |
                               | Consume
                               v
                +----------------------------+
                |      Worker Service        |
                | - Parse event              |
                | - Normalize + store        |
                | - Aggregate metrics        |
                +--------------+-------------+
                               |
                               v
          +------------------------------------------------+
          |             Database (PostgreSQL)              |
          |  event_logs     subscription_events   metrics  |
          +------------------------------------------------+

                              |
                              | Query
                              v
                    +-------------------------+
                    |     Metrics API         |
                    |  (Dashboard Backend)    |
                    +-----------+-------------+
                                |
                                v
                            Frontend
```

---

# 📦 Components Breakdown

## 1. Ingest API (FastAPI)

Handles all incoming events from SaaS applications.

Responsibilities:

* Authenticate using API key
* Validate event payloads
* Route event types:

  * `feature_used`
  * `subscription_started`
  * `subscription_changed`
  * `subscription_canceled`
* Push events to Redis queues
* Return **202 Accepted** immediately

Why? To keep writes super fast.

---

## 2. Event Queue (Redis Streams)

The queue is the buffer between the ingest layer and the workers.

Benefits:

* Spikes in traffic won't overload workers
* Retries are easy
* Durable enough for a portfolio project

Event example stored in queue:

```json
{
  "project_id": "proj_123",
  "user_id": "u_55",    // optional for feature events
  "type": "feature_used",
  "feature": "export_to_pdf",
  "timestamp": "2026-03-03T12:00:11Z"
}
```

---

## 3. Worker Service

A background service (separate FastAPI process or Celery worker) that:

### Workflows

#### **A. Feature Usage Event**

* Insert event log into `feature_usage_events`
* Update aggregated metrics table:

  * Increment daily count
  * Increment weekly count
  * Increment monthly count
  * (optional) track unique users

#### **B. Subscription Events**

Simplified model:

* No per-user full history
* Only store timestamped subscription events

Worker updates tables:

* Insert into `subscription_events`
* Recompute:

  * Active subscriptions
  * Churn count
  * New subscriptions
  * Upgrades
  * Downgrades

---

## 4. Database (PostgreSQL)

### Tables

#### `projects`

Projects that use your platform.

#### `feature_usage_events`

Raw events.

#### `daily_feature_metrics`

Aggregated counts.

#### `subscription_events`

Raw subscription events only.

#### `daily_subscription_metrics`

Aggregated subscription summaries (the primary thing dashboards use).

This keeps queries fast and your system scalable.

---


# 📊 Metrics Produced


### **Feature Usage Metrics**

* Daily active users (based on feature events)
* Feature popularity list
* Feature usage trends
* Peak usage times

### **Subscription Metrics**

* Active subscriptions
* New vs. canceled subscriptions
* Upgrades / downgrades
* Daily subscription changes
* Basic churn rate


---

# 🚀 Deployment Model

### Minimal setup

* FastAPI (Ingest + Metrics API)
* Redis (queue)
* Python Worker (Celery / RQ / custom)
* PostgreSQL (RDS / Railway / Supabase)


