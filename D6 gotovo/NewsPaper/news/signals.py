from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.urls import reverse as django_reverse

from .models import Post, Subscription


@receiver(m2m_changed, sender=Post.postCategory.through)
def notify_subscribers_on_news_publish(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add":
        post = Post.objects.get(pk=instance.pk)
        subscribers = Subscription.objects.filter(category__in=post.postCategory.all())

        for subscriber in subscribers:
            user_email = subscriber.user.email
            category_names = ', '.join(post.postCategory.values_list('name', flat=True))

            subject = f'Новая новость в вашей подписке - {category_names}'
            post_link = django_reverse('news_detail', kwargs={'pk': post.pk})
            message = f'Посетите страницу для прочтения новости в категории: {category_names}\n'
            message += f'https://127.0.0.1:8000{post_link}'

            send_mail(subject, message, 'goskazon@yandex.ru', [user_email])


