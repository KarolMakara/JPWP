# Generated by Django 4.2 on 2023-04-21 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='task',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='tasks.usertask'),
        ),
    ]
