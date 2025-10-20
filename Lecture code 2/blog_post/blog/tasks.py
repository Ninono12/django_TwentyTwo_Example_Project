import time

from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from django.core.mail import send_mail

from blog.models import BlogPost, BlogPostCover
from blog_post import settings


@shared_task
def send_email_task(email):
    print(f"Sending email to {email}")


@shared_task
def delete_inactive_blog_posts():
    blog_posts_count = BlogPost.objects.filter(is_active=False).count()
    BlogPost.objects.filter(is_active=False).update(deleted=True)

    send_mail(
        subject=f"Deleted blog posts",
        message=f"Deleted {blog_posts_count} blog posts",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=["mari.kifshidze@gmail.com"],
    )

    print(f"Deleted {blog_posts_count} blog posts")


@shared_task
def reorder_blog_posts(sort_field: str, asc_des: str):
    if asc_des == 'des':
        sort_field = f'-{sort_field}'
    blog_posts = BlogPost.objects.order_by(sort_field)

    for index, blog_post in enumerate(blog_posts, start=1):
        blog_post.order = index
        blog_post.save(update_fields=['order'])

    print(f"reordered {blog_posts.count()} blog posts")


@shared_task
def send_blog_post_to_email(email: str, blog_post_id: int):
    try:
        blog_post = BlogPost.objects.get(id=blog_post_id)
        send_mail(
            subject=f"{blog_post.title}",
            message=f"{blog_post.title} - {blog_post.text} - {blog_post.get_category_display()}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
        return f"Email sent to {email}"
    except BlogPost.DoesNotExist:
        return f"Blog Post with ID {blog_post_id} not found."


@shared_task
def create_blog_post_cover(image_url: str, blog_post_id: int):
    try:
        blog_post = BlogPost.objects.get(id=blog_post_id)
        BlogPostCover.objects.create(image=image_url, blog_post=blog_post)
        print(f"Blog post cover created")
    except BlogPost.DoesNotExist:
        return f"Blog Post with ID {blog_post_id} not found."


@shared_task
def send_email_about_deleted_blog_post(email: str, blog_post_title: str):
    send_mail(
        subject="Your Blog post has been deleted",
        message=f"Blog Post - {blog_post_title}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )
    return f"Email sent to {email}"


@shared_task(soft_time_limit=10, time_limit=12)
def my_task():
    try:
        print("Task started...")
        for i in range(15):
            print(f"Working... {i + 1} seconds elapsed")
            time.sleep(1)
        print("Task finished successfully!")
        return "Completed"
    except SoftTimeLimitExceeded:
        print("Task took too long and was interrupted!")
        return "Timeout"
