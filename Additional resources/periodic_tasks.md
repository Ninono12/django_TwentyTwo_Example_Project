# Django Celery – Periodic Tasks with Celery Beat

## What Are Periodic Tasks?

**Periodic tasks** are tasks that run automatically on a schedule — like cron jobs — using **Celery Beat**, the scheduler that adds recurring tasks to your Celery queue.

### Common Use Cases

* Send weekly or daily emails
* Clean up expired sessions
* Generate daily reports
* Sync data with external APIs

---

## ⚙️ Requirements

Make sure both `celery` and `django-celery-beat` are installed:

```bash
pip install django-celery-beat
```

Add to your Django settings:

```python
# settings.py
INSTALLED_APPS = [
    ...
    'django_celery_beat',
]
```

Then run migrations so Celery Beat can create its database tables:

```bash
python manage.py migrate django_celery_beat
```

---

## 🛠 Configure Beat Scheduler

In your `settings.py`, tell Celery to use the database-backed scheduler:

```python
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
```

This lets you manage schedules directly through the **Django Admin** or via code.

---

## ✅ Registering Periodic Tasks via Django Admin

1. Go to the **Django Admin panel**.
2. You’ll see new models: **Periodic Tasks**, **Interval Schedules**, **Crontab Schedules**, and **Solar Schedules**.
3. Create a new **Periodic Task**:

   * **Task name** → e.g., `your_app.tasks.auto_close_old_orders`
   * **Schedule type** → select Interval or Crontab
   * **Enabled** → ✔️ checked

> 💡 Make sure your task is defined and registered with `@shared_task` in your app’s `tasks.py`.

---

## 🧩 Example: Run Daily Task to Close Old Orders

```python
# your_app/tasks.py

from celery import shared_task

@shared_task
def auto_close_old_orders():
    # Your logic here
    print("Closing old orders...")
```

Then in Django Admin:

* **Task name**: `your_app.tasks.auto_close_old_orders`
* **Crontab schedule**: every day at midnight

Celery Beat will now trigger this automatically every day.

---

## ⚡ Optional: Create Periodic Tasks Programmatically

You can also **seed** periodic tasks in code instead of using the Admin UI.

This is useful for:

* Auto-creating default schedules on deployment
* Ensuring required tasks always exist

### Example Code

```python
# your_app/utils.py (or management/commands/setup_tasks.py)

from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

def create_periodic_task():
    # 1. Define schedule (every 1 day)
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.DAYS,
    )

    # 2. Create the task entry if it doesn’t already exist
    PeriodicTask.objects.get_or_create(
        interval=schedule,
        name='Close old orders daily',
        task='your_app.tasks.auto_close_old_orders',
        defaults={'args': json.dumps([])},
    )
```

---

### 🗂 Where to Put This Code

There are **two common ways** to execute this automatically:

#### **Option 1 – Inside `AppConfig.ready()`**

This runs once when Django starts (after all apps are loaded).

```python
# your_app/apps.py

from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'your_app'

    def ready(self):
        from .utils import create_periodic_task
        create_periodic_task()
```

> ⚠️ Use this only if you’re sure it won’t cause duplicate task creation in multi-worker setups.
> For production, **Option 2** is safer.

---

#### **Option 2 – Via a Management Command**

Create a custom Django command that seeds periodic tasks when needed.

```python
# your_app/management/commands/setup_periodic_tasks.py

from django.core.management.base import BaseCommand
from your_app.utils import create_periodic_task

class Command(BaseCommand):
    help = "Create default periodic tasks"

    def handle(self, *args, **options):
        create_periodic_task()
        self.stdout.write(self.style.SUCCESS('✅ Periodic tasks created/updated'))
```

Then run manually or during deployment:

```bash
python manage.py setup_periodic_tasks
```

---

## 🧠 Summary

| Step                 | Description                                      |
| -------------------- | ------------------------------------------------ |
| **1. Install**       | `django-celery-beat` and add to `INSTALLED_APPS` |
| **2. Migrate**       | `python manage.py migrate django_celery_beat`    |
| **3. Configure**     | Set `CELERY_BEAT_SCHEDULER` in `settings.py`     |
| **4. Register Task** | Via Django Admin or programmatically             |
| **5. Run Beat**      | `celery -A your_project beat --loglevel=info`    |
| **6. Run Worker**    | `celery -A your_project worker --loglevel=info`  |
