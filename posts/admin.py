# posts/admin.py
from django.contrib import admin
from .models import Post, Comment, Like  # Ensure this import is correct

# Register your models here
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)