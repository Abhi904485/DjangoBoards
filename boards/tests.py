from django.shortcuts import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import resolve

from .views import home, board_topics, new_topic
from .models import Board, Topic, Post
from .forms import NewTopicForm


class HomeTests(TestCase):

    def setUp(self):
        self.board = Board.objects.create(name="test", description="test")
        self.url = reverse('home')
        self.view = resolve('/')
        self.response = self.client.get(self.url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        self.assertEquals(self.view.func, home)

    def test_home_url_not_resolves_home_view(self):
        self.assertNotEquals(self.view.func, board_topics)

    def test_home_view_success_contains_link_to_topics_page(self):
        topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, topics_url)

    def test_home_view_not_found_contains_link_to_topics_page(self):
        topics_url = reverse('board_topics', kwargs={'pk': 99})
        self.assertNotContains(self.response, topics_url)


class TopicTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name="board", description="board")
        self.user = User.objects.create(username='test', password='test@123', email='test@gmail.com')
        self.topic = Topic.objects.create(subject='topic', starter=self.user, board=self.board)
        self.url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.view = resolve(reverse('board_topics', kwargs={'pk': self.board.pk}))
        self.response = self.client.get(self.url)

    def test_topic_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_topic_view_not_found_status_code(self):
        self.url = reverse('board_topics', kwargs={'pk': 99})
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 404)

    def test_home_url_resolves_topic_view(self):
        self.assertEquals(self.view.func, board_topics)

    def test_topic_view_contains_link_to_home_page(self):
        home_url = reverse('home')
        self.assertContains(self.response, home_url)

    def test_new_topic_create_button_success_in_topics_page(self):
        self.assertContains(self.response, reverse('new_topic', kwargs={'pk': self.board.pk}))

    def test_new_topic_create_button_not_found_in_topics_page(self):
        self.assertNotContains(self.response, reverse('new_topic', kwargs={'pk': 99}))


class NewTopicTest(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name="board", description="board")
        self.user = User.objects.create(username='test', password='test@123', email='test@gmail.com')
        self.url = reverse('new_topic', kwargs={'pk': self.board.pk})
        self.view = resolve(reverse('new_topic', kwargs={'pk': self.board.pk}))
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
