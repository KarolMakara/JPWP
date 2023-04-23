from celery import shared_task
from apps.tasks.models import *


@shared_task()
def send_upcoming_task_notifications():
    for user in MyUser.objects.all():
        due_date_threshold = timezone.now() + timedelta(days=int(user.notification_before))
        user_tasks_due_soon = UserTask.objects.filter(due_date__lte=due_date_threshold)
        user_tasks_missed_deadline = UserTask.objects.filter(due_date__lt=timezone.now())

        for task in user_tasks_due_soon:

            if user_tasks_missed_deadline.filter(id=task.id).exists():
                notification_message = f"USER: Missed deadline for '{task.name}'!"
            else:
                notification_message = f"USER: Task '{task.name}' is due soon!"

            existing_notification, _ = Notification.objects.update_or_create(
                user_task=task,
                defaults={'message': notification_message, 'user': task.user_task_list.owner}
            )

    groups = MyGroup.objects.all()
    for group in groups:
        due_date_threshold = timezone.now() + timedelta(days=int(group.notification_before))
        members = group.members.all()
        for g in GroupTaskList.objects.filter(for_group=group):
            due_date_tasks = GroupTask.objects.filter(group_task_list=g, due_date__lte=due_date_threshold)

            missed_tasks = GroupTask.objects.filter(group_task_list=g, due_date__lt=timezone.now())
            for task in due_date_tasks:
                for member in members:
                    if missed_tasks.filter(id=task.id).exists():
                        notification_message = f"GROUP: Missed deadline for '{task.name}'!"
                    else:
                        notification_message = f"GROUP: Task '{task.name}' is due soon!"
                    existing_notification, _ = Notification.objects.update_or_create(
                        group_task=task,
                        user=member,
                        defaults={'message': notification_message, 'user': member}
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
