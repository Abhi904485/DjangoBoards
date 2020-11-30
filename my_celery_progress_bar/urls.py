from django.conf.urls import url
from django.urls import include

from .views import UserListView, create_user_view

app_name = "my_celery_progress_bar"
urlpatterns = [
    url(r'user-list/$', UserListView.as_view(), name='user-list'),
    url(r'create-user1/$', create_user_view, name='create-user1'),
    url(r'celery-progress/', include('celery_progress.urls', namespace="celery_progress"), name='celery-progress')
]
