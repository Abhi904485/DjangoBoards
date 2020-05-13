from django.conf.urls import url
from .views import UserListView,  create_user_view

app_name = "my_celery_progress_bar"
urlpatterns = [
    url(r'user-list/$', UserListView.as_view(), name='user-list'),
    url(r'create-user1/$', create_user_view, name='create-user1'),
]
