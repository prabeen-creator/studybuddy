from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from django.apps import apps

UserProfile= apps.get_model('studygroup','UserProfile')

@receiver(post_save, sender=User)
def create_seller_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save,sender= User)
def save_seller_profile(sender,instance, **kwargs):
    instance.userprofile.save()
   