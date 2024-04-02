import logging
from django_apscheduler.jobstores import register_events
from datetime import timedelta
from django.core.management.base import BaseCommand
from django_apscheduler import util
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler.jobstores import DjangoJobStore
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from news.models import Subscription, Post, LastSentDate
from django.utils import timezone
from django.conf import settings

logger = logging.getLogger(__name__)

@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

def get_last_sent_date(subscription_id):
    last_sent_date_obj = LastSentDate.objects.filter(subscription_id=subscription_id).first()
    return last_sent_date_obj.last_sent_date if last_sent_date_obj else None

def update_last_sent_date(subscription_id, date):
    last_sent_date_obj, created = LastSentDate.objects.get_or_create(subscription_id=subscription_id)
    last_sent_date_obj.last_sent_date = date
    last_sent_date_obj.save()

def send_weekly_email():
    for subscription in Subscription.objects.all():
        last_week = timezone.now() - timedelta(days=7)

        last_sent_date = get_last_sent_date(subscription.id)

        articles = Post.objects.filter(dateCreation__gt=last_sent_date if last_sent_date else last_week,
                                       postCategory=subscription.category, categoryType='AR')
        news = Post.objects.filter(dateCreation__gt=last_sent_date if last_sent_date else last_week,
                                   postCategory=subscription.category, categoryType='NW')
        context = {
            'subscription_name': subscription.category.name,
            'subscriber_name': subscription.user.username,
            'posts': {
                'articles': articles,
                'news': news,
            },
        }

        if articles or news:
            subject = f'Еженедельный дайджест - {subscription.category.name}'
            message = render_to_string('daily_post.html', context)
            plain_message = strip_tags(message)

            try:
                send_mail(
                    subject,
                    plain_message,
                    'goskazon@yandex.ru',
                    [subscription.user.email],
                    html_message=message,
                )

                update_last_sent_date(subscription.id, timezone.now())
            except Exception as e:
                logger.error(f"Failed to send email to {subscription.user.email}. Error: {e}")
        else:
            context['no_new_posts'] = True
            subject = f'Еженедельный дайджест - {subscription.category.name}'
            message = render_to_string('no_new_posts.html', context)
            plain_message = strip_tags(message)

            try:
                send_mail(
                    subject,
                    plain_message,
                    'goskazon@yandex.ru',
                    [subscription.user.email],
                    html_message=message,
                )
            except Exception as e:
                logger.error(f"Failed to send email to {subscription.user.email}. Error: {e}")

class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_weekly_email,
            trigger=CronTrigger(
                day_of_week="fri",
                hour="18",
                minute="00",
            ),
            id="send_weekly_email",
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon",
                hour="00",
                minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )

        register_events(scheduler)

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")




