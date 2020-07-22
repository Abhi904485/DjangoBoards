from django.contrib.auth import authenticate
from django.shortcuts import reverse
from django.test import TestCase
from django.urls import resolve

from boards.forms import NewTopicForm
from boards.models import Board, Topic, Post
from boards.views import new_topic
from accounts.models import User


class NewTopicTest(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name="board", description="board")
        self.user = User.objects.create_user(username='test', password='test@123', email='test@gmail.com')
        self.url = reverse('new_topic', kwargs={'pk': self.board.pk})
        self.view = resolve(reverse('new_topic', kwargs={'pk': self.board.pk}))
        self.client.login(email='test@gmail.com', password='test@123')
        self.response = self.client.get(self.url)

    def test_new_topic_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        self.url = reverse('new_topic', kwargs={'pk': 99})
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 404)

    def test_topics_url_resolves_new_topic_view(self):
        self.assertEquals(self.view.func, new_topic)

    def test_new_topic_view_success_contains_link_back_to_topics_page(self):
        topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, topics_url)

    def test_new_topic_view_not_found_contains_link_back_to_topics_page(self):
        topics_url = reverse('board_topics', kwargs={'pk': 99})
        self.assertNotContains(self.response, topics_url)

    def test_new_topic_view_success_contains_link_back_to_home_page(self):
        topics_url = reverse('home')
        self.assertContains(self.response, topics_url)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_new_topic_check_form_on_post_redirect_to_topics_view(self):
        response = self.client.post(self.url, data={'subject': 'topic', 'message': 'this is first post on topic'})
        self.assertEquals(response.status_code, 302)

    def test_new_topic_check_form_on_get(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

    def test_new_topic_valid_post_data(self):
        self.client.post(self.url, data={'subject': 'topic', 'message': 'this is first post on topic'})
        self.assertTrue(Topic.objects.exists() and Topic.objects.first().subject == 'topic')
        self.assertTrue(Post.objects.exists() and Post.objects.first().message == 'this is first post on topic')

    def test_new_topic_invalid_post_data(self):
        response = self.client.post(self.url, data={})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_topic_empty_post_data(self):
        response = self.client.post(self.url, data={'subject': '', 'message': ''})
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists() and Topic.objects.first().subject == 'topic')
        self.assertFalse(Post.objects.exists() and Post.objects.first().message == 'this is first post on topic')
