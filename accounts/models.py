from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save 
# Create your models here.

user = settings.AUTH_USER_MODEL

@receiver(pre_save, sender = user)
def user_created_handler(sender, instance, *args, **kwargs):
    print(instance.username)