from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .tasks import send_notification_email
from .models import Post

@receiver(m2m_changed, sender=Post.postCategory.through)
def notify_subscribers_on_news_publish(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add":
        post_id = instance.pk

        send_notification_email.delay(post_id)
