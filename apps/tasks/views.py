from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from django.utils import timezone
from datetime import datetime, timedelta
from datetime import date
from calendar import monthrange

from apps.accounts.models import MyGroup, MyUser
from apps.tasks.forms import UserTaskForm
from apps.tasks.models import UserTaskList, UserTask, GroupTaskList, GroupTask, Notification


def last_modified_at_for_task_status(request):
    user = request.user
    task_lists = UserTaskList.objects.filter(owner=user.id)
    to_do_tasks = []
    in_progress_tasks = []
    completed_tasks = []
    for task_list in task_lists:
        to_do_tasks.extend(get_tasks_from_query_set(UserTask.objects.filter(user_task_list=task_list, to_do=True)))
        in_progress_tasks.extend(
            get_tasks_from_query_set(UserTask.objects.filter(user_task_list=task_list, in_progress=True)))
        completed_tasks.extend(
            get_tasks_from_query_set(UserTask.objects.filter(user_task_list=task_list, completed=True)))
    to_do_tasks = sort_and_update_tasks(to_do_tasks, 'modified_at', True)
    in_progress_tasks = sort_and_update_tasks(in_progress_tasks, 'modified_at', True)
    completed_tasks = sort_and_update_tasks(completed_tasks, 'modified_at', True)

    if len(to_do_tasks) > 0 and len(in_progress_tasks) > 0 and len(completed_tasks) > 0:
        return to_do_tasks[0].modified_at, in_progress_tasks[0].modified_at, completed_tasks[0].modified_at
    else:
        return 0, 0, 0


def get_tasks_from_query_set(tasks):
    return [task for task in tasks]


@login_required(login_url="login/")
def default_task_view(request):
    user = request.user
    user_task_lists = get_all_user_task_lists(user)

    if user_task_lists:
        return render(request, 'tasks/task-list-view.html',
                      {'user_task_lists': user_task_lists,
                       'user_tasks': get_tasks_from_list(user_task_lists[0]),
                       'current_task_list_id': user_task_lists[0].id,
                       })
    else:
        return render(request, 'tasks/task-list-view.html',
                      {'user_task_lists': user_task_lists,
                       'user_tasks': [],
                       'current_task_list_id': 0,
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
    if task_list is None:
        return []

    if isinstance(task_list, GroupTaskList):
        tasks = GroupTask.objects.filter(group_task_list=task_list)
    elif isinstance(task_list, UserTaskList):
        tasks = UserTask.objects.filter(user_task_list=task_list)
    else:
        raise ValueError("Invalid task list type")

    tasks = [task for task in tasks]
    tasks = sorted(tasks, key=lambda x: (x.due_date is None, x.due_date))
    for task in tasks:
        if task.due_date is None:
            task.due_date = ''

    return tasks


@login_required(login_url="login/")
def task_add(request, task_list_id, task_status):
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
            if task_status != 'lists':
                return redirect('/' + task_status)
            else:
                return redirect('/task-list/' + str(task_list_id))

    return render(request, 'tasks/task-add.html', {'form': UserTaskForm(), 'task_list_name': task_list_name})


@login_required(login_url="login/")
def task_edit(request, user_task_list_id, user_task_id, task_status):
    task_list = get_object_or_404(UserTaskList, id=user_task_list_id)
    task = get_object_or_404(UserTask, id=user_task_id, user_task_list=task_list)
    if request.method == 'POST':
        form = UserTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            if task_status != 'lists':
                return redirect('/' + task_status)
            else:
                return redirect('/task-list/' + str(task.user_task_list.id))
    else:
        form = UserTaskForm(instance=task)

    return render(request, 'tasks/task-edit.html', {'form': form, 'task': task, 'user_task_list_name': task_list.name})


@login_required(login_url="login/")
def task_del(request, user_task_list_id, user_task_id, task_status):
    task_list = UserTaskList.objects.filter(id=user_task_list_id).first()
    task = UserTask.objects.filter(id=user_task_id, user_task_list=task_list).first()

    if task and task_list:
        task.delete()

    notification = Notification.objects.filter(task=task).first()
    if notification:
        notification.delete()

    if task_status != 'lists':
        return redirect('/' + task_status)
    else:
        return redirect('/task-list/' + str(task.user_task_list.id))


@login_required(login_url="login/")
def task_list_add(request):
    form = ""
    msg = ""
    return render(request, 'tasks/task-list-add.html', {"form": form, "msg": msg})


@login_required(login_url="login/")
def tasks_to_do(request):
    user = request.user
    user_task_lists = get_all_user_task_lists(user)
    group_task_lists = get_all_group_task_lists(user)
    return render(request, 'tasks/tasks-to-do.html',
                  {'user_tasks': get_task_attributes_sort(user, user_task_lists, group_task_lists,
                                                          {'to_do': True},
                                                          'due_date')})


@login_required(login_url="login/")
def tasks_in_progress(request):
    user = request.user
    user_task_lists = get_all_user_task_lists(user)
    group_task_lists = get_all_group_task_lists(user)
    return render(request, 'tasks/tasks-in-progress.html',
                  {'user_tasks': get_task_attributes_sort(user, user_task_lists, group_task_lists,
                                                          {'in_progress': True},
                                                          'due_date')})


@login_required(login_url="login/")
def tasks_completed(request):
    user = request.user
    user_task_lists = get_all_user_task_lists(user)
    group_task_lists = get_all_group_task_lists(user)
    return render(request, 'tasks/tasks-completed.html',
                  {'user_tasks': get_task_attributes_sort(user, user_task_lists, group_task_lists, {'completed': True},
                                                          'completed_at')})


def get_all_group_task_lists(user):
    groups = MyGroup.objects.filter(members=user)
    group_task_lists = []
    for group in groups:
        group_task_lists.append(GroupTaskList.objects.filter(for_group=group))

    group_task_lists = [gtl for qs in group_task_lists for gtl in qs]

    return group_task_lists


def get_task_attributes_sort(user, user_task_lists, group_task_lists, attributes, sort_option):
    tasks = get_all_tasks_attributes(user, user_task_lists, group_task_lists, attributes=attributes)
    return sort_and_update_tasks(tasks, sort_option)


def get_all_tasks_attributes(user, user_task_lists, group_task_lists, attributes):
    tasks = []
    for task_list in user_task_lists:
        user_task_list = UserTask.objects.filter(user_task_list=task_list, **attributes)
        for user_task in user_task_list:
            tasks.append(user_task)

    for task_list in group_task_lists:
        group_task_list = GroupTask.objects.filter(group_task_list=task_list, **attributes)
        for user_task in group_task_list:
            tasks.append(user_task)

    return tasks


def sort_and_update_tasks(tasks, attribute, rev=False):
    sorted_tasks = sorted(tasks, key=lambda x: (getattr(x, attribute) is None, getattr(x, attribute)), reverse=rev)
    for task in sorted_tasks:
        if getattr(task, attribute) is None:
            setattr(task, attribute, '')
    return sorted_tasks


def notification_mark_as_seen(request, notification_id):
    notification = Notification.objects.get(id=notification_id, seen=False)
    notification.seen = True
    notification.save()

    task = notification.task
    task_list = task.user_task_list

    return render(request, 'tasks/task-show.html',
                  {'notification': notification, 'task': task, 'user_task_list_name': task_list.name,
                   'message': 'TEST'})


@csrf_exempt
@login_required(login_url="login/")
def get_notifications_data(request):
    user_notifications = Notification.objects.filter(user=request.user, seen=False).values('message', 'id')
    notifications = []
    notifications.extend(list(user_notifications))
    notification_length = len(notifications)
    if notification_length > 0:
        notifications[0]['count'] = notification_length
    # print(notifications)
    # ser = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    # task = models.OneToOneField(UserTask, on_delete=models.CASCADE, null=True)
    # message = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)
    # seen = models.BooleanField(default=False)
    return JsonResponse({'notifications': notifications})


@login_required(login_url="login/")
def task_show(request, user_task_list_id, user_task_id):
    task_list = UserTaskList.objects.get(id=user_task_list_id)
    task = UserTask.objects.get(id=user_task_id, user_task_list=task_list)

    return render(request, 'tasks/task-show.html', {'task': task, 'user_task_list_name': task_list.name})


@login_required(login_url="login/")
def default_group_view(request):
    user = request.user
    groups = MyGroup.objects.filter(members=user)
    lists = GroupTaskList.objects.filter(for_group=groups.first())
    tasks = get_tasks_from_list(lists.first())

    if lists and groups:
        return render(request, 'tasks/groups.html', {'groups': groups,
                                                     'lists': lists,
                                                     'tasks': tasks,
                                                     'current_list': lists[0],
                                                     'current_group': groups[0],
                                                     'user': user})
    else:
        return render(request, 'tasks/groups.html', {'groups': groups,
                                                     'lists': lists,
                                                     'tasks': tasks,
                                                     'current_list': [],
                                                     'current_group': [],
                                                     'user': user})


@login_required(login_url="login/")
def handle_fill_group_task_list(request, group_id, group_list_id):
    user = request.user
    groups = MyGroup.objects.filter(members=user)

    current_group = MyGroup.objects.get(members=user, id=group_id)

    lists = GroupTaskList.objects.filter(for_group=current_group)

    if group_list_id == 0:
        current_list = []
        tasks = []
    else:
        current_list = GroupTaskList.objects.filter(for_group=current_group, id=group_list_id).first()
        tasks = get_tasks_from_list(current_list)

    print(current_list)

    return render(request, 'tasks/groups.html', {'groups': groups,
                                                 'lists': lists,
                                                 'tasks': tasks,
                                                 'current_group': current_group,
                                                 'current_list': current_list,
                                                 'user': user})


@login_required(login_url="login/")
def daily_view(request):
    user = request.user
    user_task_lists = get_all_user_task_lists(user)
    tasks_due = []
    tasks_no_due = []
    current_date = request.GET.get('date')
    if current_date:
        try:
            current_date = timezone.datetime.strptime(current_date, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Nieprawidłowy format daty.'})
    else:
        current_date = timezone.now().date()
    for task_list in user_task_lists:
        user_tasks = get_tasks_from_list(task_list)
        for task in user_tasks:
            if not isinstance(task.due_date, date):
                tasks_no_due.append(task)
                continue
            if not task.due_date or task.due_date.date() <= current_date:
                tasks_due.append(task)
            elif task.due_date.date() == current_date:
                tasks_due.append(task)
    tasks_due.sort(key=lambda x: x.due_date)
    if user_task_lists is not None:
        current = user_task_lists[0].id
    else:
        current = None
    return render(request, 'tasks/daily-view.html',
                  {'user_task_lists': user_task_lists,
                   'user_tasks': tasks_due + tasks_no_due,
                   'current_task_list_id': current,
                   'current_date': current_date})


@login_required(login_url="login/")
def weekly_view(request):
    user = request.user
    user_task_lists = get_all_user_task_lists(user)
    tasks_current_week = []
    tasks_past_week = []
    tasks_no_due = []
    current_date = request.GET.get('date')
    if current_date:
        try:
            current_date = timezone.datetime.strptime(current_date, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Nieprawidłowy format daty.'})
    else:
        current_date = timezone.now().date()
    current_week_start = current_date - timedelta(days=current_date.weekday())
    current_week_end = current_week_start + timedelta(days=6)
    for task_list in user_task_lists:
        user_tasks = get_tasks_from_list(task_list)
        for task in user_tasks:
            if not isinstance(task.due_date, date):
                tasks_no_due.append(task)
                continue
            if task.due_date.date() <= current_week_start:
                tasks_past_week.append(task)
            elif current_week_start <= task.due_date.date() <= current_week_end:
                tasks_current_week.append(task)
    tasks_current_week.sort(key=lambda x: x.due_date)
    tasks_past_week.sort(key=lambda x: x.due_date)

    if user_task_lists is not None:
        current = user_task_lists[0].id
    else:
        current = None

    return render(request, 'tasks/weekly-view.html',
                  {'user_task_lists': user_task_lists,
                   'user_tasks_current_week': tasks_current_week,
                   'user_tasks_past_week': tasks_past_week,
                   'user_tasks': tasks_no_due,
                   'current_task_list_id': current,
                   'current_week_start': current_week_start,
                   'current_week_end': current_week_end})


@login_required(login_url="login/")
def monthly_view(request):
    user = request.user
    user_task_lists = get_all_user_task_lists(user)
    tasks_current_month = []
    tasks_past_month = []
    tasks_no_due = []
    current_date = request.GET.get('date')
    if current_date:
        try:
            current_date = timezone.datetime.strptime(current_date, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Nieprawidłowy format daty.'})
    else:
        current_date = timezone.now().date()
    current_week_start = current_date - timedelta(days=current_date.weekday())
    current_week_end = current_week_start + timedelta(days=6)
    current_month_start = timezone.datetime(current_date.year, current_date.month, 1, 0, 0, 0)
    _, last_day = monthrange(current_month_start.year, current_month_start.month)
    current_month_end = timezone.datetime(current_month_start.year, current_month_start.month, last_day, 0, 0, 0)
    for task_list in user_task_lists:
        user_tasks = get_tasks_from_list(task_list)
        for task in user_tasks:
            if not isinstance(task.due_date, date):
                tasks_no_due.append(task)
                continue
            if current_month_start.date() <= task.due_date.date() <= current_month_end.date():
                tasks_current_month.append(task)
            elif task.due_date.date() < current_month_start.date():
                tasks_past_month.append(task)
    tasks_current_month.sort(key=lambda x: x.due_date)
    tasks_past_month.sort(key=lambda x: x.due_date)

    if user_task_lists is not None:
        current = user_task_lists[0].id
    else:
        current = None

    return render(request, 'tasks/monthly-view.html',
                  {'user_task_lists': user_task_lists,
                   'user_tasks_month': tasks_current_month,
                   'user_tasks_past': tasks_past_month,
                   'user_tasks': tasks_no_due,
                   'current_task_list_id': current,
                   'current_month_start': current_month_start})


def start_task(request, user_task_list_id, user_task_id):
    task_list = UserTaskList.objects.get(id=user_task_list_id)
    task = UserTask.objects.get(id=user_task_id, user_task_list=task_list)
    task.set_in_progress()
    task.save()

    return redirect('/tasks-to-do')


def test(request):
    pass


#     # due_date_threshold = timezone.now() + timedelta(days=1)
#     # group_tasks_due_soon = GroupTask.objects.filter(due_date__lte=due_date_threshold)
#     # group_tasks_missed_deadline = GroupTask.objects.filter(due_date__lt=timezone.now())
#     due_date_threshold = timezone.now() + timedelta(days=1)
#     groups = MyGroup.objects.all()
#     for group in groups:
#         members = group.members.all()
#         for g in GroupTaskList.objects.filter(for_group=group):
#             due_date_tasks = GroupTask.objects.filter(group_task_list=g, due_date__lte=due_date_threshold)
#
#             missed_tasks = GroupTask.objects.filter(group_task_list=g, due_date__lt=timezone.now())
#             for task in due_date_tasks:
#                 for member in members:
#                     if missed_tasks.filter(id=task.id).exists():
#                         notification_message = f"GROUP: Missed deadline for '{task.name}'!"
#                     else:
#                         notification_message = f"GROUP: Task '{task.name}' is due soon!"
#                     print(task, ' : ', member)
#
#     return render(request, 'tasks/test.html')


# if group_tasks_missed_deadline.filter(id=task.id).exists():
#     notification_message = f"GROUP: Missed deadline for '{task.name}'!"
# else:
#     notification_message = f"GROUP: Task '{task.name}' is due soon!"
#
# existing_notification, _ = Notification.objects.update_or_create(
#     group_task=task,
#     defaults={'message': notification_message, 'user': user}
# )
def end_task(request, user_task_list_id, user_task_id):
    task_list = UserTaskList.objects.get(id=user_task_list_id)
    task = UserTask.objects.get(id=user_task_id, user_task_list=task_list)
    task.set_completed()
    task.completed_at = timezone.now()
    task.save()

    return redirect('/tasks-in-progress')
