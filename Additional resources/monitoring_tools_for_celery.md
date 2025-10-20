# Monitoring Tools for Celery

## Why Monitor Celery?

Monitoring helps ensure your **Celery workers** and **tasks** are:

* Running as expected ✅
* Not stuck, failing, or retrying too often ❌
* Efficient in resource usage ⏳

---

## Popular Monitoring Tools

### 1. **Flower** – Real-time Web-based Monitoring

**Flower** is a lightweight web UI for monitoring Celery:

#### Installation:

```bash
pip install flower
```

#### Run Flower:

```bash
celery -A your_project flower
```

Visit [http://localhost:5555](http://localhost:5555) in your browser.

#### Features:

* Task monitoring (success, failure, retries)
* Task details and execution time
* Real-time worker status
* Queues overview

---

### 2. **Prometheus + Grafana** (Advanced)

For production setups needing advanced metrics.

* Prometheus scrapes task metrics.
* Grafana visualizes charts, trends, and alerts.

> Requires `celery-prometheus-exporter` or custom instrumentation.

---

### 3. **Sentry** – Error Reporting for Celery Tasks

If you're using [Sentry](https://sentry.io/) for Django, it can also track Celery errors.

#### ✅ Setup:

Install the SDK:

```bash
pip install sentry-sdk
```

Initialize in `celery.py`:

```python
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

sentry_sdk.init(
    dsn="your_sentry_dsn",
    integrations=[CeleryIntegration()],
)
```

---

### 4. **Django Admin** (for Beat only)

If you're using **django-celery-beat**, you can:

* View upcoming periodic tasks
* Check schedule configurations
* Manually trigger or pause tasks

---

## ✅ Summary Table

| Tool         | Purpose                      | Use Case                  |
| ------------ | ---------------------------- | ------------------------- |
| Flower       | Real-time dashboard          | Local & staging           |
| Sentry       | Error logging & stack traces | Debug production issues   |
| Prometheus   | Task metrics & alerts        | Enterprise-grade setups   |
| Django Admin | Beat schedule inspection     | Admin-friendly scheduling |
