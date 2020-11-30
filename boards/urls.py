from django.conf.urls import url

from .views import board_topics, new_topic, home, topic_posts, reply_topic , edit_post

app_name = "boards"

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'boards/(?P<pk>\d+)/$', board_topics, name="board_topics"),
    url(r'boards/(?P<pk>\d+)/new_topic/$', new_topic, name="new_topic"),
    url(r'boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', topic_posts, name="topic_posts"),
    url(r'boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', reply_topic, name='reply_topic'),
    url(r'boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$', edit_post, name='edit_post'),
]
