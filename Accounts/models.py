from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import *


class MyUser(AbstractUser):
    email = CharField(unique=False)
    pass
