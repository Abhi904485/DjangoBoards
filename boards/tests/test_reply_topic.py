from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework import status

from accounts.models import User
from boards.forms import ReplyPostForm
from boards.models import Board, Topic, Post
from boards.utility import get_pagination
from boards.views import reply_topic


class ReplyTopicTestCase(TestCase):
    """
    Base test case to be used in all `reply_topic` view tests
    """

    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        self.username = 'john'
        self.password = '123'
        self.email = 'john@doe.com'
        user = User.objects.create_user(username=self.username, email=self.email, password=self.password)
        self.topic = Topic.objects.create(subject='Hello, world', board=self.board, starter=user)
        self.post = Post.objects.create(message='Lorem ipsum dolor sit amet', topic=self.topic, created_by=user)
        self.url = reverse('boards:reply_topic', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})


class LoginRequiredReplyTopicTests(ReplyTopicTestCase):
    def test_redirection(self):
        login_url = reverse('accounts:sign-in')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


class ReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.email, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(first=self.response.status_code, second=status.HTTP_200_OK)

    def test_view_function(self):
        view = resolve('/boards/1/topics/1/reply/')
        self.assertEquals(view.func, reply_topic)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ReplyPostForm)

    def test_form_inputs(self):
        """
        The view must contain two inputs: csrf, message textarea
        """
        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<textarea', 1)


class SuccessfulReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.email, password=self.password)
        self.response = self.client.post(self.url, {'message': 'hello, world!'})

    def test_redirection(self):
        """
        A valid form submission should redirect the user
        """
        topic_posts_url = reverse('boards:topic_posts', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})
        topic_post_url = '{url}?page={page}#{id}'.format(
            url=topic_posts_url,
            id=self.post.pk + 1,
            page=get_pagination(self.topic.get_all_posts(), 1, 2).paginator.num_pages
        )
        self.assertRedirects(self.response, topic_post_url)

    def test_reply_created(self):
        """
        The total post count should be 2
        The one created in the `ReplyTopicTestCase` setUp
        and another created by the post data in this class
        """
        self.assertEquals(Post.objects.count(), 2)


class InvalidReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        """
        Submit an empty dictionary to the `reply_topic` view
        """
        super().setUp()
        self.client.login(username=self.email, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        """
        An invalid form submission should return to the same page
        """
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
