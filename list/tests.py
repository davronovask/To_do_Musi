from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task

class HomePageTests(TestCase):
    def setUp(self):
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

        
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task

class HomePageTests(TestCase):
    def setUp(self):
        # Создаем клиента и пользователя
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='12345')
        # Логинимся под этим пользователем
        self.client.login(username='user', password='12345')
        # Получаем ссылку на главную страницу
        self.url = reverse('home')

    def test_home_page_works(self):
        # Проверяем, что главная страница открывается
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        # Проверяем, что используется нужный шаблон
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'home.html')

    def test_username_shown_on_page(self):
        # Проверяем, что имя пользователя есть на странице
        response = self.client.get(self.url)
        self.assertContains(response, self.user.username)

    def test_can_create_task(self):
        # Проверяем, что можно создать новую задачу через форму
        response = self.client.post(self.url, {'title': 'Новая задача'})
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertEqual(task.title, 'Новая задача')
        self.assertEqual(task.user, self.user)
        self.assertRedirects(response, self.url)

    def test_tasks_show_active_and_done(self):
        # Создаем активную и выполненную задачу
        Task.objects.create(title='Активная задача', user=self.user, completed=False)
        Task.objects.create(title='Выполненная задача', user=self.user, completed=True)

        response = self.client.get(self.url)

        # Проверяем, что обе задачи видны на странице
        self.assertContains(response, 'Активная задача')
        self.assertContains(response, 'Выполненная задача')
