from django.db import models
from apps.accounts.models import MyUser
from JPWP import settings


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    due_date = models.DateField()
    to_do = models.BooleanField(default=True)
    in_progress = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class UserTaskList(models.Model):
    title = models.CharField(max_length=100, unique=True)
    owner = models.OneToOneField(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class UserTask(Task):
    user_task_list = models.ForeignKey(UserTaskList, on_delete=models.CASCADE)

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
