from django.test import TestCase
from django.urls import reverse, resolve
from ..forms import PasswordChangeForm
from accounts.models import User
from accounts.views import change_password


class PasswordChangeTests(TestCase):
    def setUp(self):
        username = 'john'
        password = 'secret123'
        email = 'john@doe.com'
        user = User.objects.create_user(username=username, email=email, password=password)
        url = reverse('accounts:password_change')
        self.client.login(username=email, password=password)
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolves_correct_view(self):
        view = resolve('/user/password_change/')
        self.assertEquals(view.func, change_password)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordChangeForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="password"', 2)


class PasswordChangeTestCase(TestCase):
    def setUp(self, data=None):
        if data is None:
            data = {}
        self.user = User.objects.create_user(username='john', email='john@doe.com', password='old_password')
        self.url = reverse('accounts:password_change')
        self.client.login(username='john@doe.com', password='old_password')
        self.response = self.client.post(self.url, data)
        self.client.login(username='john@doe.com', password='new_password')


class SuccessfulPasswordChangeTests(PasswordChangeTestCase):
    def setUp(self, **kwargs):
        data = {
            'password1': 'old_password',
            'password2': 'new_password',
        }
        super().setUp(data=data)

    def test_redirection(self):
        '''
        A valid form submission should redirect the user
        '''
        self.assertRedirects(self.response, reverse('accounts:password_change_done'))

    def test_password_changed(self):
        '''
        refresh the user instance from database to get the new password
        hash updated by the change password view.
        '''
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))

    def test_user_authentication(self):
        '''
        Create a new request to an arbitrary page.
        The resulting response should now have an `user` to its context, after a successful sign up.
        '''
        response = self.client.get(reverse('boards:home'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidPasswordChangeTests(PasswordChangeTestCase):
    def test_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_didnt_change_password(self):
        '''
        refresh the user instance from the database to make
        sure we have the latest data.
        '''
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('old_password'))
