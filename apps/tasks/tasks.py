from datetime import datetime, timedelta
from celery import shared_task
from django.http.response import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone

from apps.accounts.models import MyGroup
from apps.tasks.models import *


@shared_task()
def send_upcoming_task_notifications():
    due_date_threshold = timezone.now() + timedelta(days=1)
    user_tasks_due_soon = UserTask.objects.filter(due_date__lte=due_date_threshold)
    user_tasks_missed_deadline = UserTask.objects.filter(due_date__lt=timezone.now())

    group_tasks_due_soon = GroupTask.objects.filter(due_date__lte=due_date_threshold)
    group_tasks_missed_deadline = GroupTask.objects.filter(due_date__lt=timezone.now())

    for task in user_tasks_due_soon:

        if user_tasks_missed_deadline.filter(id=task.id).exists():
            notification_message = f"USER: Missed deadline for '{task.name}'!"
        else:
            notification_message = f"USER: Task '{task.name}' is due soon!"

        existing_notification, _ = Notification.objects.update_or_create(
            user_task=task,
            defaults={'message': notification_message, 'user': task.user_task_list.owner}
        )

    group_task_lists = []
    for task in list(group_tasks_due_soon) + list(group_tasks_missed_deadline):
        group_task_lists.append(GroupTaskList.objects.filter(id=task.group_task_list.id).first())

    groups = []
    for task_list in group_task_lists:
        groups.append(MyGroup.objects.filter(id=task_list.for_group.id).first())

    users = []
    for group in groups:
        user_ids = group.members.all().values_list('id', flat=True)
        group_users = MyUser.objects.filter(id__in=user_ids)
        users.extend(group_users)

    users = list(set(users))

    for task in group_tasks_due_soon:

        for user in users:
            if group_tasks_missed_deadline.filter(id=task.id).exists():
                notification_message = f"GROUP: Missed deadline for '{task.name}'!"
            else:
                notification_message = f"GROUP: Task '{task.name}' is due soon!"

            existing_notification, _ = Notification.objects.update_or_create(
                group_task=task,
                defaults={'message': notification_message, 'user': user}
            )


# @shared_task
# def send_notification(notification_id):
#     notification = Notification.objects.get(id=notification_id, seen=False)
#     html_message = render_to_string('home/index.html', {'notification': notification})
#     #notification.seen = False
#     notification.save()
#     return HttpResponse(html_message)

# @shared_task()
# def send_notifications(user):
#     notifications = Notification.objects.filter(user=user, seen=False)
#     return HttpResponse('home/index.html', {'notifications': notifications})
#     #     html_message = render_to_string('home/index.html', {'notification': notification})
#     #     #notification.seen = False
#     #     notification.save()
#     #     return HttpResponse(html_message)