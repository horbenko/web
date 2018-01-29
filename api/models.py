from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

from tastypie.models import create_api_key


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='')
    body = models.TextField(default='')
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


# Make a tastypie API key whenever a new user is created.
models.signals.post_save.connect(create_api_key, sender=User)
