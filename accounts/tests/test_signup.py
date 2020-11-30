from django.test import TestCase
from django.urls import resolve
from django.shortcuts import reverse
from rest_framework import status
from ..views import signup
from ..forms import UserCreationForm
from ..models import User


class SignupTests(TestCase):
    def setUp(self):
        self.url = reverse('accounts:sign-up')
        self.view = resolve('/user/signup/')
        self.response = self.client.get(self.url)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_signup_status_code(self):
        self.assertEquals(first=self.response.status_code, second=status.HTTP_200_OK, msg="Test Signup Status Code 200")

    def test_signup_url_resolves_signup_view(self):
        self.assertEquals(first=self.view.func, second=signup, msg="Function name is Signup")

    def test_signup_view_contains_board_link(self):
        self.assertContains(response=self.response, text=reverse('boards:home'), status_code=status.HTTP_200_OK,
                            msg_prefix="No Board Link present in Sign up Page")
        self.assertContains(response=self.response, text="Django Boards", status_code=status.HTTP_200_OK,
                            msg_prefix="No Text with name Django Boards Link present in Sign up Page")

    def test_signup_view_contains_login_link(self):
        self.assertContains(response=self.response, text=reverse('accounts:sign-in'), status_code=status.HTTP_200_OK,
                            msg_prefix="No Login Link present in Sign up Page", count=1)

    def test_signup_view_check_form_on_get(self):
        user_creation_form = self.response.context.get('form')
        self.assertIsInstance(user_creation_form, UserCreationForm,
                              msg="User Creation Form instance is loaded on Signup page")

    def test_form_inputs(self):
        self.assertContains(response=self.response, text='<input', count=7)
        self.assertContains(response=self.response, text='type="text"', count=3)
        self.assertContains(response=self.response, text='type="email"', count=1)
        self.assertContains(response=self.response, text='type="password"', count=2)


class SuccessfulSignupTests(TestCase):
    def setUp(self) -> None:
        self.url = reverse('accounts:sign-up')
        self.view = resolve(self.url)
        self.response = self.client.get(self.url)
        self.valid_data = {
            'email': "test@gmail.com",
            'first_name': "first_test",
            'last_name': "last_test",
            'username': "user_test",
            'password1': "test@123",
            'password2': "test@123"
        }
        self.response = self.client.post(self.url, data=self.valid_data, follow=True)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_redirection(self):
        self.assertRedirects(response=self.response, expected_url=reverse("boards:home"),
                             status_code=status.HTTP_302_FOUND,
                             target_status_code=status.HTTP_200_OK,
                             msg_prefix="On Successful Sign Up User Will logged in and redirected to Home page")

    def test_user_authentication(self):
        response = self.client.get(reverse('boards:home'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):
    def setUp(self):
        self.url = reverse('accounts:sign-up')
        self.response = self.client.post(self.url, {})
        self.invalid_data = {
            'email': "test@gmail.com",
            'first_name': "first_test",
            'last_name': "last_test",
            'username': " ",
            'password1': "test@123",
            'password2': "test123"
        }

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())

    def test_signup_view_invalid_or_missing_post_data(self):
        response = self.client.post(self.url, data=self.invalid_data)
        user_creation_form = self.response.context.get('form')
        user = User.objects.filter(email__iexact="test@gmail.com", first_name__iexact="first_test",
                                   last_name__iexact="last_test", username__iexact="user_test").first()
        self.assertNotIsInstance(user, User, msg="user is not instance of User")
        self.assertIsInstance(user, type(None), msg="User is Instance of None")
        self.assertContains(response=response, text="Sign up", status_code=status.HTTP_200_OK,
                            msg_prefix="On Failed Sign Up User Will redirected to Signup page", count=2)
        self.assertIsInstance(user_creation_form, UserCreationForm)

    def test_signup_view_empty_post_data(self):
        response = self.client.post(self.url, data={})
        user_creation_form = self.response.context.get('form')
        self.assertContains(response=response, text="Sign up", status_code=status.HTTP_200_OK,
                            msg_prefix="On Failed Sign Up User Will redirected to Signup page", count=2)
        self.assertIsInstance(user_creation_form, UserCreationForm)


class SignUpFormTest(TestCase):
    def setUp(self) -> None:
        self.form = UserCreationForm()

    def test_form_has_fields(self):
        expected = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']
        actual = list(self.form.fields)
        self.assertSequenceEqual(expected, actual)
