# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path

from apps import accounts
from apps.tasks import views, notifications

urlpatterns = [
    path('task-list', views.default_task_view, name='tasks'),
    path('task-list/<int:task_list_id>', views.handle_fill_user_task_list, name='tasks'),
    path('task-add/<int:task_list_id>/<str:task_status>/<str:task_type>', views.task_add, name='task_add'),
    path('task-list-del/<int:task_list_id>/<str:task_type>', views.task_list_delete, name='task_list_del'),
    path('task-list-add/<str:task_status>/<str:task_type>/<int:group_id>', views.task_list_add, name='task_list_add'),
    path('task-list-edit//<str:task_type>/<int:task_list_id>', views.task_list_edit, name='task_list_edit'),
    path('task/<int:task_list_id>/edit/<int:task_id>/<str:task_status>/<str:task_type>', views.task_edit, name='task_edit'),
    path('task/<int:task_list_id>/delete/<int:task_id>/<str:task_status>/<str:task_type>', views.task_del, name='task_delete'),
    path('task/<int:task_list_id>/show/<int:task_id>/<str:task_type>', views.task_show, name='task_show'),
    path('tasks-to-do', views.tasks_to_do, name='tasks_to_do'),
    path('tasks-in-progress', views.tasks_in_progress, name='tasks_in_progress'),
    path('tasks-completed', views.tasks_completed, name='tasks_completed'),
    path('daily-view', views.daily_view, name='daily_view'),
    path('weekly-view', views.weekly_view, name='weekly_view'),
    path('monthly-view', views.monthly_view, name='monthly_view'),
    path('notifications/mark-as-seen/<int:notification_id>', views.notification_mark_as_seen, name='notification_mark_as_seen'),
    path('notifications-data', views.get_notifications_data, name='notifications_data'),
    path('groups', views.default_group_view, name='default_groups'),
    path('groups/<int:group_id>', views.handle_fill_group, name='groups'),
    path('groups/<int:group_id>/<int:group_list_id>', views.handle_fill_group_task_list, name='groups_and_lists'),
    path('start-task/<int:task_list_id>/<int:task_id>/<str:task_type>', views.start_task, name='start_task'),
    path('end-task/<int:task_list_id>/<int:task_id>/<str:task_type>/<str:view>', views.end_task, name='end_task'),
    path('test', views.test, name='test'),
    path('create-group', views.create_group, name='create_group'),
    path('edit-group/<int:group_id>', views.edit_group, name='edit_group'),
    path('delete-group/<int:group_id>', views.delete_group, name='delete_group'),
]
