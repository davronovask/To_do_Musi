from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    """Модель задачи, связанная с конкретным пользователем."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'  # user.tasks.all()
    )
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)


def __str__(self) -> str:
    """
    Возвращает строковое представление задачи — её заголовок.
    """
    return self.title


class Meta:
    ordering = ['-id']  # Новые задачи отображаются первыми
    verbose_name = 'Задача'
    verbose_name_plural = 'Задачи'