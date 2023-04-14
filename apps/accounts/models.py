from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import *
#from apps.tasks.models import Task, UserTaskList#, GroupTask


class MyUser(AbstractUser):
    #user_task_list = models.OneToOneField
    pass
    #group_tasks = models.ManyToManyField(GroupTask, related_name='users', blank=True)


# class MyUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = MyUser
#         fields = ('username', 'email')