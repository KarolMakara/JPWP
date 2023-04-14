from django.contrib import admin
from apps.tasks.models import Task, UserTaskList, UserTask


# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    pass


class UserTaskAdmin(admin.ModelAdmin):
    pass


class UserTaskListTaskAdmin(admin.ModelAdmin):
    pass


admin.site.register(Task, TaskAdmin)
admin.site.register(UserTask, UserTaskAdmin)
admin.site.register(UserTaskList, UserTaskListTaskAdmin)