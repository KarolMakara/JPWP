import django
import humanize
from celery import shared_task

from apps.tasks.models import *

@shared_task()
def send_upcoming_task_notifications():
    from django.utils import timezone
    import datetime

    now = timezone.now().astimezone(timezone.utc)
    now = now.replace(second=0, microsecond=0)

    for user in MyUser.objects.all():
        daily_report = Notification.objects.filter(user=user, message='Daily report').first()

        user_datetime = timezone.make_aware(datetime.datetime.combine(timezone.now().date(), user.daily_report_at))
        user_time = user_datetime.astimezone(timezone.utc).replace(second=0, microsecond=0)

        if now == user_time:
            if not daily_report:
                Notification.objects.create(message='Daily report', user=user)
            elif daily_report.seen is True:
                daily_report.seen = False
                daily_report.save()

        due_date_threshold = timezone.now() + timedelta(days=int(user.notification_before))
        user_tasks_due_soon = UserTask.objects.filter(due_date__lte=due_date_threshold)
        user_tasks_missed_deadline = UserTask.objects.filter(due_date__lt=timezone.now())

        for task in user_tasks_due_soon:

            if user_tasks_missed_deadline.filter(id=task.id).exists():
                notification_message = f"USER: Missed deadline for '{task.name}'!"
            else:
                time_due = humanize.precisedelta(timezone.now() - task.due_date, minimum_unit="minutes", format="%d")
                notification_message = f"USER: Task '{task.name}' is due soon! ({time_due})"

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
                        time_due = humanize.precisedelta(timezone.now() - task.due_date, minimum_unit="minutes",
                                                         format="%d")
                        notification_message = f"GROUP: Task '{task.name}' is due soon! ({time_due})"
                    existing_notification, _ = Notification.objects.update_or_create(
                        group_task=task,
                        user=member,
                        defaults={'message': notification_message, 'user': member}
                    )


