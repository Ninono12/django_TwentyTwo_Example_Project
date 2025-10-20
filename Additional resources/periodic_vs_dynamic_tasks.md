# Periodic vs Dynamic Tasks in Celery

## What’s the Difference?

In Celery, tasks can be scheduled in two main ways:

1. **Periodic Tasks** – Run on a **recurring, fixed schedule**.
2. **Dynamic Tasks** – Scheduled **on the fly**, based on real-time conditions.

Both have their purpose. Let’s explore them in detail.

---

## 1. Periodic Tasks

These are **predefined**, recurring tasks. You configure them **once**, and they keep running at regular intervals.

📦 Typically defined using `django-celery-beat`.

### Use Cases

* Send daily newsletters
* Sync data every hour
* Run weekly reports

### Example (with `django-celery-beat`)

```python
# tasks.py
@shared_task
def send_newsletter():
    # logic here
    pass
```

You’d then set the schedule using the Django admin (under **Periodic Tasks**).

---

### ⚙️ How It Works

* **Celery Beat** (the scheduler) runs in the background.
* It checks the database (or schedule file) for any due tasks.
* When the time matches, Beat pushes the task into the Celery queue.
* Celery **workers** then pick it up and execute it.

🧠 Think of it like a **calendar reminder**: it will always trigger on schedule.

---

### 🧩 Characteristics

| Feature              | Description                                      |
| -------------------- | ------------------------------------------------ |
| **Setup**            | Configured once in admin or code                 |
| **Recurrence**       | Runs automatically on a fixed interval           |
| **Persistence**      | Stored in database (or file) — survives restarts |
| **Scheduler Needed** | ✅ Requires Celery Beat                           |
| **Flexibility**      | Limited — tied to fixed schedules                |

---

## ⚡ 2. Dynamic Tasks

These are **programmatically scheduled** tasks — you decide when they should run based on runtime logic, user actions, or external events.

They use Celery’s `.apply_async()` method, allowing you to set custom execution times dynamically.

### Use Cases

* Send email 1 hour after registration
* Cancel an order if payment not received in 10 minutes
* Trigger reminders based on user preferences or inputs

### Example

```python
from datetime import timedelta
from django.utils import timezone
from myapp.tasks import send_reminder_email

send_reminder_email.apply_async(
    args=['user@example.com'],
    eta=timezone.now() + timedelta(minutes=10)
)
```

This sends the email **10 minutes after** the function is called — dynamically scheduled per user or event.

---

### ⚙️ How It Works

* You call `.apply_async()` in your code when you need the task.
* Celery handles the timing internally — it can execute immediately or later.
* Once scheduled, it doesn’t repeat automatically (you’d need to re-trigger it).

🧠 Think of it like **setting a one-time reminder manually** when something happens.

---

## 🕒 `.delay()` vs `.apply_async()`

Both methods run Celery tasks asynchronously, but there’s a key difference:

| Method                                                       | What It Does                                                   | Scheduling Options       |
| ------------------------------------------------------------ | -------------------------------------------------------------- | ------------------------ |
| `task.delay(*args, **kwargs)`                                | Shortcut for running a task **immediately**.                   | ❌ None — runs now        |
| `task.apply_async(args=None, countdown=None, eta=None, ...)` | Fully customizable — lets you **delay or schedule** execution. | ✅ Can delay or run later |

### Examples

```python
# Runs immediately
send_email.delay("user@example.com")

# Runs after 5 minutes
from datetime import timedelta
from django.utils import timezone

send_email.apply_async(
    args=["user@example.com"],
    eta=timezone.now() + timedelta(minutes=5)
)
```

So:

> `.delay()` = shorthand for `.apply_async()` **without scheduling options**.
> **Dynamic tasks** usually rely on `.apply_async()` with timing arguments.

---

## 🧠 Key Technical Differences

| Aspect           | **Periodic Tasks**                     | **Dynamic Tasks**              |
| ---------------- | -------------------------------------- | ------------------------------ |
| **Defined in**   | Admin panel / database / code (static) | In code, triggered dynamically |
| **Scheduler**    | ✅ Requires Celery Beat                 | ❌ No external scheduler        |
| **Recurrence**   | ✅ Automatic                            | ❌ One-time unless re-triggered |
| **Persistence**  | ✅ Stored in DB                         | ❌ Ephemeral                    |
| **Triggered by** | Time or fixed interval                 | User events / business logic   |
| **Best for**     | Repeating jobs (daily/hourly)          | On-demand, event-based jobs    |

---

## 🧾 Real-World Examples

### 🕒 Periodic Task (Daily)

```python
# settings.py
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'send_daily_summary': {
        'task': 'myapp.tasks.send_daily_summary',
        'schedule': crontab(hour=0, minute=0),  # every midnight
    },
}
```

Runs automatically every day at midnight.

---

### ⚡ Dynamic Task (After Event)

```python
# views.py
from datetime import timedelta
from django.utils import timezone
from myapp.tasks import send_reminder

def schedule_user_reminder(user):
    send_reminder.apply_async(
        args=[user.email],
        countdown=60 * 30  # 30 minutes from now
    )
```

Runs **30 minutes after** a user action — customized for that specific event.

---

## 📊 Comparison Table

| Feature             | **Dynamic Task**             | **Periodic Task (`django-celery-beat`)** |
| ------------------- | ---------------------------- | ---------------------------------------- |
| Scheduled in code?  | ✅ Yes                        | ❌ (Configured in DB/Admin)               |
| Flexible timing     | ✅ Fully flexible             | ❌ Fixed intervals                        |
| Triggered by events | ✅ Yes                        | ❌ No                                     |
| Recurring support   | ❌ Manual re-trigger required | ✅ Automatic                              |
| Scheduler required  | ❌ No                         | ✅ Yes (Celery Beat)                      |
| Persistence         | ❌ Temporary                  | ✅ Stored in DB/File                      |
| Best for            | On-demand, user-driven jobs  | Repetitive, time-based jobs              |

---

## 🧰 Summary

* Use **Periodic Tasks** when your job must **repeat on a known schedule** (daily, hourly, weekly).
* Use **Dynamic Tasks** when the schedule depends on **runtime logic, user behavior, or custom timing**.
* Use `.delay()` for **immediate** task execution.
* Use `.apply_async()` for **controlled scheduling** (e.g., run later or after an event).
