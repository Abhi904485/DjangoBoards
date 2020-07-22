from django.test import TestCase
from django.urls import reverse, resolve

from boards.models import Board
from boards.views import home, board_topics


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
