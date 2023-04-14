# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.tasks import views
from apps.home.views import index

urlpatterns = [
    path('', index, name='home'),
    re_path('daily-calendar', views.daily_calendar, name='daily-calendar'),


]
