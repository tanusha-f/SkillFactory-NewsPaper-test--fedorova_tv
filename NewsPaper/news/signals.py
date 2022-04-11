from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers
from .models import Post


@receiver(post_save, sender=Post)
def notify_managers_appointment(sender, instance, created, **kwargs):
    if created:
        subject = instance.head
    else:
        subject = f'Post changed for {instance.head}'

    mail_managers(
        subject=subject,
        message=instance.text,
    )
