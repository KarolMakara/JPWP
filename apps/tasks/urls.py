# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from apps.tasks import views

urlpatterns = [
    path('task-list', views.default_task_view, name='tasks'),
    path('task-list/<int:task_list_id>/', views.handle_fill_user_task_list, name='tasks'),
    path('task-add/<int:task_list_id>/', views.task_add, name='task_add'),
    path('task-list-add', views.task_list_add, name='task_list_add'), #/<str:task_list_name>/
    path('task-list/<str:task_list_name>/delete/<int:task_id>/', views.task_del, name='delete_user_task'),


]
