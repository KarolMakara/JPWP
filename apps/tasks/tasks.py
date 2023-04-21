from datetime import datetime, timedelta
from celery import shared_task
from django.http.response import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone

from apps.tasks.models import UserTask, Notification, MyUser


@shared_task()
def send_upcoming_task_notifications():
    due_date_threshold = timezone.now() + timedelta(days=1)
    tasks_due_soon = UserTask.objects.filter(due_date__lte=due_date_threshold)
    for task in tasks_due_soon:
        notification_message = f"Task '{task.name}' is due soon!"
        existing_notification = Notification.objects.filter(task=task, seen=False).first()
        if not existing_notification:
            Notification.objects.create(message=notification_message, user=task.user_task_list.owner, task=task)

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