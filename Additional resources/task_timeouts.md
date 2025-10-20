# Task Timeouts in Celery

## What Are Task Timeouts?

A **task timeout** is the maximum time a Celery worker allows a task to run before it is **terminated or revoked**.

Timeouts help:

* Avoid tasks running indefinitely.
* Free up worker resources.
* Ensure responsiveness and stability.

---

## Types of Timeouts in Celery

| Timeout Type        | Description                                                                                              |
| ------------------- | -------------------------------------------------------------------------------------------------------- |
| **Soft Time Limit** | Sends a `SoftTimeLimitExceeded` exception inside the task, allowing graceful cleanup before termination. |
| **Hard Time Limit** | Forces immediate termination of the task by killing the worker process. No cleanup.                      |

---

## How to Set Task Timeouts

You can set timeouts globally or per task.

### 1. Global Timeout (in `celery.py` or `settings.py`)

```python
app.conf.task_soft_time_limit = 300  # 5 minutes
app.conf.task_time_limit = 310       # 5 minutes + 10 seconds hard limit
```

### 2. Per-Task Timeout

```python
from celery import shared_task

@shared_task(soft_time_limit=60, time_limit=70)  # seconds
def long_running_task():
    # task logic here
    pass
```

---

## Handling Soft Timeout Exception

When the soft time limit is reached, Celery raises `SoftTimeLimitExceeded` inside the task.

You can catch it to perform cleanup:

```python
from celery.exceptions import SoftTimeLimitExceeded

@shared_task(soft_time_limit=60)
def my_task():
    try:
        # long process
        pass
    except SoftTimeLimitExceeded:
        # cleanup code here
        print("Task took too long and was interrupted!")
```

---

## ⚠ Why Use Both Soft and Hard Time Limits?

* **Soft time limit** gives your task a chance to stop safely.
* **Hard time limit** guarantees the task will not run beyond the specified time (even if cleanup code hangs).

---

## Summary Table

| Feature           | Description                                   |
| ----------------- | --------------------------------------------- |
| `soft_time_limit` | Graceful timeout, raises exception to task    |
| `time_limit`      | Hard kill timeout, immediately terminates     |
| Catch Exception   | Use `SoftTimeLimitExceeded` to handle cleanup |
| Usage             | Prevents infinite/hanging tasks               |
