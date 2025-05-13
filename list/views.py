from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Task
from .forms import TaskForm

@login_required
def home(request):
    tasks_active = Task.objects.filter(user=request.user, completed=False).order_by('-id')
    tasks_completed = Task.objects.filter(user=request.user, completed=True).order_by('-id')
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('home')
    return render(request, 'home.html', {
        'form': form,
        'tasks_active': tasks_active,
        'tasks_completed': tasks_completed
    })

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = True
    task.save()
    return redirect('home')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('home')

@require_POST
@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    new_title = request.POST.get('title')
    if new_title:
        task.title = new_title
        task.save()
    return redirect('home')