from django.db import models

from django.db.models import Count


class BoardQuerySet(models.QuerySet):

    def board_topic_post_details(self):
        return self.annotate(topics_count=Count('topic', distinct=True)).annotate(
            posts_count=Count('topic__post', distinct=True))
