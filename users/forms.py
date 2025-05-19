from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from typing import Any


class RegisterForm(UserCreationForm):
    """Форма регистрации пользователя"""

    first_name = forms.CharField(
        max_length=30,
        label='Имя',
        widget=forms.TextInput(attrs={'placeholder': 'Введите имя'})
    )
    last_name = forms.CharField(
        max_length=30,
        label='Фамилия',
        widget=forms.TextInput(attrs={'placeholder': 'Введите фамилию'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Удаляет help_text у всех полей"""
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''
