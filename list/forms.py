from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    """
    Форма для добавления новой задачи.
    Использует только поле 'title'.
    """
    class Meta:
        model = Task
        fields = ['title']  # Только поле заголовка задачи
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Add a new task...',  # Подсказка внутри поля
                'class': 'task-input',               # CSS-класс для стилизации
                'autocomplete': 'off',               # Отключает автозаполнение браузером
            })
        }
        labels = {
            'title': ''
        }
    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError("Задача не может быть пустой.")
        return title
