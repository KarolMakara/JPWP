# Generated by Django 4.2 on 2023-04-23 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='daily_report_at',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='notification_before',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
