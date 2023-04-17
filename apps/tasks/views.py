from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from apps.tasks.forms import UserTaskForm
from apps.tasks.models import UserTaskList, UserTask, GroupTaskList, GroupTask, Task


@login_required(login_url="login/")
def default_task_view(request):
    user = request.user
    user_task_lists = get_all_user_task_lists(user)
    return render(request, 'tasks/task-list-view.html',
                  {'user_task_lists': user_task_lists,
                   'user_tasks': get_tasks(user_task_lists[0]),
                   'current_task_list_id': user_task_lists[0].id,
                   })


@login_required(login_url="login/")
def handle_fill_user_task_list(request, task_list_id):
    user = request.user
    user_task_list = get_user_task_list(user, task_list_id)
    return render(request, 'tasks/task-list-view.html',
                  {'user_task_lists': get_all_user_task_lists(user),
                   'user_tasks': get_tasks(user_task_list),
                   'current_task_list_id': user_task_list.id})


def get_all_user_task_lists(user):
    return UserTaskList.objects.filter(owner_id=user.id)


def get_tasks(task_list):
    return UserTask.objects.filter(user_task_list=task_list)


def get_user_task_list(user, task_list_id):
    return UserTaskList.objects.filter(owner_id=user.id, id=task_list_id).first()


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


def task_del(request, task_list_name, task_id):
    user_task = get_object_or_404(UserTask, id=task_id)

    if user_task.user_task_list.title != task_list_name:
        return redirect('/task-list')

    user_task.delete()
    return redirect('/task-list')


def task_list_add(request):
    form = ""
    msg = ""
    return render(request, 'tasks/task-list-add.html', {"form": form, "msg": msg})
