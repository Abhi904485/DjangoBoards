from django.db import models

from django.db.models import Count


class BoardQuerySet(models.QuerySet):
    def last_post(self):
        pass

    def board_topic_post_details(self):
        return self.prefetch_related('topics').annotate(posts=Count('topic__post'))
