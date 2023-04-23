from datetime import time

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import *


class MyUser(AbstractUser):
    notification_before = models.IntegerField(default=0)
    daily_report_at = models.TimeField(default=time(hour=0, minute=0))


class MyGroup(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='owned_groups')
    members = models.ManyToManyField(MyUser, related_name='group_members')

    def __str__(self):
        return self.name
