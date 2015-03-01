from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User

class SiteUser(models.Model):
  def __str__(self):
    return self.company + " | " + self.user.username
  # Using a OneToOneField so we can add the extra 'company' parameter to the user
  # without extending or replacing Django's User model
  user = models.OneToOneField(User)
  company = models.CharField(default='', max_length=100)


class Testimonial(models.Model):
  def __str__(self):
    return self.postedby
  text = models.TextField(default='', max_length=1000)
  postedby = models.CharField(default='', max_length=1000)
  email = models.CharField(default='', max_length=100)

@receiver(post_save, sender=User)
def create_site_user_on_create(sender, instance, created, **kwargs):
  if created:
    su = SiteUser(user=instance)
    su.save()
