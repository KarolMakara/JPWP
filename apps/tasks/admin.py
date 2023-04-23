from django.contrib import admin
from apps.tasks.models import TaskList, Task, UserTaskList, UserTask, GroupTask, GroupTaskList, Notification, Category


class TaskAdmin(admin.ModelAdmin):
    #list_display = ['name', 'due_date']
    #ordering = ['due_date', 'name']
    pass


class TaskListAdmin(admin.ModelAdmin):
    pass


class UserTaskAdmin(admin.ModelAdmin):
    pass


class UserTaskListAdmin(admin.ModelAdmin):
    pass


class GroupTaskAdmin(admin.ModelAdmin):
    pass


class GroupTaskListAdmin(admin.ModelAdmin):
    pass


class NotificationAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskList, TaskListAdmin)
admin.site.register(UserTask, UserTaskAdmin)
admin.site.register(UserTaskList, UserTaskListAdmin)
admin.site.register(GroupTask, GroupTaskAdmin)
admin.site.register(GroupTaskList, GroupTaskListAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Category, CategoryAdmin)
