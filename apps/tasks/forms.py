from django import forms
from .models import UserTask


class UserTaskForm(forms.ModelForm):
    class Meta:
        model = UserTask
        fields = ('name', 'description', 'due_date')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'due_date': forms.TextInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }






