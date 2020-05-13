from django.contrib import admin

from .models import Topic, Board, Post

# Register your models here.
admin.site.register(Topic)
admin.site.register(Board)
admin.site.register(Post)
