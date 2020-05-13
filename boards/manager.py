from django.db import models
from .queryset import BoardQuerySet


class BoardManager(models.Manager):

    def get_queryset(self):
        return BoardQuerySet(model=self.model, using=self._db)

    def get_board_details(self):
        return self.get_queryset().board_topic_post_details()
