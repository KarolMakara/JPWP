# Generated by Django 4.2 on 2023-04-23 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0017_alter_notification_group_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='completed_at',
            field=models.DateField(null=True),
        ),
    ]
