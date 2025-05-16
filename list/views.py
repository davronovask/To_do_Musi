from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from .models import Task
from .forms import TaskForm


def get_user_task(task_id: int, user) -> Task:
    """Получить задачу по id, принадлежащую пользователю, или вернуть 404."""
    return get_object_or_404(Task, id=task_id, user=user)


@login_required
def home(request: HttpRequest) -> HttpResponse:
    """
    Главная страница. Показывает задачи пользователя — активные и выполненные.
    Также показывает форму для добавления новой задачи и смены пароля.
    Если пришёл POST-запрос с задачей, добавляет её.
    """
    tasks_active = Task.objects.filter(user=request.user, completed=False).order_by('-id')
    tasks_completed = Task.objects.filter(user=request.user, completed=True).order_by('-id')
    form = TaskForm()
    password_form = PasswordChangeForm(user=request.user)

    if request.method == 'POST' and 'title' in request.POST:
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('home')

    return render(request, 'home.html', {
        'form': form,
        'tasks_active': tasks_active,
        'tasks_completed': tasks_completed,
        'password_form': password_form,
    })


@login_required
def complete_task(request: HttpRequest, task_id: int) -> HttpResponse:
    """
    Помечает задачу как выполненную.
    """
    task = get_user_task(task_id, request.user)
    task.completed = True
    task.save()
    return redirect('home')


@login_required
def delete_task(request: HttpRequest, task_id: int) -> HttpResponse:
    """
    Удаляет задачу пользователя.
    """
    task = get_user_task(task_id, request.user)
    task.delete()
    return redirect('home')


@require_POST
@login_required
def update_task(request: HttpRequest, task_id: int) -> HttpResponse:
    """
    Обновляет название задачи, если оно не пустое.
    """
    task = get_user_task(task_id, request.user)
    new_title = request.POST.get('title')
    if new_title:
        task.title = new_title
        task.save()
    else:
        messages.error(request, "Название задачи не может быть пустым.")
    return redirect('home')


@require_POST
@login_required
def change_password_modal(request: HttpRequest) -> HttpResponse:
    """
    Обрабатывает смену пароля через модальное окно.
    """
    form = PasswordChangeForm(user=request.user, data=request.POST)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Пароль успешно изменён.")
    else:
        for error in form.errors.values():
            messages.error(request, error)
    return redirect('home')
