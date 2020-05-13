"""DjangoBoards URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from boards import views as b_views
from accounts import views as a_views

urlpatterns = [
    url(r'^$', b_views.home, name='home'),
    url(r'signup/$', a_views.signup, name='sign-up'),
    url(r'signin/$', a_views.signin, name='sign-in'),
    url(r'signout/$', a_views.signout, name='sign-out'),
    url(r'boards/(?P<pk>\d+)/$', b_views.board_topics, name="board_topics"),
    url(r'boards/(?P<pk>\d+)/new_topic/$', b_views.new_topic, name="new_topic"),
    url(r'^password_reset/$', a_views.password_reset_view, name='password_reset'),
    url(r'^password_rest_done/$', a_views.password_reset_done, name='password_reset_done'),
    url(r'password_change/$', a_views.change_password, name='password_change'),
    url(r'password_change/done$', a_views.change_password_done, name='password_change_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        a_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/complete/$', a_views.password_reset_complete, name='password_reset_complete'),
    url(r'^celery/', include('my_celery_progress_bar.urls', namespace='my_celery_progress_bar')),
    url(r'^celery-progress/', include('celery_progress.urls', namespace="celery_progress"), name='celery-progress'),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
