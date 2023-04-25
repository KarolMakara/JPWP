from django import forms
from .models import UserTask, GroupTask, Category, TaskList, UserTaskList, GroupTaskList


class BaseTaskForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        fields = ('name', 'category', 'description', 'due_date')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'due_date': forms.TextInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }


class UserTaskForm(BaseTaskForm):
    class Meta(BaseTaskForm.Meta):
        model = UserTask


class GroupTaskForm(BaseTaskForm):
    class Meta(BaseTaskForm.Meta):
        model = GroupTask


class BaseTaskListForm(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserTaskListForm(BaseTaskListForm):
    class Meta(BaseTaskListForm.Meta):
        model = UserTaskList


class GroupTaskListForm(BaseTaskListForm):
    class Meta(BaseTaskListForm.Meta):
        model = GroupTaskList
