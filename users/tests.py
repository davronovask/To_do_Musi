from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class UserAuthTests(TestCase):
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

    def test_register_user_success(self):
        response = self.client.post(self.register_url, {
            'first_name': 'Test',
            'last_name': 'User',
            'username': self.credentials['username'],
            'password1': self.credentials['password'],
            'password2': self.credentials['password'],
        })
        self.assertRedirects(response, self.home_url)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_user_password_mismatch(self):
        response = self.client.post(self.register_url, {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'wrongpass',
            'password1': 'pass1234',
            'password2': 'pass12345',
        })
        self.assertContains(response, "The two password fields didn’t match.")
        self.assertFalse(User.objects.filter(username='wrongpass').exists())

    def test_login_user_success(self):
        User.objects.create_user(**self.credentials)
        response = self.client.post(self.login_url, self.credentials, follow=True)
        self.assertRedirects(response, self.home_url)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_user_fail(self):
        response = self.client.post(self.login_url, {
            'username': 'wrong',
            'password': 'wrongpass'
        }, follow=True)
        self.assertContains(response, "Incorrect username or password.")

    def test_logout_user(self):
        User.objects.create_user(**self.credentials)
        self.client.login(**self.credentials)
        response = self.client.post(self.logout_url, follow=True)
        self.assertRedirects(response, self.login_url)
        self.assertFalse(response.context['user'].is_authenticated)
