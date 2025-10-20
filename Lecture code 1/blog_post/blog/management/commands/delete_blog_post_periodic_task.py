from datetime import timedelta

from django.utils import timezone
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

def create_periodic_task():
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.DAYS,
    )

    start_time = timezone.now().replace(hour=16, minute=30, second=0, microsecond=0)
    if start_time < timezone.now():
        start_time += timedelta(days=1)  # schedule for tomorrow if 3 AM already passed

    PeriodicTask.objects.update_or_create(
        name='Delete Inactive Blog Post',
        defaults={
            'interval': schedule,
            'task': 'blog.tasks.delete_blog_post',
            'start_time': start_time,
            'args': json.dumps([]),
        }
    )
