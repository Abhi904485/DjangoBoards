import math

from django.conf import settings
from django.core.paginator import Paginator
from django.db import models

# Create your models here.
from django.db.models import F, Count
from django.utils.safestring import mark_safe
from django.utils.text import Truncator
from markdown import markdown

from .manager import BoardManager


class Board(models.Model):
    name = models.CharField(verbose_name='name', help_text='', max_length=50, error_messages={}, db_column='name',
                            unique=True, blank=False, null=False)
    description = models.CharField(verbose_name='description', help_text='', max_length=500, error_messages={},
                                   db_column='description', blank=False, null=False)

    objects = BoardManager()

    class Meta:
        verbose_name = 'board'
        verbose_name_plural = 'boards'
        db_table = 'board'
        ordering = ['name']

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @property
    def get_last_post_updated_time_updated_user(self):
        return Post.objects.filter(topic__board=self).values('created_at', 'created_by__username', 'topic_id').first()

    def get_topics(self):
        return self.topics.order_by('-last_updated').annotate(topic_starter=F('starter__username')).annotate(
            replies=Count('post') - 1)


class Topic(models.Model):
    subject = models.CharField(verbose_name='subject', help_text='', max_length=50, error_messages={},
                               db_column='subject', unique=True, blank=False, null=False)
    last_updated = models.DateTimeField(auto_now=True, help_text='', error_messages={}, db_column='last_updated',
                                        blank=False, null=False)
    board = models.ForeignKey(to=Board, on_delete=models.CASCADE, related_name='topics', related_query_name='topic',
                              to_field='id', db_column='board', help_text='', error_messages={}, null=False,
                              blank=False)
    starter = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='topics',
                                related_query_name='topic', to_field='id', db_column='user', help_text='',
                                error_messages={}, null=False, blank=False)
    views = models.PositiveIntegerField(verbose_name='views', help_text='', error_messages={},
                                        db_column='views', default=0, )

    class Meta:
        verbose_name = 'topic'
        verbose_name_plural = 'topics'
        db_table = 'topic'
        ordering = ['subject']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.post_count = math.ceil(self.get_all_posts().count()/2)

    def __str__(self):
        return self.subject

    def __repr__(self):
        return self.subject

    def get_all_posts(self):
        return self.posts.all().order_by('created_at')

    def has_many_pages(self):
        return True if self.post_count > 10 else False

    def get_page_range(self):
        count = self.post_count
        if self.has_many_pages():
            return range(1, count)
        return range(1, count + 1)


class Post(models.Model):
    message = models.TextField(verbose_name='message', help_text='', max_length=100, error_messages={},
                               db_column='message', unique=False, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, help_text='', error_messages={}, db_column='created_at',
                                      blank=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, help_text='', error_messages={}, db_column='updated_at',
                                      blank=False, null=True)
    topic = models.ForeignKey(verbose_name='topic', to=Topic, on_delete=models.CASCADE, related_name='posts',
                              related_query_name='post', to_field='id', db_column='topic', help_text='',
                              error_messages={}, blank=False, null=False)
    created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='posts_created_by', related_query_name='post', to_field='id',
                                   db_column='created_by', help_text="", error_messages={}, blank=False, null=False)
    updated_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='posts_updated_by', related_query_name='post', to_field='id',
                                   db_column='updated_by', help_text="", error_messages={}, blank=True, null=True)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        db_table = 'post'
        ordering = ['-created_at']

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    def __repr__(self):
        return self.message

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))
