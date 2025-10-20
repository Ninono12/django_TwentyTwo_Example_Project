from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        from blog.management.commands.delete_inactive_blog_post_periodic_task import \
            delete_inactive_blog_post_periodic_task
        delete_inactive_blog_post_periodic_task()