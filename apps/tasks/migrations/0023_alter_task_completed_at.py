# Generated by Django 4.2 on 2023-04-26 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0022_alter_task_completed_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
