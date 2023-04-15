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


def get_tasks(obj_tasks):
    tasks = []
    for obj_task in obj_tasks:
        task = Task.objects.filter(id=obj_task.id).first()
        tasks.append(task)
    return tasks


def get_user_tasks(user):
    query_user_task_lists = UserTaskList.objects.filter(owner_id=user.id).all()
    user_task_lists = []

    for qutl in query_user_task_lists:
        user_task_list = UserTask.objects.filter(user_task_list=qutl)
        user_task_lists.append(qutl)
        user_task_lists.append(get_tasks(user_task_list))

    # user_task_lists_and_names = []
    # for i in range(len(user_tasks)):
    #     user_task_lists_and_names.append((user_tasks_names[i], user_tasks[i]))

    return user_task_lists


def get_group_tasks(user):
    group_task_list = GroupTaskList.objects.filter(for_group=user.id).first()
    group_tasks = GroupTask.objects.filter(group_task_list=group_task_list)
    return get_tasks(group_tasks)


@login_required(login_url="login/")
def index(request):
    user = request.user
    user_task_lists_and_names = get_user_tasks(user)
    group_tasks = get_group_tasks(user)
    print(user_task_lists_and_names)
    return render(request, 'home/index.html', {'group_tasks': group_tasks, 'user_task_lists': user_task_lists_and_names[1],
                                               'user_task_names': user_task_lists_and_names[0], 'user': user})

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
