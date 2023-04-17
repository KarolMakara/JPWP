from django.db import models
from django.urls import reverse
from django.utils import timezone

from apps.accounts.models import MyUser, MyGroup
from JPWP import settings


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    completed_at = models.BooleanField(null=True)
    due_date = models.DateField(blank=True, null=True)
    to_do = models.BooleanField(default=True)
    in_progress = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class TaskList(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class UserTaskList(TaskList):
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE)


class UserTask(Task):
    user_task_list = models.ForeignKey(UserTaskList, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class GroupTaskList(TaskList):
    for_group = models.OneToOneField(MyGroup, on_delete=models.CASCADE)


class GroupTask(Task):
    group_task_list = models.ForeignKey(GroupTaskList, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# class Group(models.Model):
#     name = models.CharField(max_length=50)
#     users = models.ManyToManyField(
#         settings.AUTH_USER_MODEL,
#         related_name='groups_joined',
#         related_query_name='group_joined',
#         blank=True,
#         through='GroupMembership'
#     )
#
#     def __str__(self):
#         return self.name
#
#
# class GroupMembership(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE
#     )
#     group = models.ForeignKey(
#         Group,
#         on_delete=models.CASCADE
#     )
#
#
# class GroupTask(models.Model):
#     task = models.ForeignKey(Task, on_delete=models.CASCADE)
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.task.name + ' for ' + self.group.name
