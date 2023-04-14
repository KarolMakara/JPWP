# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from apps.tasks.models import UserTaskList, UserTask, Task



@login_required(login_url="login/")
def index(request):
    user = request.user
    user_task_list = UserTaskList.objects.filter(owner_id=user.id).first()
    user_tasks = UserTask.objects.filter(user_task_list=user_task_list)
    tasks = []
    for user_task in user_tasks:
        task = Task.objects.filter(id=user_task.id).first()
        tasks.append(task)
    return render(request, 'home/index.html', {'tasks': tasks, 'user': user})


    # user = request.user
    # user_task_list = UserTaskList.objects.filter(owner_id=user.id)
    # print(user_task_list)
    # user_task = UserTask.objects.filter(user_task_list_id=user_task_list.id)
    # tasks = Task.objects.filter(id=user_task.task_ptr_id)
    # return render(request, 'home/index.html', {'tasks': tasks, 'user': user})
    # context = {'segment': 'index'}
    #
    # html_template = loader.get_template('home/index.html')
    # return HttpResponse(html_template.render(context, request))


@login_required(login_url="login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        print(request.path)
        load_template = request.path.split('/')[1]
        print(load_template)
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

