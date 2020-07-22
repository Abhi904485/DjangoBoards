from django.test import TestCase
from django.urls import reverse, resolve

from accounts.models import User
from boards.models import Board, Topic
from boards.views import board_topics


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
