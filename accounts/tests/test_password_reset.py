from ..forms import PasswordResetForm
from ..views import password_reset_view
from ..models import User
from django.core import mail
from django.shortcuts import reverse
from django.urls import resolve
from django.test import TestCase


class PasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('accounts:password_reset')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/user/password_reset/')
        self.assertEquals(view.func, password_reset_view)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)

    def test_form_inputs(self):
        '''
        The view must contain two inputs: csrf and email
        '''
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)


class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        email = 'john@gmail.com'
        User.objects.create_user(username='john', email=email, password='123abcdef')
        url = reverse('accounts:password_reset')
        self.response = self.client.post(url, {'email': email})

    def test_redirection(self):
        url = reverse('accounts:password_reset_done')
        self.assertRedirects(self.response, url, status_code=302, target_status_code=200)

    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))


class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        self.url = reverse('accounts:password_reset')
        self.response = self.client.post(self.url, {'email': 'donotexist@email.com'})

    def test_render_same_page(self):
        self.assertContains(self.response, 'Password Reset')

    def test_no_reset_email_sent(self):
        self.assertEqual(0, len(mail.outbox))
