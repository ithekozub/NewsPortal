import logging
from datetime import timezone

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from datetime import timedelta, datetime
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from news.models import Post, Category, Author

logger = logging.getLogger(__name__)

# наша задача по выводу текста на экран
def my_job():
    # timer = datetime.now(timezone.utc)
    #
    # user_posts = {
    # }
    #
    # for cat in Category.objects.all():
    #     for subscriber in cat.subscribers.all():
    #         my_post = Post.objects.filter(category_id=cat.id, post_time__gte=(timer - timedelta(days=7)))
    #         posts = list(my_post)
    #         if posts:
    #             user_posts[subscriber] = user_posts.get(subscriber, []) + [posts]
    #
    # for user, art in user_posts.items():
    #     html_content = render_to_string(
    #         'weekly_posts.html',
    #         {
    #             'user': user,
    #             'art': art,
    #         }
    #     )
    #     msg = EmailMultiAlternatives(
    #         subject='Посты за неделю',
    #         from_email='ithekozub@i.ua',
    #         to=[user.email],
    #     )
    #     msg.attach_alternative(html_content, "text/html")
    #     msg.send()


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="sun", hour="23", minute="55"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")