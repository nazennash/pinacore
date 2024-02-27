from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User


@receiver(post_save, sender=User.phone_number)
def post_save_generate_otp(sender, instance, created, *args, **kwargs):
    if created:
        User.objects.create(user=instance)