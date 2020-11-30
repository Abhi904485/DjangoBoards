from django.test import TestCase
from django.urls import reverse, resolve

from accounts.views import password_reset_complete


class PasswordResetCompleteTests(TestCase):
    def setUp(self):
        url = reverse('accounts:password_reset_complete')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/user/reset/complete/')
        self.assertEquals(view.func , password_reset_complete)