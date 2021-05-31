from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, User


@receiver(post_save, sender=Post)
def notify_users_post(sender, instance, created, **kwargs):
    if created:
        subject = f'Новая статья/новость в категории {instance.category}'
    else:
        subject = f'Статья/новость {instance.title} обновлена!'

    subscribers = instance.category.subscribers.all()
    for user_id in list(instance.category.subscribers.all().values_list('id', flat=True)):
        user = User.objects.get(id=user_id)
        email = user.email
        html_content = render_to_string(
            'message_for_subscribers.html',
            {
                'text': instance.text,
                'title': instance.title,
                'category': instance.category,
                'username': user.username,
                'link': f'http://127.0.0.1:8000/news/{instance.id}',
            })
        msg = EmailMultiAlternatives(
            subject=subject,
            from_email='ithekozub@i.ua',
            to=[email],
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()


m2m_changed.connect(notify_users_post, sender=Post.category)