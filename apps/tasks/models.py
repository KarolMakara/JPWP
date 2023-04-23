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


class GroupTaskList(TaskList):
    for_group = models.ForeignKey(MyGroup, on_delete=models.CASCADE)


class GroupTask(Task):
    group_task_list = models.ForeignKey(GroupTaskList, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Notification(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="user_notifications")
    user_task = models.OneToOneField(UserTask, on_delete=models.CASCADE, null=True, blank=True)
    group_task = models.OneToOneField(GroupTask, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.message

