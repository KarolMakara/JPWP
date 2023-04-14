from django.contrib import admin
from apps.tasks.models import Task, GroupTask, Group


# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    pass


class GroupAdmin(admin.ModelAdmin):
    pass


class GroupTaskAdmin(admin.ModelAdmin):
    pass


admin.site.register(Task, TaskAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupTask, GroupTaskAdmin)