from django.conf import settings
from django.db import models

# Create your models here.
from django.db.models import Count, F
from .manager import BoardManager


class Board(models.Model):
    name = models.CharField(verbose_name='name', help_text='', max_length=50, error_messages={}, db_column='name', unique=True, blank=False, null=False)
    description = models.CharField(verbose_name='description', help_text='', max_length=500, error_messages={}, db_column='description', blank=False, null=False)

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

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).annotate(last_updated_time=F('created_at')).annotate(last_updated_user=F('created_by__username')).first()

    def get_topics(self):
        return self.topics.select_related('starter').annotate(topic_starter=F('starter__username'))


class Topic(models.Model):
    subject = models.CharField(verbose_name='subject', help_text='', max_length=50, error_messages={}, db_column='subject', unique=True, blank=False, null=False)
    last_updated = models.DateTimeField(auto_now=True, help_text='', error_messages={}, db_column='last_updated', blank=False, null=False)
    board = models.ForeignKey(to=Board, on_delete=models.CASCADE, related_name='topics', related_query_name='topic', to_field='id', db_column='board', help_text='', error_messages={}, null=False, blank=False)
    starter = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='topics', related_query_name='topic', to_field='id', db_column='user', help_text='', error_messages={}, null=False, blank=False)

    class Meta:
        verbose_name = 'topic'
        verbose_name_plural = 'topics'
        db_table = 'topic'
        ordering = ['subject']

    def __str__(self):
        return self.subject

    def __repr__(self):
        return self.subject


class Post(models.Model):
    message = models.CharField(verbose_name='message', help_text='', max_length=100, error_messages={}, db_column='message', unique=False, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, help_text='', error_messages={}, db_column='created_at', blank=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, help_text='', error_messages={}, db_column='updated_at', blank=False, null=True)
    topic = models.ForeignKey(verbose_name='topic', to=Topic, on_delete=models.CASCADE, related_name='posts', related_query_name='post', to_field='id', db_column='topic', help_text='', error_messages={}, blank=False, null=False)
    created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts_created_by', related_query_name='post', to_field='id', db_column='created_by', help_text="", error_messages={}, blank=False, null=False)
    updated_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts_updated_by', related_query_name='post', to_field='id', db_column='updated_by', help_text="", error_messages={}, blank=True, null=True)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        db_table = 'post'
        ordering = ['-created_at']

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message
