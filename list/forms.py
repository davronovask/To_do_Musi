from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Add a new task...',
                'class': 'task-input',
                'autocomplete': 'off',
            })
        }
        labels = {
            'title': ''
        }
