from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from list.models import Task

class HomePageTests(TestCase):
    def setUp(self):
        """Создаем пользователя и нужные данные для тестирования"""
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='12345')
        self.client.login(username='user', password='12345')
        self.url = reverse('home')

    def test_home_status_code(self):
        """Проверяет, что страница /home/ открывается (код 200)"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_home_template_used(self):
        """Проверяет, что используется шаблон home.html"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'home.html')

    def test_user_name_visible(self):
        """Имя пользователя отображается в боковой панели"""
        response = self.client.get(self.url)
        self.assertContains(response, self.user.username)

    def test_create_new_task(self):
        """Создание новой задачи через форму на главной"""
        response = self.client.post(self.url, {'title': 'New Task'})
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertEqual(task.title, 'New Task')
        self.assertEqual(task.user, self.user)
        self.assertRedirects(response, self.url)

    def test_display_active_and_completed_tasks(self):
        """Задачи делятся на активные и завершённые"""
        Task.objects.create(title='Active Task', user=self.user, completed=False)
        Task.objects.create(title='Done Task', user=self.user, completed=True)

        response = self.client.get(self.url)

        self.assertContains(response, 'Active Task')
        self.assertContains(response, 'Done Task')
