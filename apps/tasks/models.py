from django.db import models

# Create your models here.


from django.db import models

from JPWP import settings


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='groups_joined',
        related_query_name='group_joined',
        blank=True,
        through='GroupMembership'
    )

    def __str__(self):
        return self.name


class GroupMembership(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE
    )


class GroupTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.task.name + ' for ' + self.group.name
