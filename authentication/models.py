import os
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    email = models.TextField(default="r@r.rr")
    preferences = models.TextField(default="")
    image = models.FileField(upload_to='profiles/full/', null=True)
    image_thumb = models.FileField(upload_to='profiles/thumbs/', null=True)


@receiver(models.signals.post_delete, sender=UserProfile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
            os.remove(instance.image_thumb.path)


@receiver(models.signals.pre_save, sender=UserProfile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = UserProfile.objects.get(pk=instance.pk).image
        old_file_thumb = UserProfile.objects.get(pk=instance.pk).image_thumb
    except UserProfile.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        try:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
                os.remove(old_file_thumb.path)
        except Exception:
            return False