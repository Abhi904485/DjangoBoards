from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .manager import UserManager


# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=_('Email address'), unique=True, db_column='email', help_text="", error_messages={})
    first_name = models.CharField(verbose_name=_('First name'), max_length=30, blank=True, null=True, db_column='first_name', help_text="", error_messages={})
    last_name = models.CharField(verbose_name=_('Last name'), max_length=30, blank=True, null=True, db_column='last_name', help_text="", error_messages={})
    username = models.CharField(verbose_name=_('Username'), max_length=100, blank=True, null=True, db_column='username', help_text="", error_messages={})
    date_joined = models.DateTimeField(verbose_name=_('Date joined'), auto_now_add=True, db_column='date_joined', help_text="", error_messages={})
    active = models.BooleanField(verbose_name=_('Active'), default=True, db_column='active', help_text="", error_messages={}),
    is_staff = models.BooleanField(verbose_name=_('Is staff'), default=False, db_column='is_staff', help_text="", error_messages={})
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'user'

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_sort_name(self):
        return "{}".format(self.first_name)
