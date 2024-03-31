from django.urls import reverse as django_reverse
from .models import Subscription, Post,LastSentDate
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.utils import timezone

@shared_task
def send_notification_email(post_id):
    post = Post.objects.get(pk=post_id)
    subscribers = Subscription.objects.filter(category__in=post.postCategory.all())

    for subscriber in subscribers:
        user_email = subscriber.user.email
        category_names = ', '.join(post.postCategory.values_list('name', flat=True))

        subject = f'Новая новость в вашей подписке - {category_names}'
        post_link = django_reverse('news_detail', kwargs={'pk': post.pk})
        message = f'Посетите страницу для прочтения новости в категории: {category_names}\n'
        message += f'https://127.0.0.1:8000{post_link}'

        send_mail(subject, message, 'goskazon@yandex.ru', [user_email])



@shared_task
def send_weekly_email():
    for subscription in Subscription.objects.all():
        last_week = timezone.now() - timezone.timedelta(days=7)

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