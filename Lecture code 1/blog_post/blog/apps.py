from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'


    def ready(self):
        from blog.management.commands.delete_blog_post_periodic_task import create_periodic_task
        create_periodic_task()
