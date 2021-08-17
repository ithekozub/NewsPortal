from celery import shared_task
from datetime import timezone, datetime, timedelta
from .models import Category, Post, User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import post_save


@shared_task
def mail_new_post(pid):
    post = Post.objects.get(pk=pid)
    subscribers = list(post.category.subscribers.all().values_list('id', flat=True))
    subject = f'Новая статья/новость в категории {post.category}'
    for user_id in subscribers:
        user = User.objects.get(id=user_id)
        email = user.email
        html_content = render_to_string(
            'message_for_subscribers.html',
            {
                'text': post.text,
                'title': post.title,
                'category': post.category,
                'username': user.username,
                'link': f'http://127.0.0.1:8000/news/{post.id}',
            })
        msg = EmailMultiAlternatives(
            subject=subject,
            from_email='ithekozub@i.ua',
            to=[email],
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()


@shared_task
def weekly_posts():
    timer = datetime.now(timezone.utc)
    user_posts = {}
    for cat in Category.objects.all():
        for subscriber in cat.subscribers.all():
            my_post = Post.objects.filter(category_id=cat.id, post_time__gte=(timer - timedelta(days=7)))
            posts = list(my_post)
            if posts:
                user_posts[subscriber] = user_posts.get(subscriber, []) + [posts]

    for user, art in user_posts.items():
        html_content = render_to_string(
            'weekly_posts.html',
            {
                'user': user,
                'art': art,
            }
        )
        msg = EmailMultiAlternatives(
            subject='Посты за неделю',
            from_email='ithekozub@i.ua',
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


