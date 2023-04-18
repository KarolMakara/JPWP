# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import json
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from apps.tasks.models import UserTaskList, UserTask, Task, GroupTaskList, GroupTask
from apps.tasks.views import last_modified_at_for_task_status


@login_required(login_url="login/")
def index(request):
    last_modified_at = last_modified_at_for_task_status(request)
    return render(request, 'home/index.html', {'last_modified_to_do': last_modified_at[0],
                                               'last_modified_in_progress': last_modified_at[1],
                                               'last_modified_completed': last_modified_at[2]})


@login_required(login_url="login/")
def pages(request):
    context = {}
    try:
        load_template = request.path.split('/')[1]
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
