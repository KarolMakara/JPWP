from datetime import time

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import *
from django import forms


class MyUser(AbstractUser):
    notification_before = models.IntegerField(default=1)
    daily_report_at = models.TimeField(default=time(hour=0, minute=0))


class MyGroup(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='owned_groups')
    members = models.ManyToManyField(MyUser, related_name='group_members')
    notification_before = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class MyGroupForm(forms.ModelForm):
    class Meta:
        model = MyGroup
        fields = ['name', 'members', 'notification_before']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['members'].widget.attrs.update(
            {'class': 'form-control', 'multiple': True, 'style': 'height: 100px'})
        self.fields['notification_before'].widget.attrs.update({'class': 'form-control'})


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('notification_before', 'daily_report_at')
        widgets = {
            'notification_before': forms.TextInput(attrs={'class': 'form-control'}),
            'daily_report_at': forms.TextInput(attrs={'type': 'time', 'class': 'form-control'}),
        }