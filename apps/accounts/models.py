from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import *


# from apps.tasks.models import Task, UserTaskList#, GroupTask


class MyUser(AbstractUser):
    user_groups = models.ManyToManyField('MyGroup', related_name='users', blank=True)
    pass
    # group_tasks = models.ManyToManyField(GroupTask, related_name='users', blank=True)


class MyGroup(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='owned_groups')
    members = models.ManyToManyField(MyUser, related_name='group_members')

    def __str__(self):
        return self.name
# class MyUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = MyUser
#         fields = ('username', 'email')
