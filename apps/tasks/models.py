import asyncio
from datetime import timedelta

from django.db import models
from django.utils import timezone

from apps.accounts.models import MyUser, MyGroup


class Category(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=255, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(blank=True, null=True)
    to_do = models.BooleanField(default=True)
    in_progress = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def set_to_do(self):
        self.to_do = True
        self.in_progress = False
        self.completed = False
        return self

    def set_in_progress(self):
        self.to_do = False
        self.in_progress = True
        self.completed = False
        return self

    def set_completed(self):
        self.to_do = False
        self.in_progress = False
        self.completed = True
        return self

    def __str__(self):
        if self.name:
            return self.name
        else:
            return ""

    def is_past_due(self):
        if self.due_date == "":
            return
        return timezone.now() > self.due_date and not self.completed

    def upcoming(self):
        if self.due_date is None or self.due_date == "":
            return
        return timezone.now() + timedelta(days=2) > self.due_date and not self.completed

    def is_completed(self):
        return self.completed

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

    def get_instance(self):
        return type(self).__name__

    def __str__(self):
        return self.name


class GroupTaskList(TaskList):
    for_group = models.ForeignKey(MyGroup, on_delete=models.CASCADE)


class GroupTask(Task):
    group_task_list = models.ForeignKey(GroupTaskList, on_delete=models.CASCADE)

    def get_instance(self):
        return type(self).__name__

    def __str__(self):
        return self.name


class Notification(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="user_notifications")
    user_task = models.OneToOneField(UserTask, on_delete=models.CASCADE, null=True, blank=True)
    group_task = models.ForeignKey(GroupTask, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    def has_user_task(self):
        return isinstance(self.user_task, UserTask)

    def has_group_task(self):
        return isinstance(self.group_task, GroupTask)