# Generated by Django 4.2 on 2023-04-26 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0021_alter_task_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='completed_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]