from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'completed')  # Показывать в таблице
    search_fields = ('title',)                     # Поиск по названию задачи
    list_filter = ('completed', 'user')            # Фильтрация по статусу и пользователю
