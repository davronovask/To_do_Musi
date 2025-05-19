from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """Задача, привязанная к пользователю"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        """Строковое представление задачи"""
        return self.title

    class Meta:
        ordering = ['-id']
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
