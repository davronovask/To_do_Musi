from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from .forms import RegisterForm

def register(request: HttpRequest) -> HttpResponse:
    """
    Обрабатывает регистрацию нового пользователя.

    При GET-запросе отображает форму регистрации.
    При POST-запросе проверяет данные формы, создаёт пользователя и выполняет вход.

    Args:
        request (HttpRequest): объект запроса.

    Returns:
        HttpResponse: страницу с формой или перенаправление на главную страницу.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})
