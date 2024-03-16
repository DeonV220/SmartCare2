from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OwnerProfile

# creates a new user
@receiver(post_save,sender=User)
def create_owner_profile(sender, instance, created, **kwargs):
    if created:
        OwnerProfile.objects.create(user=instance, name=instance.username)


# saving the user profile
# @receiver(post_save,sender=User)
# def save_owner_profile(sender, instance, **kwargs):
#     instance.OwnerProfile.save()