from django.contrib import admin
from apps.tasks.models import UserTaskList, UserTask, GroupTask, GroupTaskList


class UserTaskAdmin(admin.ModelAdmin):
    pass


class UserTaskListAdmin(admin.ModelAdmin):
    pass


class GroupTaskAdmin(admin.ModelAdmin):
    pass


class GroupTaskListAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserTask, UserTaskAdmin)
admin.site.register(UserTaskList, UserTaskListAdmin)
admin.site.register(GroupTask, GroupTaskAdmin)
admin.site.register(GroupTaskList, GroupTaskListAdmin)
