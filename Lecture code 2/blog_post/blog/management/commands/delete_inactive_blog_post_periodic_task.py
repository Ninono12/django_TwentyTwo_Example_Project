from datetime import datetime, time

from django.utils import timezone
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

def delete_inactive_blog_post_periodic_task():
    # 1. Define schedule (every 1 day)
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.MINUTES,
    )

    # 2. Create the task entry if it doesn’t already exist
    now = timezone.now()
    start_time = timezone.make_aware(datetime.combine(now.date(), time(16, 20)))

    PeriodicTask.objects.update_or_create(
        name='Delete inactive blog post periodic task',
        defaults={
            'interval': schedule,
            'task': 'blog.tasks.delete_inactive_blog_posts',
            'args': json.dumps([]),
            'start_time': start_time,
        }
    )
