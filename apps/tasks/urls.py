# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from apps.tasks import views, notifications

urlpatterns = [
    path('task-list', views.default_task_view, name='tasks'),
    path('task-list/<int:task_list_id>', views.handle_fill_user_task_list, name='tasks'),
    path('task-add/<int:task_list_id>/<str:task_status>', views.task_add, name='task_add'),
    path('task-list-add', views.task_list_add, name='task_list_add'),
    path('task-list/<int:user_task_list_id>/edit/<int:user_task_id>/<str:task_status>', views.task_edit, name='task_edit'),
    path('task-list/<int:user_task_list_id>/delete/<int:user_task_id>/<str:task_status>', views.task_del, name='task_delete'),
    path('tasks-to-do', views.tasks_to_do, name='tasks_to_do'),
    path('tasks-in-progress', views.tasks_in_progress, name='tasks_in_progress'),
    path('tasks-completed', views.tasks_completed, name='tasks_completed'),
    path('daily-view', views.daily_view, name='daily_view'),
    path('weekly-view', views.weekly_view, name='weekly_view'),
    path('monthly-view', views.monthly_view, name='monthly_view'),
    path('notifications/send/<int:notification_id>/', views.notification_view, name='notification_view'),
]
