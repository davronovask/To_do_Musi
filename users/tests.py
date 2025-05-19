from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class UserAuthTests(TestCase):
    """Тесты для регистрации, логина и логаута пользователя"""

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.home_url = reverse('home')
        self.credentials = {
            'username': 'testuser',
            'password': 'testpass123'
        }

    def _register_user(self, username=None, password=None, first_name='Test', last_name='User', password2=None):
        """Вспомогательный метод для регистрации пользователя через POST-запрос"""
        if username is None:
            username = self.credentials['username']
        if password is None:
            password = self.credentials['password']
        if password2 is None:
            password2 = password
        return self.client.post(self.register_url, {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'password1': password,
            'password2': password2,
        })

    def _login_user(self, username=None, password=None):
        """Вспомогательный метод для логина пользователя"""
        if username is None:
            username = self.credentials['username']
        if password is None:
            password = self.credentials['password']
        return self.client.post(self.login_url, {
            'username': username,
            'password': password,
        }, follow=True)

    def test_register_user_success(self):
        """Проверяет успешную регистрацию нового пользователя"""
        response = self._register_user()
        self.assertRedirects(response, self.home_url)
        self.assertTrue(User.objects.filter(username=self.credentials['username']).exists())

    def test_register_user_password_mismatch(self):
        """Проверяет ошибку при несовпадении паролей при регистрации"""
        response = self._register_user(password='pass1234', password2='pass12345', username='wrongpass')
        self.assertFormError(response, 'form', 'password2', "The two password fields didn’t match.")
        self.assertFalse(User.objects.filter(username='wrongpass').exists())

    def test_register_user_existing_username(self):
        """Проверяет ошибку при попытке регистрации с уже существующим username"""
        User.objects.create_user(username='testuser', password='anypass')
        response = self._register_user()
        self.assertFormError(response, 'form', 'username', "A user with that username already exists.")
        self.assertEqual(User.objects.filter(username='testuser').count(), 1)

    def test_register_user_empty_username(self):
        """Проверяет ошибку при пустом username"""
        response = self._register_user(username='')
        self.assertFormError(response, 'form', 'username', "This field is required.")

    def test_login_user_success(self):
        """Проверяет успешный вход пользователя с правильными данными"""
        User.objects.create_user(**self.credentials)
        response = self._login_user()
        self.assertRedirects(response, self.home_url)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_user_fail(self):
        """Проверяет ошибку входа с неправильными данными"""
        response = self._login_user(username='wrong', password='wrongpass')
        self.assertContains(response, "Неверное имя пользователя или пароль.")
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_user(self):
        """Проверяет успешный выход пользователя и что он не аутентифицирован"""
        User.objects.create_user(**self.credentials)
        self.client.login(**self.credentials)
        response = self.client.post(self.logout_url, follow=True)
        self.assertRedirects(response, self.login_url)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
