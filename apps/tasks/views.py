from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F

from apps.tasks.forms import UserTaskForm
from apps.tasks.models import UserTaskList, UserTask, GroupTaskList, GroupTask, Task


@login_required(login_url="login/")
def default_task_view(request):
    user = request.user
    user_task_lists = get_all_user_task_lists(user)
    return render(request, 'tasks/task-list-view.html',
                  {'user_task_lists': user_task_lists,
                   'user_tasks': get_tasks_from_list(user_task_lists[0]),
                   'current_task_list_id': user_task_lists[0].id,
                   })


@login_required(login_url="login/")
def handle_fill_user_task_list(request, task_list_id):
    user = request.user
    user_task_list = get_user_task_list(user, task_list_id)
    return render(request, 'tasks/task-list-view.html',
                  {'user_task_lists': get_all_user_task_lists(user),
                   'user_tasks': get_tasks_from_list(user_task_list),
                   'current_task_list_id': user_task_list.id})


def get_user_task_list(user, task_list_id):
    return UserTaskList.objects.filter(owner_id=user.id, id=task_list_id).first()


def get_all_user_task_lists(user):
    return UserTaskList.objects.filter(owner_id=user.id)


def get_tasks_from_list(task_list):
    user_tasks = UserTask.objects.filter(user_task_list=task_list)
    tasks = [task for task in user_tasks]
    tasks = sorted(tasks, key=lambda x: (x.due_date is None, x.due_date))
    for task in tasks:
        if task.due_date is None:
            task.due_date = ''

    return tasks


@login_required(login_url="login/")
def task_add(request, task_list_id):
    task_list_id = int(task_list_id)
    task_list_name = UserTaskList.objects.filter(owner_id=request.user.id, id=task_list_id).first()
    if request.method == 'POST':
        form = UserTaskForm(request.POST)
        if form.is_valid():
            user_task_list = UserTaskList.objects.get(id=task_list_id)
            user_task = UserTask(name=form.cleaned_data['name'],
                                 description=form.cleaned_data['description'],
                                 due_date=form.cleaned_data['due_date'],
                                 to_do=True, user_task_list=user_task_list)
            user_task.save()
            return redirect('/task-list')

    return render(request, 'tasks/task-add.html', {'form': UserTaskForm(), 'task_list_name': task_list_name})


@login_required(login_url="login/")
def task_del(request, task_list_name, task_id):
    user_task = get_object_or_404(UserTask, id=task_id)

    if user_task.user_task_list.name != task_list_name:
        return redirect('/task-list')

    user_task.delete()
    return redirect('/task-list')


@login_required(login_url="login/")
def task_list_add(request):
    form = ""
    msg = ""
    return render(request, 'tasks/task-list-add.html', {"form": form, "msg": msg})


@login_required(login_url="login/")
def tasks_to_do(request):
    user = request.user
    user_task_lists = get_all_user_task_lists(user)
    return render(request, 'tasks/tasks-to-do.html',
                  {'user_tasks': get_user_task_attributes_sort(user, user_task_lists, {'to_do': True}, 'due_date')})


@login_required(login_url="login/")
def tasks_in_progress(request):
    user = request.user
    user_task_lists = get_all_user_task_lists(user)
    return render(request, 'tasks/tasks-in-progress.html',
                  {'user_tasks': get_user_task_attributes_sort(user, user_task_lists, {'in_progress': True}, 'due_date')})


def get_user_task_attributes_sort(user, task_lists, attributes, sort_option):
    tasks = get_all_user_tasks_attributes(user, task_lists, attributes=attributes)
    return sort_and_update_tasks(tasks, sort_option)


def get_all_user_tasks_attributes(user, task_lists, attributes):
    tasks = []
    for task_list in task_lists:
        user_task_list = UserTask.objects.filter(user_task_list=task_list, **attributes)
        for user_task in user_task_list:
            tasks.append(user_task)
    return tasks


def sort_and_update_tasks(tasks, attribute):
    sorted_tasks = sorted(tasks, key=lambda x: (getattr(x, attribute) is None, getattr(x, attribute)))
    for task in sorted_tasks:
        if getattr(task, attribute) is None:
            setattr(task, attribute, '')
    return sorted_tasks


@login_required(login_url="login/")
def tasks_completed(request):
    user = request.user
    user_task_lists = get_all_user_task_lists(user)
    return render(request, 'tasks/tasks-completed.html',
                  {'user_tasks': get_user_task_attributes_sort(user, user_task_lists, {'completed': True}, 'completed_at')})


def daily_view(request):
    return render(request, 'tasks/daily-view.html')


def weekly_view(request):
    return render(request, 'tasks/weekly-view.html')


def monthly_view(request):
    return render(request, 'tasks/monthly-view.html')
