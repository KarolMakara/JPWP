# Generated by Django 4.2 on 2023-04-23 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_myuser_daily_report_at'),
        ('tasks', '0011_alter_task_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grouptasklist',
            name='for_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.mygroup'),
        ),
    ]
