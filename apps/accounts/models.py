from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import *
from apps.tasks.models import *


class User(AbstractUser):
    tasks = models.ForeignKey()