import asyncio
from datetime import timedelta

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.datetime_safe import date

from apps.accounts.models import MyUser, MyGroup


class Task(models.Model):
    name = models.CharField(max_length=255, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    completed_at = models.BooleanField(null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    to_do = models.BooleanField(default=True)
    in_progress = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def is_past_due(self):
        if self.due_date == "":
            return
        return timezone.now() > self.due_date

    def upcoming(self):
        if self.due_date is None or self.due_date == "":
            return
        return timezone.now() + timedelta(days=2) > self.due_date

    async def update_last_modified(self):
        # simulate some long-running task
        await asyncio.sleep(5)

        self.last_modified = timezone.now()
        self.save()


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


class Notification(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    task = models.OneToOneField(UserTask, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.message


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
