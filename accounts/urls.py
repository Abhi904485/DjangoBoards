from django.conf.urls import url

from .views import (
    change_password,
    change_password_done,
    password_reset_complete,
    signin,
    signup,
    signout,
    password_reset_view,
    password_reset_done,
    password_reset_confirm,
    profile
)

app_name = "accounts"
urlpatterns = [
    url(r'signup/$', signup, name='sign-up'),
    url(r'signin/$', signin, name='sign-in'),
    url(r'signout/$', signout, name='sign-out'),
    url(r'password_reset/$', password_reset_view, name='password_reset'),
    url(r'password_rest_done/$', password_reset_done, name='password_reset_done'),
    url(r'reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,100})/$', password_reset_confirm,
        name='password_reset_confirm'),
    url(r'password_change/$', change_password, name='password_change'),
    url(r'password_change/done$', change_password_done, name='password_change_done'),
    url(r'reset/complete/$', password_reset_complete, name='password_reset_complete'),
    url(r'profile/$', profile, name='profile'),
]
