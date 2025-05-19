from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task


class HomePageTests(TestCase):
    """Тесты для главной страницы"""

    def setUp(self):
        """Создание пользователя и вход в систему"""
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='12345')
        self.client.login(username='user', password='12345')
        self.url = reverse('home')

    def test_home_status_code(self):
        """Страница доступна (код 200)"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_home_template_used(self):
        """Используется шаблон home.html"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'home.html')

    def test_user_name_visible(self):
        """Имя пользователя отображается на странице"""
        response = self.client.get(self.url)
        self.assertContains(response, self.user.username)

    def test_create_new_task(self):
        """Можно создать новую задачу"""
        response = self.client.post(self.url, {'title': 'Новая задача'})
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertEqual(task.title, 'Новая задача')
        self.assertEqual(task.user, self.user)
        self.assertRedirects(response, self.url)

    def test_display_active_and_completed_tasks(self):
        """Отображаются активные и завершённые задачи"""
        Task.objects.create(title='Активная задача', user=self.user, completed=False)
        Task.objects.create(title='Выполненная задача', user=self.user, completed=True)

        response = self.client.get(self.url)
        self.assertContains(response, 'Активная задача')
        self.assertContains(response, 'Выполненная задача')
